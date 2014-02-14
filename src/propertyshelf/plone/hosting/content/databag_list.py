# -*- coding: utf-8 -*-

""" Content type for Databags in propertyshelf.plone.hosting """

# plone imports
from OFS.Folder import Folder

# zope imports
from zope.component import queryUtility
from zope.container.contained import Contained
from zope.interface import implementer

# local imports
from .databag import PloneDataBag
from .interfaces import IPloneDataBagList
from propertyshelf.plone.hosting.interfaces import IChefTool


@implementer(IPloneDataBagList)
class PloneDataBagList(Folder, Contained):

    def __init__(self, name):
        super(PloneDataBagList, self).__init__()
        self.name = name
        self.id = str(name)

    @property
    def available(self):
        return self._available

    def get_databags(self):
        return sorted(self.values(), key=lambda x: x.name)

    def update(self):
        self._available = False
        chef_tool = queryUtility(IChefTool)
        if chef_tool is None:
            return

        self._available = chef_tool.authenticated

        self.manage_delObjects(self.objectIds())
        for name in chef_tool.get_databags():
            databag = PloneDataBag(name)        # TODO: make factory
            self[databag.getId()] = databag

    def add_databag(self, name):
        chef_tool = queryUtility(IChefTool)
        if chef_tool is None:
            return

        return chef_tool.create_databag(name)
