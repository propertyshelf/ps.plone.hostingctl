# -*- coding: utf-8 -*-

# python imports
from chef import ChefAPI, Client, DataBag, DataBagItem

# zope imports
from persistent import Persistent
from zope.component import queryUtility
from zope.interface import implementer

# plone imports
from plone.registry.interfaces import IRegistry

# local imports
from .interfaces import IChefTool
from .views.interfaces import IHostingSettings


@implementer(IChefTool)
class ChefTool(object):
    """ Utility for interaction with Chef API """

    def __init__(self):
        self._initialized = False
        self.clear_settings()

    @property
    def authenticated(self):
        if not self._initialized:
            self.setup_from_registry()
        return self._authenticated

    def setup_from_registry(self):
        registry = queryUtility(IRegistry)
        if registry is None:
            return

        settings = registry.forInterface(IHostingSettings)
        if settings is None:
            return

        self.setup(
            node_name=getattr(settings, 'node_name', u''),
            chef_server_url=getattr(settings, 'chef_server_url', u''),
            client_key=getattr(settings, 'client_key', u'')
        )
        self._initialized = True

    def setup(self, node_name, chef_server_url, client_key):
        self.clear_settings()

        # must at least check for black client_key because PyChef crashes
        # without exception on a blank client_key
        if not node_name or not chef_server_url or not client_key:
            return

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
        self._authenticated = False
        self._api = None

    def get_databags(self):
        if not self.authenticated:
            return []

        return list(DataBag.list(api=self._api))

    def get_databag_items(self, name):
        if not self.authenticated:
            return []

        bag = DataBag(name, api=self._api)

        if not bag.exists:
            return None

        return bag.keys()

    def get_data_from_item(self, bag_name, item_name):
        if not self.authenticated:
            return {}

        item = DataBagItem(bag_name, item_name, api=self._api)
        if not item.raw_data:
            return None

        return item.raw_data

    def create_databag(self, bag_name):
        if not self.authenticated:
            return

        return DataBag.create(bag_name, api=self._api)

    def create_databag_item(self, bag_name, item_id):
        if not self.authenticated:
            return

        return DataBagItem.create(bag_name, item_id, api=self._api)
