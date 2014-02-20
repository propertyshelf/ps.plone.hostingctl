# -*- coding: utf-8 -*-

# python imports
from chef import ChefError

# zope imports
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from z3c.form import button, field, form

# plone imports
from plone import api
from plone.z3cform import layout

# local imports
from .interfaces import IDatabag, IDatabagItem
from propertyshelf.plone.hosting.interfaces import IChefTool
from propertyshelf.plone.hosting.i18n import _


class DatabagViewForm(form.Form):
    """
        The form that is shown directly below the table view
    """

    def update_path(self, traverse_subpath):
        self.traverse_subpath = traverse_subpath

    @button.buttonAndHandler(_(u'Create'), name='create')
    def handle_create(self, action):
        data, errors = self.extractData()
        add_url = ""
        if len(self.traverse_subpath) == 0:
            add_url = self.context.absolute_url() + '/create-databag'
        elif len(self.traverse_subpath) == 1:
            add_url = '%s/create-item/%s' % (
                self.context.absolute_url(),
                self.traverse_subpath[0])
        self.request.response.redirect(add_url)


@implementer(IPublishTraverse)
class DatabagView(BrowserView):
    """
        The main view for showing the listings of databags or the listing
        of databag items. The context is determined by the traversal subpath,
        parsing it to determine whether the view will be for a specific
        databag, databag item, etc.
    """

    index = ViewPageTemplateFile("templates/databags.pt")

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.form = DatabagViewForm(context, request)
        self.traverse_subpath = []
        self.tool = queryUtility(IChefTool)

    def __call__(self):
        if len(self.traverse_subpath) > 1:
            self.form = None
        else:
            self.form.update_path(self.traverse_subpath)
        super(DatabagView, self).__call__()
        return self.index()

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    @property
    def available(self):
        if self.tool is not None:
            return self.tool.authenticated

    def list_databags(self):
        if len(self.traverse_subpath) == 0:
            return self.tool.get_databags()

    def databag_items(self):
        if len(self.traverse_subpath) == 1:
            databag = self.traverse_subpath[0]
            return self.tool.get_databag_items(databag)

    def databag_item_details(self):
        if len(self.traverse_subpath) == 2:
            databag = self.traverse_subpath[0]
            item = self.traverse_subpath[1]
            return self.tool.get_data_from_item(databag, item)


class AddDatabagForm(form.AddForm):
    """
        Add form to create a new databag of type IDatabag
    """

    fields = field.Fields(IDatabag)
    label = _(u'Add Databag')

    def createAndAdd(self, data):
        chef_tool = queryUtility(IChefTool)
        self.databag_name = data.get('name')
        try:
            return chef_tool.create_databag(self.databag_name)
        except ChefError as e:
            api.portal.show_message(
                e.message,
                request=self.request,
                type='error')

    def nextURL(self):
        return 'application-listing/' + self.databag_name


class AddDatabagView(BrowserView):
    """
        View associated to wrap around the AddDatabagForm class
    """

    index = ViewPageTemplateFile('templates/add_form.pt')

    def __init__(self, context, request):
        super(AddDatabagView, self).__init__(context, request)
        self.form = AddDatabagForm(context, request)

    def __call__(self):
        self.form.update()
        return self.index()

    @property
    def available(self):
        chef_tool = queryUtility(IChefTool)
        if chef_tool is not None:
            return chef_tool.authenticated
        return False


class AddDatabagItemForm(form.AddForm):
    """
        Add form to create a new databag item of type IDatabagItem
    """

    fields = field.Fields(IDatabagItem)
    label = _(u'New item for databag ')

    parent = None

    def update(self):
        if self.parent is None:
            api.portal.show_message(
                _(u'Databag item must be added to a specific parent databag'),
                request=self.request,
                type='error')

        super(AddDatabagItemForm, self).update()

    def render(self):
        if self.parent is None:
            return ""
        return super(AddDatabagItemForm, self).render()

    def createAndAdd(self, data):
        chef_tool = queryUtility(IChefTool)
        self.item_name = data.get('name')
        try:
            return chef_tool.create_databag_item(self.parent, self.item_name)
        except ChefError as e:
            api.portal.show_message(
                e.message,
                request=self.request,
                type='error')

    def nextURL(self):
        return '%s/application-listing/%s/%s' % (
            self.context.absolute_url(),
            self.parent,
            self.item_name)

    def update_path(self, traverse_subpath):
        if len(traverse_subpath) == 1:
            self.parent = traverse_subpath[0]
            self.label += self.parent


@implementer(IPublishTraverse)
class AddDatabagItemView(BrowserView):
    """
        View to wrap the form for adding a new databag item. Implements
        IPublishTraverse in order to ensure the item is being added to a
        databag parent.
    """

    index = ViewPageTemplateFile('templates/add_form.pt')

    def __init__(self, context, request):
        super(AddDatabagItemView, self).__init__(context, request)
        self.traverse_subpath = []
        self.form = AddDatabagItemForm(context, request)

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        chef_tool = queryUtility(IChefTool)
        if chef_tool is not None:
            return chef_tool.authenticated
        return False

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    def update(self):
        if self.available:
            self.form.update_path(self.traverse_subpath)
            self.form.update()
