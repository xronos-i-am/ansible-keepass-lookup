#!/usr/bin/env python3.6
import uuid
from pykeepass import PyKeePass

# load database
kp = PyKeePass('./test.kdbx', password='test')

# find by title
entry = kp.find_entries(title='id_rsa', first=True)
print(entry.title)

# find by path
entry = kp.find_entries(path='dir1/dir2/id_rsa', first=True)
print(entry.path)

# find by uuid
entry = kp.find_entries(uuid=uuid.UUID('de37072b8cec670ff58212b9cae05806'), first=True)
print(entry.uuid)