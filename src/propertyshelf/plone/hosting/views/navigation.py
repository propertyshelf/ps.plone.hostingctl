# -*- coding: utf-8 -*-

""" View for custom navigation of propertyshelf.plone.hosting """

# plone imports
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs

# local imports
from propertyshelf.plone.hosting.i18n import _


class HostingBreadcrumbs(PhysicalNavigationBreadcrumbs):
    """
        View that overrides the built-in breadcrumb functionality with a custom
        breadcrumb that is based of the traverse_subpath
    """

    def breadcrumbs(self):
        add_blank = False
        crumbs = ()
        base_url = self.context.absolute_url().rstrip('/')
        url = self.request.getURL()
        path = url.split('/')

        # we are in our main view
        if 'applications' in path:
            path_pos = path.index('applications')
        elif 'create-domain' in path:
            path_pos = path.index('create-domain')
            add_blank = True
        elif 'edit-domain' in path:
            path_pos = path.index('edit-domain')
            add_blank = True
        else:
            return crumbs

        base_url += '/applications'
        crumbs += (
            {'absolute_url': base_url,
             'Title': _(u'Applications')},
        )

        titles = path[path_pos + 1:]
        urls = ['/'.join(titles[:i + 1]) for i in range(len(titles))]
        urls = [base_url + '/' + end_url for end_url in urls]
        crumbs += tuple(
            {'absolute_url': abs_url, 'Title': title}
            for (abs_url, title) in zip(urls, titles)
        )

        if add_blank:
            crumbs += ({'absolute_url': '', 'Title': ''},)

        return crumbs
