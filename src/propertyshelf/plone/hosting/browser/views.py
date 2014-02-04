# -*- coding: utf-8 -*-

""" Views of the propertyshelf.plone.hosting add-on """

# zope imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from zope.component import queryUtility

# local imports
from propertyshelf.plone.hosting.interfaces import IChefTool


class DataBagView(BrowserView):
    """
        This view shows the data bags available for the current
        authenticated session of the Chef API
    """

    index = ViewPageTemplateFile("templates/databag.pt")

    def __init__(self, context, request):
        super(DataBagView, self).__init__(context, request)

        self._available = False
        chef_api = queryUtility(IChefTool)
        if chef_api is not None:
            self._available = chef_api.authenticated

    def __call__(self):
        return self.index()

    @property
    def available(self):
        return self._available
