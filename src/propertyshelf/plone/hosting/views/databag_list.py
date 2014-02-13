# -*- coding: utf-8 -*-

""" Views of the propertyshelf.plone.hosting add-on """

# zope imports
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# local imports
from propertyshelf.plone.hosting.i18n import _


class DataBagListView(BrowserView):
    """
        This view shows the data bags available for the current
        authenticated session of the Chef API
    """

    index = ViewPageTemplateFile("templates/databag_list.pt")
    label = _(u'Databags')

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        return self.context.available
        
    def update(self):
        self.context.update()

