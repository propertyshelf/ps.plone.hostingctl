# -*- coding: utf-8 -*-

""" Setup handlers for installation of propertyshelf.plone.hosting """

# local imports
from propertyshelf.plone.hosting import config
from propertyshelf.plone.hosting.content.databag_list import PloneDataBagList


def setup_various(context):
    """
        @param context: Products.GenericSetup.context.DirectoryImportContext
                        instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('propertyshelf.plone.hosting.marker.txt') is None:
        return

    site = context.getSite()
    setup_folders(site)


def setup_folders(site):
    """
        Creates the PloneDataBagList folder that will act as the
        content container
    """

    # if it already exists, delete      TODO: find a better solution
    if config.DATABAG_CONTAINER in site:
        site.manage_delObjects([config.DATABAG_CONTAINER])

    databag_list = PloneDataBagList(config.DATABAG_CONTAINER)
    site[config.DATABAG_CONTAINER] = databag_list
