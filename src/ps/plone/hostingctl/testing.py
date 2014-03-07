# -*- coding: utf-8 -*-

"""Setup of test layers for ps.plone.hostingctl"""

# plone imports
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE


class PSPloneHostingCtlLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import ps.plone.hostingctl
        self.loadZCML(package=ps.plone.hostingctl)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ps.plone.hostingctl:default')


PS_PLONE_HOSTINGCTL = PSPloneHostingCtlLayer()
PS_PLONE_HOSTINGCTL_INTEGRATION = IntegrationTesting(
    bases=(PS_PLONE_HOSTINGCTL, ),
    name="PS_PLONE_HOSTINGCTL_INTEGRATION")
