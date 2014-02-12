# -*- coding: utf-8 -*-

""" Content type for databag items in propertyshelf.plone.hosting """

# plone imports
from OFS.SimpleItem import SimpleItem

# zope imports
from zope.interface import implementer

# local imports
from .interfaces import IPloneDataBagItem


@implementer(IPloneDataBagItem)
class PloneDataBagItem(SimpleItem):

    def __init__(self, name):
        super(PloneDataBagItem, self).__init__()
        self.name = name
        self.id = str(name)
