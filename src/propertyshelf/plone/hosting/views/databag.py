# -*- coding: utf-8 -*-

""" Views for Databags in propertyshelf.plone.hosting """

# plone imports
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# local imports
from propertyshelf.plone.hosting.i18n import _


class DataBagView(BrowserView):
    """
        This view shows the data bag items contained in the given
        databag.
    """

    index = ViewPageTemplateFile('templates/databag.pt')
    label = _(u'Databag View')

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        return self.context.available

    def update(self):
        self.context.update()
