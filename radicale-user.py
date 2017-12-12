#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""radicale-user usage:
    input  : radicale-user username
    output : username:bcrypthash

Redirect the output to yours user(s) file path:
    radicale-user username >> /etc/radicale/users
"""

import getpass
import bcrypt
import sys

try:
    user = sys.argv[1]
except IndexError:
    sys.exit(__doc__)

password = getpass.getpass('Password: ')
password = bytes(password, 'utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

print(('{0}:{1}'.format(user, hashed)))
