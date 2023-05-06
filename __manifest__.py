# -*- coding: utf-8 -*-
{
    'name': "Google Drive Files",

    'summary': """
        Manage Google Drive Files""",

    'description': """
        Manage Google Drive Files
    """,

    'author': "Md Mazharul Islam",
    'website': "https://www.github.com/mazharulsabbir",
    'category': 'Tools',
    'version': '16.0.1',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [],
    # external dependencies
    "external_dependencies": {"python": ['google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib']}
}
