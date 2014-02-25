# -*- coding: utf-8 -*-

""" Form definitions for the views of propertyshelf.plone.hosting """

# python imports
from chef import ChefError

# zope imports
from z3c.form import button, field, form
from zope.component import queryUtility

# plone imports
from plone import api

# local imports
from .interfaces import IDatabag, IDatabagItem, IDomainDatabagItem
from propertyshelf.plone.hosting.i18n import _
from propertyshelf.plone.hosting.interfaces import IChefTool


class MainViewForm(form.Form):
    """
        The form that is shown directly below the table view
    """

    traverse_subpath = []

    def update_path(self, traverse_subpath):
        self.traverse_subpath = traverse_subpath

    @button.buttonAndHandler(_(u'Create'), name='create')
    def handle_create(self, action):
        data, errors = self.extractData()
        add_url = ""
        if len(self.traverse_subpath) == 0:
            add_url = self.context.absolute_url() + '/create-databag'
        elif len(self.traverse_subpath) == 1:
            add_url = '%s/create-domain/%s' % (
                self.context.absolute_url(),
                self.traverse_subpath[0])
        self.request.response.redirect(add_url)


class AddDatabagForm(form.AddForm):
    """
        Add form to create a new databag of type IDatabag
    """

    fields = field.Fields(IDatabag)
    label = _(u'Add Databag')
    
    @property
    def valid(self):
        return True

    def update(self):
        super(AddDatabagForm, self).update()
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())

    def createAndAdd(self, data):
        chef_tool = queryUtility(IChefTool)
        self.databag_name = data.get('name')
        try:
            return chef_tool.create_databag(self.databag_name)
        except ChefError as e:
            api.portal.show_message(
                e.message,
                request=self.request,
                type='error')

    def nextURL(self):
        return 'applications/' + self.databag_name


class AddDatabagItemForm(form.AddForm):
    """
        Add form to create a new databag item of type IDatabagItem
    """

    fields = field.Fields(IDatabagItem)
    label = _(u'New item for databag ')

    parent = None
    _valid = True

    @property
    def valid(self):
        return self._valid

    def update(self):
        super(AddDatabagItemForm, self).update()
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())

        if self.parent is None:
            self._valid = False
            api.portal.show_message(
                _(u'Databag item must be added to a specific parent databag'),
                request=self.request,
                type='error')

    def createAndAdd(self, data):
        chef_tool = queryUtility(IChefTool)
        self.item_name = data.get('name')
        try:
            return chef_tool.create_databag_item(self.parent, self.item_name)
        except ChefError as e:
            api.portal.show_message(
                e.message,
                request=self.request,
                type='error')

    def nextURL(self):
        return '%s/applications/%s/%s' % (
            self.context.absolute_url(),
            self.parent,
            self.item_name)

    def update_path(self, traverse_subpath):
        if len(traverse_subpath) == 1:
            self.parent = traverse_subpath[0]
            self.label += self.parent


class AddDomainItemForm(AddDatabagItemForm):
    """
        Form definition for creating a 'domain' type databag item using the
        schema from IDomainDatabagItem
    """

    fields = field.Fields(IDomainDatabagItem)

    def createAndAdd(self, data):
        chef_tool = queryUtility(IChefTool)
        domain = data.get('domain')
        if not domain:
            return
        subdomain = data.get('subdomain')
        redirect = data.get('redirect')
        caching = data.get('caching')
        data = {}
        if redirect:
            data['redirect'] = redirect
        if caching:
            data['backend_port'] = 9000
            data['warmup_cache'] = True
        else:
            data['backend_port'] = 8300
            data['warmup_cache'] = False

        full_domain = domain
        self.item_name = domain.replace('.', '_')
        if subdomain:
            self.item_name = '{0}__{1}'.format(self.item_name, subdomain)
            full_domain = '{0}.{1}'.format(subdomain, full_domain)
        data['site'] = self.item_name
        data['domain'] = full_domain
        try:
            return chef_tool.create_databag_item(
                self.parent,
                self.item_name,
                data
            )
        except ChefError as e:
            api.portal.show_message(
                e.message,
                request=self.request,
                type='error')
