# -*- coding: utf-8 -*-

""" Views for Databags in propertyshelf.plone.hosting """

# plone imports
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DataBagView(BrowserView):

    index = ViewPageTemplateFile('templates/databag.pt')

    def __call__(self):
        self.update()
        return self.index()

    @property
    def available(self):
        return self.context.available

    def get_databag_items(self):
        return self.context.get_databag_items()

    def update(self):
        self.context.update()
