# -*- coding: utf-8 -*-
"""Setup for ps.plone.hostingctl package."""

from setuptools import setup, find_packages

version = '0.1dev'
description = 'Hosting management for Propertyshelf\'s shared hosting using ' \
              'Chef Data Bags.'
long_description = ('\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
]))

install_requires = [
    'setuptools',
    'plone.api',
    'plone.directives.form',
    'pychef',
    'zope.app.container',
]

setup(
    name='ps.plone.hostingctl',
    version=version,
    description=description,
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='plone hosting chef',
    author='Propertyshelf, Inc.',
    author_email='development@propertyshelf.com',
    url='https://github.com/propertyshelf/ps.plone.hostingctl',
    download_url='http://pypi.python.org/pypi/ps.plone.hostingctl',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['ps', 'ps.plone'],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': [
            'plone.app.testing',
        ],
    },
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
