# -*- coding: utf-8 -*-

""" Interface definitions for ps.plone.hostingctl """

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
        """
            Return a dictionary of (key: display_name) values for all databag
            items for the given databag name
        """

    def get_data_from_item(bag, item):
        """
            Return the data of a databag item transformed into a list of tuples
            in the form of (attribute, value) pairs
        """

    def get_dict_from_item(bag_name, item_name):
        """
            Return the data of a databag item as the raw data of type
            dictionary
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

    def edit_databag_item(bag_name, old_id, data):
        """
            Edits an existing databag item with the data passed in as a
            dictionary. The databag item is defined by its parent bag_name and
            the id found in the dictionary data['id']. The old_id parameter is
            used to determine if the name (and therefore the id) of the databag
            item was changed in the edits. If so, a new databag is created with
            the new id, and the old one is deleted from the server
        """

    def remove(bag_name, item_name):
        """
            Removes the Chef object from the server. If both item_name and
            bag_name are provided, this method removes the corresponding
            DataBagItem. If only the bag_name is provided, the method removes
            the corresponding DataBag.
        """
