# -*- coding: utf-8 -*-

""" Views for Databag Items in propertyshelf.plone.hosting """

# plone imports
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# local imports
from propertyshelf.plone.hosting.i18n import _


class DataBagItemView(BrowserView):
    """
        This view lists the data for a given databag item
    """

    index = ViewPageTemplateFile('templates/databag_item.pt')
    label = _(u'Databag Item')

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        return self.context.available

    def update(self):
        self.context.update()
