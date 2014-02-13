# -*- coding: utf-8 -*-

""" Content type for Databags in propertyshelf.plone.hosting """

# plone imports
from OFS.Folder import Folder

# zope imports
from zope.component import queryUtility
from zope.interface import implementer

# local imports
from .databag_item import PloneDataBagItem
from .interfaces import IPloneDataBag
from propertyshelf.plone.hosting.interfaces import IChefTool


@implementer(IPloneDataBag)
class PloneDataBag(Folder):

    def __init__(self, name):
        super(PloneDataBag, self).__init__()
        self.name = name
        self.id = str(name)

    @property
    def available(self):
        return self._available

    def get_databag_items(self):
        return sorted(self.values(), key=lambda x: x.name)

    def update(self):
        self._available = False
        chef_tool = queryUtility(IChefTool)
        if chef_tool is None:
            return

        self._available = chef_tool.authenticated

        self.manage_delObjects(self.objectIds())
        for item_name in chef_tool.get_databag_items(self.name):
            item = PloneDataBagItem(self.name, item_name)        # TODO: make factory
            self[item.getId()] = item

