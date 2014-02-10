# -*- coding: utf-8 -*-

""" Views of the propertyshelf.plone.hosting add-on """

# zope imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility

# plone imports
from plone.app.layout.viewlets.common import ViewletBase

# local imports
from propertyshelf.plone.hosting.i18n import _
from propertyshelf.plone.hosting.interfaces import IChefTool


class DataBagViewlet(ViewletBase):
    """
        This view shows the data bags available for the current
        authenticated session of the Chef API
    """

    index = ViewPageTemplateFile("templates/databag.pt")
    label = _(u'Available Data Bag')

    def update(self):
        self._available = False
        chef_tool = queryUtility(IChefTool)
        if chef_tool is None:
            return

        self._available = chef_tool.authenticated
        self._databags = chef_tool.get_databags()

    @property
    def available(self):
        return self._available

    def get_databag_names(self):
        return self._databags

    def get_num_databags(self):
        return len(self._databags)
