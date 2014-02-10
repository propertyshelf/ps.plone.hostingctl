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

    def setup(node_name, chef_server_url, client_key):
        """ Sets up the API for authentication """
