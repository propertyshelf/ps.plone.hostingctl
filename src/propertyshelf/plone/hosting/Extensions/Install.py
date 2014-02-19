# -*- coding: utf-8 -*-
"""Install/Uninstall methods."""

# python imports
from logging import getLogger
from Products.CMFCore.utils import getToolByName


UNINSTALL_PROFILE = 'profile-propertyshelf.plone.hosting:uninstall'
logger = getLogger('propertyshelf.plone.hosting')


def runProfile(portal, profileName):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profileName)


def uninstall(portal, reinstall=False):
    """
        Uninstall the remaining bits that are leftover
        after this addon is removed
    """
    if reinstall:
        return

    """Run the GS profile to uninstall this package"""
    runProfile(portal, UNINSTALL_PROFILE)

    logger.info('Ran all uninstall steps.')
