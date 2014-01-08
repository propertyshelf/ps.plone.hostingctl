# -*- coding: utf-8 -*-
"""Interface definitions."""

from plone.directives import form
from plone.theme.interfaces import IDefaultPloneLayer

from zope import schema


class IHostingSpecific(IDefaultPloneLayer):
    """ Marker interface that defines the browser layer """


class IHostingSettings(form.Schema):
    """ Schema interface for the registry settings of the configlet """

    node_name = schema.TextLine(title=u"Node name", default=u'', required=True)

    chef_server_url = schema.TextLine(
        title=u"Server URL",
        default=u'',
        required=True)
    
    client_key = schema.Text(title=u"Client key", default=u'', required=True)
