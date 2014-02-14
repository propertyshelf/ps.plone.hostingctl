# -*- coding: utf-8 -*-

""" Content type for databag items in propertyshelf.plone.hosting """

# plone imports
from OFS.SimpleItem import SimpleItem

# zope imports
from zope.component import queryUtility
from zope.interface import implementer

# local imports
from .interfaces import IPloneDataBagItem
from propertyshelf.plone.hosting.interfaces import IChefTool


@implementer(IPloneDataBagItem)
class PloneDataBagItem(SimpleItem):

    __name__ = __parent__ = None
    
    def __init__(self, bag, name):
        super(PloneDataBagItem, self).__init__()
        self.parent = bag
        self.name = name
        self.id = str(name)
        self._data = {}
        self._exists = True

    @property
    def available(self):
        return self._available

    @property
    def exists(self):
        return self._exists

    def get_data(self):
        return self._data

    def update(self):
        self._available = False
        chef_tool = queryUtility(IChefTool)
        if chef_tool is None:
            return

        self._available = chef_tool.authenticated
        self._exists = True

        self._data = chef_tool.get_data(self.parent, self.name)
        if not self._data:
            self._exists = False
