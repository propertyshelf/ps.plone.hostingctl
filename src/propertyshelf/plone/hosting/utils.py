# -*- coding: utf-8 -*-

""" Utility functions for propertyshelf.plone.hosting """


def to_display_domain(val):
    """
        Converts 'example_com__subdomain' into 'subdomain.example.com'
    """
    return '.'.join(reversed(val.split('__'))).replace('_', '.')
