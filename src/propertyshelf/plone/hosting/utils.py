# -*- coding: utf-8 -*-

""" Utility functions for propertyshelf.plone.hosting """


def to_display_domain(val):
    """
        Converts 'example_com__subdomain' into 'subdomain.example.com'
    """
    return '.'.join(reversed(val.split('__'))).replace('_', '.')


def prepare_data(data):
    """
        Takes a dictionary with required entry 'domain' and optional entry
        'subdomain' and transforms the result to have the correct 'domain' and
        'id' entries
    """
    domain = data.get('domain')
    full_domain = domain
    item_id = domain.replace('.', '_')
    subdomain = data.get('subdomain')
    if subdomain:
        item_id = '{0}__{1}'.format(item_id, subdomain)
        full_domain = '{0}.{1}'.format(subdomain, full_domain)
        del data['subdomain']

    data['domain'] = full_domain
    data['id'] = item_id

    return data
