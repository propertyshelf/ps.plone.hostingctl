# -*- coding: utf-8 -*-
"""Interface definitions."""

# zope imports
from zope import schema

# plone imports
from plone.directives import form
from plone.theme.interfaces import IDefaultPloneLayer

# local imports
from propertyshelf.plone.hosting.i18n import _


class IHostingSpecific(IDefaultPloneLayer):
    """ Marker interface that defines the browser layer """


class IHostingSettings(form.Schema):
    """ Schema interface for the registry settings of the configlet """

    node_name = schema.TextLine(
        title=_(u'Node name'),
        default=u'',
        required=True
    )

    chef_server_url = schema.TextLine(
        title=_(u'Server URL'),
        default=u'',
        required=True
    )

    client_key = schema.Text(
        title=_(u'Client key'),
        default=u'',
        required=True
    )

    prefix_filter = schema.TextLine(
        title=_(u'Filter prefix'),
        required=False,
        default=u'',
        description=_(
            u'Used to match and filter the types of applications shown.'
        )
    )


class IDatabag(form.Schema):
    """
        Schema interface for the basic databag type
    """

    name = schema.TextLine(
        title=_(u'Name'),
        required=True
    )


class IDatabagItem(form.Schema):
    """
        Schema interface for the basic databag type
    """

    name = schema.TextLine(
        title=_(u'Name'),
        required=True
    )
