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
from propertyshelf.plone.hosting import utils


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
        if not chef_tool:
            return None

        data = utils.prepare_data(data)
        self.item_name = data.get('id')

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


class EditDomainItemForm(form.Form):
    """
        Form for editing an existing databag item of the specific 'domain' type
    """

    successMessage = _(u'Data successfully updated.')
    noChangesMessage = _(
        u'There was a problem while updating this item. No changes made.'
    )

    fields = field.Fields(IDomainDatabagItem)
    label = _(u'Edit ')
    parent = None
    item_name = None
    _valid = True

    @property
    def valid(self):
        return self._valid

    def update_path(self, traverse_subpath):
        if len(traverse_subpath) == 2:
            self.parent = traverse_subpath[0]
            self.item_name = traverse_subpath[1]
            self.label += self.item_name

    def getContent(self):
        if self.parent and self.item_name:
            chef_tool = queryUtility(IChefTool)
            if chef_tool:
                data = chef_tool.get_dict_from_item(self.parent, self.item_name)
                if data:
                    item_id = data.get('id')
                    split_id = item_id.split('__')
                    if len(split_id) == 2:
                        data['subdomain'] = split_id[1]
                    data['domain'] = split_id[0].replace('_', '.')
                    return data

        self._valid = False
        api.portal.show_message(
            _(u'Databag item not found.'),
            request=self.request,
            type='error')
        return {}

    def applyChanges(self, data):
        content = self.getContent()
        content.update(data)
        content = utils.prepare_data(content)

        chef_tool = queryUtility(IChefTool)
        if chef_tool:
            chef_tool.edit_databag_item(self.parent, self.item_name, content)
            return content

        return None

    @button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        if changes:
            api.portal.show_message(
                self.successMessage,
                request=self.request,
                type='info')
            if self.item_name != changes.get('id'):
                url = '%s/edit-item/%s/%s' % (
                    self.context.absolute_url(),
                    self.parent,
                    changes.get('id'))
                self.request.response.redirect(url)
        else:
            api.portal.show_message(
                self.noChangesMessage,
                request=self.request,
                type='warn')
