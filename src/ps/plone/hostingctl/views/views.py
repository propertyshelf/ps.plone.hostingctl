# -*- coding: utf-8 -*-


# zope imports
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

# local imports
from .forms import (
    MainViewForm,
    AddDomainItemForm,
    EditDomainItemForm
)
from ps.plone.hostingctl.utils import to_display_domain
from ps.plone.hostingctl.interfaces import IChefTool


@implementer(IPublishTraverse)
class DatabagView(BrowserView):
    """
        The main view for showing the listings of databags or the listing
        of databag items. The context is determined by the traversal subpath,
        parsing it to determine whether the view will be for a specific
        databag, databag item, etc.
    """

    index = ViewPageTemplateFile("templates/databags.pt")
    _label = u''

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.form = MainViewForm(context, request)
        self.traverse_subpath = []
        self.tool = queryUtility(IChefTool)

    def __call__(self):
        self.form.update_path(self.traverse_subpath)
        self.form.update()
        return self.index()

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    @property
    def available(self):
        if self.tool is not None:
            return self.tool.authenticated

    @property
    def label(self):
        return self._label

    def list_databags(self):
        if len(self.traverse_subpath) == 0:
            return self.tool.get_databags()

    def databag_items(self):
        if len(self.traverse_subpath) == 1:
            databag = self.traverse_subpath[0]
            self._label = databag
            return self.tool.get_databag_items(databag)

    def databag_item_details(self):
        if len(self.traverse_subpath) == 2:
            databag = self.traverse_subpath[0]
            item = self.traverse_subpath[1]
            self._label = to_display_domain(item)
            return self.tool.get_data_from_item(databag, item)

    def get_databag_name(self):
        if len(self.traverse_subpath) > 0:
            return self.traverse_subpath[0]
        return ''


class FormWrapperView(BrowserView):
    """
        View for ps.plone.hostingctl to wrap around a form. The
        attribute form_class must be defined as the class of the form to be
        created.
    """

    index = ViewPageTemplateFile('templates/form_wrapper.pt')
    form_class = None

    def __init__(self, context, request):
        super(FormWrapperView, self).__init__(context, request)
        if not self.form_class:
            raise NotImplementedError
            return
        self.form = self.form_class(context, request)

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        chef_tool = queryUtility(IChefTool)
        if chef_tool is not None:
            return chef_tool.authenticated
        return False

    def update(self):
        if self.available:
            self.form.update()


@implementer(IPublishTraverse)
class FormWrapperSubpathView(FormWrapperView):
    """
        View to wrap a form that requires a traversal subpath. Implements
        IPublishTraverse and passes the subpath to the form object on update.
        The attribute form_class must be defined as the class of the form to be
        created. The form must have a method implemented called update_path to
        pass it the traverse_subpath.
    """

    def __init__(self, context, request):
        super(FormWrapperSubpathView, self).__init__(context, request)
        self.traverse_subpath = []

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    def update(self):
        if self.available:
            self.form.update_path(self.traverse_subpath)
            self.form.update()


class AddDomainItemView(FormWrapperSubpathView):
    """ View for the 'domain' specific databag item form """
    form_class = AddDomainItemForm


class EditDomainItemView(FormWrapperSubpathView):
    """ Edit view for the 'domain' specific databag item form """
    form_class = EditDomainItemForm


class DeleteDatabagView(BrowserView):
    """
        Basic view that displays nothing but will delete the databag that
        is passed to it through the query string
    """

    def __call__(self):
        bag_name = self.request.form.get('bag_name')
        item_name = self.request.form.get('item_name')
        self.remove_databag(bag_name, item_name)

        next_url = 'applications'
        if item_name:
            next_url += '/' + bag_name
        self.request.response.redirect(next_url)
        return ""

    def remove_databag(self, bag_name, item_name=None):
        chef_tool = queryUtility(IChefTool)
        if chef_tool:
            chef_tool.remove(bag_name, item_name)
