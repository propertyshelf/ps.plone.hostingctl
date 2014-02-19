# -*- coding: utf-8 -*-

""" Interface definitions for propertyshelf.plone.hosting """

# zope imports
from zope.interface import Interface


class IChefTool(Interface):
    """ Interface definition for the Chef API utility """

    def authenticated():
        """
            Returns whether the API has been successfully authenticated or not
        """

    def clear_settings():
        """ Clears the current settings for API authentication """

    def setup_from_registry():
        """ Sets up the API from the settings in the registry """

    def setup(node_name, chef_server_url, client_key):
        """ Sets up the API for authentication """

    def get_databags():
        """ Return a list of all databags of this authenticated instance """

    def get_databag_items(name):
        """ Return a list of all databag items for the given databag name """

    def get_data_from_item(bag, item):
        """
            Return the dictionary of attribute-value pairs for the given
            databag item
        """

    def create_databag(bag_name):
        """
            Creates a DataBag on the Chef server with the given name. Throws
            a ChefServerError if the DataBag with that name already exists.
        """

    def create_databag_item(bag_name, item_id):
        """
            Creates a DataBagItem on the Chef server with the given id in the
            given databag. Throws a ChefServerError if the DataBag with that
            name already exists.
        """
