#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# (c) 2018-2021, Sergei Malykh <xronos.i.am@gmail.com>
# MIT

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleLookupError
from ansible.module_utils._text import to_bytes, to_text, to_native

import uuid
from pykeepass import PyKeePass

DOCUMENTATION = """
    lookup: keepass
    author:
      -  Sergei Malykh <xronos.i.am@gmail.com>
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
      search:
        description: field to search
        default: 'path'
"""

EXAMPLES = """
- name: Retrieve entry by path
  debug:
    var: lookup('keepass', 'dir1/dir2/id_rsa')
- name: Retrieve entries by title
  debug:
    var: lookup('keepass', 'id_rsa', search='title')
- name: Retrieve entry by uuid
  debug:
    var: lookup('keepass', 'de37072b8cec670ff58212b9cae05806', search='uuid')
- name: Retrieve entries by tags (list) - not tested!
  debug:
    var: lookup('keepass', {{ ['commerce', 'www'] }}, search='tags')
- name: Retrieve entries by custom fields (dict)
  debug:
    var: lookup('keepass', {{ {'tag':'ssh-key'} }}, search='custom')
"""

class KeePass(object):

    def __init__(self):
        self._db = None
        self.password = None
        self.kdbx = None
        self.keyfile = None

    def open(self):
        try:
            self._db = PyKeePass(self.kdbx, password=self.password, keyfile=self.keyfile)
        except Exception as e:
            raise AnsibleLookupError('Error occured when opening database: %s' % to_native(e))

    def format_entry(self, entry):
        out = {
          'title':    entry.title, 
          'password': entry.password, 
          'username': entry.username, 
          'url':      entry.url, 
          'tags':     entry.tags, 
          'fields':   entry.custom_properties,
          'path':     entry.path, 
          'uuid':     entry.uuid.hex, 
          # 'notes':    entry.notes, 
          # 'icon':     entry.icon, 
        }

        return out

    def find_entries(self, **kwargs):
        field = kwargs.get('field')
        value = kwargs.get('value')

        params = {}
        first  = False
        if field == 'title':
            params['title'] = value
        elif field == 'path':
            params['path'] = value
            first = True
        elif field == 'username':
            params['username'] = value
        elif field == 'uuid':
            params['uuid'] = uuid.UUID(value)
            first = True
        elif field == 'tags':
            params['tags'] = value
        elif field == 'custom':
            params['string'] = value

        result = self._db.find_entries(**params)

        if type(result) is not list:
            result = [result]

        return [ self.format_entry(entry) for entry in result ]

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        db = KeePass()
        
        db.password  = variables.get('keepass_password')
        db.kdbx      = variables.get('keepass_db_file')
        db.keyfile   = variables.get('keepass_key_file') # not tested

        search_field = kwargs.get('search', 'path')
        search_value = terms[0]

        db.open()

        return db.find_entries(field=search_field, value=search_value)
