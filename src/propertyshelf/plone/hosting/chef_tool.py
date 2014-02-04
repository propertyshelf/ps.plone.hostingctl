# -*- coding: utf-8 -*-

# python imports
from chef import ChefAPI
from chef import Client

# zope imports
from persistent import Persistent
from zope.component import queryUtility
from zope.interface import implementer

# plone imports
from plone.registry.interfaces import IRegistry

# local imports
from .interfaces import IChefTool
from .browser.interfaces import IHostingSettings


@implementer(IChefTool)
class ChefTool(Persistent):
    """ Utility for interaction with Chef API """

    def __init__(self):
        self._authenticated = False
        self._initialized = False

    @property
    def authenticated(self):
        if not self._initialized:
            self.setup_from_registry()
        return self._authenticated

    def setup_from_registry(self):
        registry = queryUtility(IRegistry)
        if registry is not None:
            settings = registry.forInterface(IHostingSettings)
            self.setup(
                node_name=getattr(settings, 'node_name', u''),
                chef_server_url=getattr(settings, 'chef_server_url', u''),
                client_key=getattr(settings, 'client_key', u'')
            )
            self._initialized = True

    def setup(self, node_name, chef_server_url, client_key):
        try:
            chef_api = ChefAPI(
                url=chef_server_url,
                key=client_key,
                client=node_name)
            Client.list(api=chef_api)
        except:
            self._authenticated = False
        else:
            self._authenticated = True
            self._api = chef_api

    def clear_settings(self):
        self.node_url = None
        self.chef_server_url = None
        self.client_key = None
        self._authenticated = False
        self._api = None

