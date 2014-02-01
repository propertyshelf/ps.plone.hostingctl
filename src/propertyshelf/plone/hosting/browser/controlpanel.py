# -*- coding: utf-8 -*-
"""Form field definitions for the registry configlet."""

# local imports
from propertyshelf.plone.hosting.browser.interfaces import IHostingSettings

# python imports
from chef import ChefAPI
from chef import Client
from logging import getLogger

# plone imports
from plone import api
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

# zope imports
from z3c.form import field

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

        try:
            chef_api = ChefAPI(
                url=chef_server_url,
                key=client_key,
                client=node_name)
            Client.list(api=chef_api)
        except:
            api.portal.show_message(
                "Chef API authentication: FAILURE",
                request=self.request)
        else:
            api.portal.show_message(
                "Chef API authentication: SUCCESS",
                request=self.request)

        return changes


class HostingSettingsView(ControlPanelFormWrapper):
    """ View wrapper for the Registry Edit Form """

    label = u"Hosting Settings"
    form = HostingSettingsEditForm
