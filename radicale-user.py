#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage exemple:
    input  :./script username password
    output : username:bcrypthash

Add to Htpasswd filename:
    ./script username password >> /etc/radicale/users
"""

import bcrypt
import sys

try:
    password = bytes(sys.argv[2], 'utf-8')
except IndexError:
    sys.exit('Usage: %s [username] [password]' % sys.argv[0])
else:
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
    print('%s:%s' % (sys.argv[1], hashed))