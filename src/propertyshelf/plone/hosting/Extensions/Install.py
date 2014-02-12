# -*- coding: utf-8 -*-
"""Install/Uninstall methods."""

# python imports
from logging import getLogger
from Products.CMFCore.utils import getToolByName

# local imports
from propertyshelf.plone.hosting import config


UNINSTALL_PROFILE = 'profile-propertyshelf.plone.hosting:uninstall'
logger = getLogger('propertyshelf.plone.hosting')


def runProfile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)


def delete_folders(site):
    """
        Deletes the databag container that was originally installed by
        this add-on product
    """

    if config.DATABAG_CONTAINER in site:
        site.manage_delObjects([config.DATABAG_CONTAINER])


def uninstall(portal, reinstall=False):
    """
        Uninstall the remaining bits that are leftover
        after this addon is removed
    """
    if reinstall:
        return

    site = portal.getSite()
    delete_folders(site)

    """Run the GS profile to uninstall this package"""
    runProfile(portal, UNINSTALL_PROFILE)

    logger.info('Ran all uninstall steps.')
