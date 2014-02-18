# -*- coding: utf-8 -*-

# zope imports
from Products.Five import BrowserView
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class Databags(BrowserView):
    """"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.traverse_subpath = []

    def publishTraverse(self, request, name):
        self.traverse_subpath.append(name)
        return self

    @property
    def available(self):
        return True

    def form(self):
        return

    def list_databags(self):
        return []

    def databag_items(self):
        if len(self.traverse_subpath) == 1:
            databag = self.traverse_subpath[0]
            return [databag]

    def databag_item_details(self):
        if len(self.traverse_subpath) == 2:
            databag = self.traverse_subpath[0]
            item = self.traverse_subpath[1]
            return {databag: item}
