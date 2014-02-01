# -*- coding: utf-8 -*-

"""Setup of test layers for propertyshelf.plone.hosting"""

# plone imports
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE


class PropertyshelfPloneHostingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import propertyshelf.plone.hosting
        self.loadZCML(package=propertyshelf.plone.hosting)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'propertyshelf.plone.hosting:default')


PROPERTYSHELF_PLONE_HOSTING = PropertyshelfPloneHostingLayer()
PROPERTYSHELF_PLONE_HOSTING_INTEGRATION = IntegrationTesting(
    bases=(PROPERTYSHELF_PLONE_HOSTING, ),
    name="PROPERTYSHELF_PLONE_HOSTING_INTEGRATION")
