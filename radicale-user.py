#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Add a Radicale user without Htpasswd (Apache package)
# Copyright (C) 2017 Joffrey
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
"""Add a Radicale user without Htpasswd (Apache package)
Usage:
    input  : radicale-user username
    output : username:bcrypthash

Redirect the output to your(s) user(s) file:
    radicale-user username >> /etc/radicale/users"""

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
