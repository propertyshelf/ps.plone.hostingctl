# -*- coding: utf-8 -*-
"""Form field definitions for the registry configlet."""

# python imports
from logging import getLogger

# plone imports
from plone import api
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

# zope imports
from z3c.form import field
from zope.component import queryUtility

#local imports
from propertyshelf.plone.hosting.i18n import _
from propertyshelf.plone.hosting.interfaces import IChefTool
from propertyshelf.plone.hosting.views.interfaces import IHostingSettings

logger = getLogger('propertyshelf.plone.hosting')


class HostingSettingsEditForm(RegistryEditForm):
    """
        Class that defines the behavior of the registry edit form for the
        configuration settings
    """

    fields = field.Fields(IHostingSettings)
    schema = IHostingSettings

    def __init__(self, context, request):
        super(HostingSettingsEditForm, self).__init__(context, request)

    def updateWidgets(self):
        super(HostingSettingsEditForm, self).updateWidgets()
        self.widgets['client_key'].rows = 15

    def applyChanges(self, data):
        changes = super(HostingSettingsEditForm, self).applyChanges(data)

        if not 'node_name' in data or \
           not 'chef_server_url' in data or \
           not 'client_key' in data:

            logger.warning(
                "Unable to extract data from Hosting Settings form: \
                unexpected field names")
            return changes

        node_name = data.get('node_name')
        chef_server_url = data.get('chef_server_url')
        client_key = data.get('client_key')
        prefix = data.get('prefix_filter')

        chef_tool = queryUtility(IChefTool)
        if chef_tool is not None:
            chef_tool.setup(node_name, chef_server_url, client_key, prefix)
            if chef_tool.authenticated:
                api.portal.show_message(
                    _(u'Chef API authentication: SUCCESS'),
                    request=self.request)
            else:
                api.portal.show_message(
                    _(u'Chef API authentication: FAILURE'),
                    request=self.request)
        else:
            logger.warning("Chef utility is not correctly registered")

        return changes


class HostingSettingsView(ControlPanelFormWrapper):
    """ View wrapper for the Registry Edit Form """

    label = _(u'Hosting Settings')
    form = HostingSettingsEditForm
