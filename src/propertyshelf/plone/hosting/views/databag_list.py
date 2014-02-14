# -*- coding: utf-8 -*-

""" Views of the propertyshelf.plone.hosting add-on """

# python imports
from chef import ChefError

# zope imports
from z3c.form import button, form, field

# plone imports
from plone import api
from plone.z3cform import layout
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# local imports
from propertyshelf.plone.hosting.i18n import _
from propertyshelf.plone.hosting.content.interfaces import IPloneDataBag


class DataBagListViewForm(form.Form):
    """
        The form that is shown directly below the table view
    """

    @button.buttonAndHandler(_(u'Create'), name='create')
    def handle_create(self, action):
        data, errors = self.extractData()
        add_url = self.context.absolute_url() + '/add'
        self.request.response.redirect(add_url)


class DataBagListView(BrowserView):
    """
        This view shows the data bags available for the current
        authenticated session of the Chef API
    """

    index = ViewPageTemplateFile("templates/databag_list.pt")
    label = _(u'Databags')

    def __init__(self, context, request):
        super(DataBagListView, self).__init__(context, request)
        self.form = DataBagListViewForm(self.context, self.request)

    def __call__(self):
        self.update()
        self.form.update()
        return self.index()

    @property
    def available(self):
        return self.context.available

    def update(self):
        self.context.update()


class DataBagAddForm(form.AddForm):
    """
        Add form to create a new databag in the container of IPloneDataBagList
        @self.context is of type IPloneDataBagList
        @self.fields are adapted from the schema of IPloneDataBag
    """

    fields = field.Fields(IPloneDataBag).omit('__parent__', '__name__')
    label = _(u'Add Databag')

    def __call__(self):
        super(DataBagAddForm, self).__call__()

    def createAndAdd(self, data):
        try:
            return self.context.add_databag(data['name'])
        except ChefError as e:
            api.portal.show_message(
                e.message,
                request=self.request,
                type='error')

    def nextURL(self):
        return 'index.html'


class DataBagAddFormView(layout.FormWrapper):
    form = DataBagAddForm
