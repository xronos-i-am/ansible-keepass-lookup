#!/usr/bin/env python3.6
from pykeepass import PyKeePass

# load database
kp = PyKeePass('./test.kdbx', password='test')

# find any group by its name
entry = kp.find_entries(title='id_rsa', first=True)

print(entry.custom_properties)