# -*- coding: utf-8 -*-

"""
Integration tests for the control panel view of propertyshelf.plone.hosting
"""

# python imports
import unittest2 as unittest

# plone imports
from plone.app.testing import logout
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

# zope imports
from AccessControl import Unauthorized
from zope.component import getMultiAdapter
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent

# local imports
from propertyshelf.plone.hosting.testing import \
    PROPERTYSHELF_PLONE_HOSTING_INTEGRATION
from propertyshelf.plone.hosting.browser.interfaces import IHostingSettings


class TestControlPanel(unittest.TestCase):
    """ Tests the control panel settings form """

    layer = PROPERTYSHELF_PLONE_HOSTING_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.context = self.portal
        self.request = self.layer['request']

        # setup manually the correct browserlayer, see:
        # https://dev.plone.org/ticket/11673
        notify(BeforeTraverseEvent(self.portal, self.request))

    def test_view(self):
        """
            Verifies that the settings view is available and the
            form provides the IHostingSettings interface
        """
        view = getMultiAdapter(
            (self.context, self.request),
            name=u'hosting-settings')
        self.assertIsNotNone(view)
        self.assertEqual(view.form.schema, IHostingSettings)

    def test_controlpanel_view_permissions(self):
        """Test that the configuration view needs authentication."""
        # logged in as TEST_USER with "Member" role
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse, '@@hosting-settings')

        # simulate "Manager" user
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        view = self.portal.restrictedTraverse('@@hosting-settings')
        self.assertEqual(view.label, u"Hosting Settings")

        # anonymous user
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse, '@@hosting-settings')

