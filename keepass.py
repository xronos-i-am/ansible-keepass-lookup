#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# (c) 2018, Sergey Malykh <xronos.i.am@gmail.com>
# MIT

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: keepass
    author:
      -  Sergey Malykh <xronos.i.am@gmail.com>
    version_added: "2.7"
    requirements:
      - pykeepass
    short_description: fetch data from keepass
    description:
      - fetch field values from keepass database
    options:
      _terms:
        description: value to search
        required: True
      field:
        description: field to search
        default: 'by_title'
      path:
        description: path to keepass database
        required: True
      password:
        description: The password used to unlock database.
        required: True
"""

EXAMPLES = """
- name: Retrieve entry by title (must be unique)
  debug:
    var: lookup('keepass', 'title', field='by_title', path='/data/keepass.kdbx', password='master_password')
"""

RETURN = """
  _raw:
    description: requested entry data
"""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleLookupError
from ansible.module_utils._text import to_bytes, to_text, to_native

from pykeepass import PyKeePass

class KeePass(object):

    def __init__(self):
        self._db = None
        self.password = None
        self.path = None

    def open(self):
        try:
            self._db = PyKeePass(self.path, password=self.password)
        except Exception as e:
            raise AnsibleLookupError('Error occured when opening database: %s' % to_native(e))

    def get_field(self, _field, value):
        entry = self._db.find_entries(title=value, first=True)

        out = {
          'title': entry.title, 
          'password': entry.password, 
          'username': entry.username, 
          'url': entry.url, 
          'tags': entry.tags, 
          'fields': entry.custom_properties
          # 'notes': entry.notes, 
          # 'icon': entry.icon, 
          # 'path': entry.path, 
        }

        return out

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        db = KeePass()
        
        db.password = kwargs.get('password')
        db.path = kwargs.get('path')

        field = kwargs.get('field', 'by_title')

        db.open()

        values = []
        for term in terms:
            values.append(db.get_field(field, term))

        return values
