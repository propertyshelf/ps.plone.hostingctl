from setuptools import setup, find_packages

version = '0.1'

long_description = (
    open('README.md').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(
    name='propertyshelf.plone.hosting',
    version=version,
    description="Add-on for Chef interface and the associated data bags.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='chef',
    author='Zach Cashero',
    author_email='zach@propertyshelf.com',
    url='https://github.com/propertyshelf/propertyshelf.plone.hosting',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['propertyshelf', 'propertyshelf.plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.directives.form',
        'plone.api',
        'pychef',
        'zope.app.container',
        # -*- Extra requirements: -*-
    ],
    extras_require={'test': ['plone.app.testing']},
    entry_points="""
        # -*- Entry points: -*-
        [z3c.autoinclude.plugin]
        target = plone
        """,
)
