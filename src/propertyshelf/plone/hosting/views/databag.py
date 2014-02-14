# -*- coding: utf-8 -*-

""" Views for Databags in propertyshelf.plone.hosting """

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
from propertyshelf.plone.hosting.content.interfaces import IPloneDataBagItem


class DataBagViewForm(form.Form):
    """
        The form that is shown directly below the table view
    """

    @button.buttonAndHandler(_(u'Create Item'), name='create')
    def handle_create(self, action):
        data, errors = self.extractData()
        add_url = self.context.absolute_url() + '/add'
        self.request.response.redirect(add_url)


class DataBagView(BrowserView):
    """
        This view shows the data bag items contained in the given
        databag.
    """

    index = ViewPageTemplateFile('templates/databag.pt')
    label = _(u'Databag View')

    def __init__(self, context, request):
        super(DataBagView, self).__init__(context, request)
        self.form = DataBagViewForm(self.context, self.request)

    def __call__(self):
        self.update()
        self.form.update()
        return self.index()

    @property
    def available(self):
        return self.context.available

    def update(self):
        self.context.update()


class DataBagItemAddForm(form.AddForm):
    """
        Add form to create a new databag item in the container of IPloneDataBag
        @self.context is of type IPloneDataBag
        @self.fields are adapted from the schema of IPloneDataBagItem
    """

    fields = field.Fields(IPloneDataBagItem).omit('__parent__', '__name__')
    label = _(u'Add Databag Item')

    def __call__(self):
        super(DataBagItemAddForm, self).__call__()

    def createAndAdd(self, data):
        try:
            return self.context.add_databag_item(data['id'])
        except ChefError as e:
            api.portal.show_message(
                e.message,
                request=self.request,
                type='error')

    def nextURL(self):
        return 'index.html'


class DataBagItemAddFormView(layout.FormWrapper):
    form = DataBagItemAddForm
