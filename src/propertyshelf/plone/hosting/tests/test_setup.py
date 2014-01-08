import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from propertyshelf.plone.hosting.testing import\
    PROPERTYSHELF_PLONE_HOSTING_INTEGRATION


class TestExample(unittest.TestCase):

    layer = PROPERTYSHELF_PLONE_HOSTING_INTEGRATION
    
    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
    
    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'propertyshelf.plone.hosting'
        installed = [p['id'] for p in self.qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_product_is_uninstalled(self):
        """ Validate that the product has been successfully uninstalled """
        self.qi_tool.uninstallProducts(['propertyshelf.plone.hosting'])
        self.assertFalse(self.qi_tool.isProductInstalled(
            'propertyshelf.plone.hosting'))
