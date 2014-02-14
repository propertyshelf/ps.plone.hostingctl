# -*- coding: utf-8 -*-

""" Interfaces definging the content type in propertyshelf.plone.hosting """

# zope imports
from zope.container.constraints import containers, contains
from zope.container.interfaces import IContainer
from zope.location.interfaces import IContained
from zope import schema

# local imports
from propertyshelf.plone.hosting.i18n import _


class IPloneDataBagList(IContainer, IContained):
    """
        Container for a list of databags
    """
    contains('.IPloneDataBag')

    def update():
        """
            Updates the databags within this container using the PyChef API
        """

    def get_databags():
        """
            Returns a list of databags within the container
        """

    def add_databag(name):
        """
            Adds a new databag to the Chef server that will be later added to
            this container on self.update()
        """


class IPloneDataBag(IContainer, IContained):
    """
        This content type is essentially a wrapper for the PyChef
        DataBag object. Contains various databag items.
    """
    containers('.IPloneDataBagList')
    contains('.IPloneDataBagItem')

    name = schema.TextLine(
        title=_(u'Name'),
        required=True,
        default=u''
    )

    def update():
        """
            Updates the databag items within this databag using the PyChef API
        """

    def get_databag_items():
        """
            Returns a list of databag items within this specific databag
        """

    def add_databag_item(self, item_id):
        """
            Adds a new databag item with the given id that will be shown in
            this container on the next self.update()
        """


class IPloneDataBagItem(IContained):
    """
        Databag item which is associated with and contained within
        a specific databag. The data contained within a databag item
        is a dictionary of key-value pairs.
    """
    containers('.IPloneDataBag')

    id = schema.TextLine(
        title=_(u'ID'),
        required=True,
        default=u''
    )

    def update():
        """
            Updates the data within this databag item using the PyChef API
        """

    def get_data():
        """
            Returns a dictionary of key-value pairs from this databag item
        """
