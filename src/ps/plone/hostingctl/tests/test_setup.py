# -*- coding: utf-8 -*-

"""
Integration tests for the registry of ps.plone.hostingctl
"""

# python imports
import unittest2 as unittest

# plone imports
from Products.CMFCore.utils import getToolByName

# local imports
from ps.plone.hostingctl.testing import\
    PS_PLONE_HOSTINGCTL_INTEGRATION


class TestSetup(unittest.TestCase):

    layer = PS_PLONE_HOSTINGCTL_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'ps.plone.hostingctl'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_product_is_uninstalled(self):
        """ Validate that the product has been successfully uninstalled """
        self.qi_tool.uninstallProducts(['ps.plone.hostingctl'])
        self.assertFalse(self.qi_tool.isProductInstalled(
            'ps.plone.hostingctl'))
