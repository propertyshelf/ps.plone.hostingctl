# -*- coding: utf-8 -*-

# local imports
from propertyshelf.plone.hosting.testing import \
    PROPERTYSHELF_PLONE_HOSTING_INTEGRATION
from propertyshelf.plone.hosting.browser.interfaces import IHostingSettings

# python imports
import unittest2 as unittest

# plone imports
from plone import api
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

# zope imports
from AccessControl import Unauthorized
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent


class TestExample(unittest.TestCase):
    """ Tests the control panel settings form """

    layer = PROPERTYSHELF_PLONE_HOSTING_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.context = self.portal
        self.request = self.layer['request']

        # setup manually the correct browserlayer, see:
        # https://dev.plone.org/ticket/11673
        notify(BeforeTraverseEvent(self.portal, self.request))

    def test_view_available(self):
        """
            Verifies that the settings view is available and the
            form provides the IHostingSettings interface
        """
        view = api.content.get_view(
            name='hosting-settings',
            context=self.context,
            request=self.request
        )
        self.assertIsNotNone(view)
        self.assertEqual(view.form.schema, IHostingSettings)

    def test_controlpanel_view_protected(self):
        """Test that the configuration view needs authentication."""
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.restrictedTraverse('@@hosting-settings')

        logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                          '@@hosting-settings')

