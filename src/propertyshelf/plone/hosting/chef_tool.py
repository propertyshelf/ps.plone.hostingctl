# -*- coding: utf-8 -*-

# python imports
from chef import ChefAPI, Client, DataBag, DataBagItem

# zope imports
from zope.component import queryUtility
from zope.interface import implementer

# plone imports
from plone.registry.interfaces import IRegistry

# local imports
from .interfaces import IChefTool
from .views.interfaces import IHostingSettings


def to_display_domain(val):
    """
        Converts 'example_com__subdomain' into 'subdomain.example.com'
    """
    return '.'.join(reversed(val.split('__'))).replace('_', '.')


class PrefixFilter(object):
    """
        This adapter works with strings or lists of strings. With a given
        prefix, all strings are filtered to only display those which begin with
        the prefix. As well, strings are displayed without the prefix filter.
        In order to revert back to the original string, the action can be
        reversed with the revert funciton.
    """

    def __init__(self, prefix):
        if prefix is None:
            prefix = u''
        self._prefix = prefix
        self._len = len(prefix)

    def filter(self, arg):
        """
            Takes a string or a list of strings as the argument and returns the
            filtered list
        """

        if isinstance(arg, basestring):
            yield self._filter(arg)
        else:
            for val in arg:
                ret_val = self._filter(val)
                if ret_val:
                    yield ret_val

    def _filter(self, val):
        """
            The inner filter function that only accepts a single string
        """
        if val.startswith(self._prefix):
            return val[self._len:]

    def revert(self, val):
        """
            Reverts a name that has already been transformed with the filter.
            Also used for creation of new names within the system.
        """
        return self._prefix + val


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
            client_key=getattr(settings, 'client_key', u''),
            prefix=getattr(settings, 'prefix_filter', u'')
        )
        self._initialized = True

    def setup(self, node_name, chef_server_url, client_key, prefix=u''):
        self.clear_settings()

        # must at least check for black client_key because PyChef crashes
        # without exception on a blank client_key
        if not node_name or not chef_server_url or not client_key:
            return

        try:
            chef_api = ChefAPI(
                url=chef_server_url,
                key=client_key,
                client=node_name
            )
            Client.list(api=chef_api)
        except:
            self._authenticated = False
            return

        self._authenticated = True
        self._api = chef_api
        self._bag_adapter = PrefixFilter(prefix)

    def clear_settings(self):
        self._authenticated = False
        self._api = None

    def get_databags(self):
        if not self.authenticated:
            return []

        vals = self._bag_adapter.filter(list(DataBag.list(api=self._api)))
        return sorted(vals)

    def get_databag_items(self, bag_name):
        if not self.authenticated:
            return []

        bag_name = self._bag_adapter.revert(bag_name)
        bag = DataBag(bag_name, api=self._api)

        if not bag.exists:
            return None

        return dict((key, to_display_domain(key)) for key in sorted(bag.keys()))

    def get_data_from_item(self, bag_name, item_name):
        if not self.authenticated:
            return {}

        bag_name = self._bag_adapter.revert(bag_name)
        item = DataBagItem(bag_name, item_name, api=self._api)
        if not item.raw_data:
            return None

        return item.raw_data

    def create_databag(self, bag_name):
        if not self.authenticated:
            return

        bag_name = self._bag_adapter.revert(bag_name)
        return DataBag.create(bag_name, api=self._api)

    def create_databag_item(self, bag_name, item_id, data={}):
        if not self.authenticated:
            return

        bag_name = self._bag_adapter.revert(bag_name)
        return DataBagItem.create(bag_name, item_id, api=self._api, **data)

    def remove(self, bag_name, item_name=None):
        if not self.authenticated:
            return

        bag_name = self._bag_adapter.revert(bag_name)
        if item_name:
            obj = DataBagItem(bag_name, item_name, api=self._api)
        else:
            obj = DataBag(bag_name, api=self._api)

        if obj.exists:
            obj.delete(api=self._api)
