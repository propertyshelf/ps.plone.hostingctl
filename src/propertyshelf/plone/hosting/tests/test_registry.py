# -*- coding: utf-8 -*-

# local imports
from propertyshelf.plone.hosting.testing import \
    PROPERTYSHELF_PLONE_HOSTING_INTEGRATION
from propertyshelf.plone.hosting.browser.interfaces import IHostingSettings

# python imports
import unittest2 as unittest

# plone imports
from plone.registry.interfaces import IRegistry

# zope imports
from zope.component import getUtility


class TestExample(unittest.TestCase):
    """ Tests for checking the registry """

    layer = PROPERTYSHELF_PLONE_HOSTING_INTEGRATION

    def test_node_name(self):
        # test default initial value
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IHostingSettings)
        self.assertTrue(hasattr(settings, 'node_name'))
        self.assertEqual(settings.node_name, u'')

        # test a dummy setting
        setattr(settings, 'node_name', u'foo')
        self.assertEqual(getattr(settings, 'node_name'), u'foo')

    def test_chef_server_url(self):
        # test default initial value
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IHostingSettings)
        self.assertTrue(hasattr(settings, 'chef_server_url'))
        self.assertEqual(settings.chef_server_url, u'')

        # test a dummy value
        setattr(settings, 'chef_server_url', u'foo_url')
        self.assertEqual(getattr(settings, 'chef_server_url'), u'foo_url')

    def test_client_key(self):
        # test default initial value
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IHostingSettings)
        self.assertTrue(hasattr(settings, 'client_key'))
        self.assertEqual(settings.client_key, u'')

        # test dummy value
        setattr(settings, 'client_key', u'foo_key\n line 2')
        self.assertEqual(getattr(settings, 'client_key'), u'foo_key\n line 2')

