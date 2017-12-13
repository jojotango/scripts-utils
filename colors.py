#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Python 3 Color class for colorise your scripts outputs
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
"""
Colors availables:
    black, white, red, green, yellow, blue, purple, cyan.

Usage exemple:

    from . import Color

    Color = Color()

    Color.normal(text, color)        # Change text color
    Color.bold(text, color)          # Change text color + bold
    Color.background(text, color)    # Change text background color
"""


class Color(object):
    """Defines a Color class object for colorise your scripts outputs
    """
    def __init__(self):
        self.__normal_colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
        }
        self.__bold_colors = {
            'black': '\033[1;30m',
            'red': '\033[1;31m',
            'green': '\033[1;32m',
            'yellow': '\033[1;33m',
            'blue': '\033[1;34m',
            'purple': '\033[1;35m',
            'cyan': '\033[1;36m',
            'white': '\033[1;37m',
        }
        self.__background_colors = {
            'black': '\033[40m',
            'red': '\033[41m',
            'green': '\033[42m',
            'yellow': '\033[43m',
            'blue': '\033[44m',
            'purple': '\033[45m',
            'cyan': '\033[46m',
            'white': '\033[47m',
        }
        self.__reset = '\033[0m'

    def normal(self, string, color='white'):
        """Return string argv with normal weight color argv
        """
        return self.__normal_colors[color] + string + self.__reset

    def bold(self, string, color='white'):
        """Return string argv with bold weight color argv
        """
        return self.__bold_colors[color] + string + self.__reset

    def background(self, string, color='white'):
        """Return string argv with background color argv
        """
        return self.__background_colors[color] + string + self.__reset

    def get_normal_dict(self):
        return self.__normal_colors

    def get_bold_dict(self):
        return self.__bold_colors

    def get_background_dict(self):
        return self.__background_colors

if __name__ == '__main__':
    import sys

    Color = Color()

    # Dicts
    bold_dict = Color.get_bold_dict()
    normal_dict = Color.get_normal_dict()
    background_dict = Color.get_background_dict()

    colors = list(normal_dict.keys())

    for color in colors:
        # Normal colors
        value = normal_dict[color].replace('\033[', '')
        sys.stdout.write(
            '    {0} {1} 0m    |'.format(
                value,                              # 0
                Color.normal(' normal ', color),    # 1
            )
        )
        # Bold colors
        value = bold_dict[color].replace('\033[', '')
        sys.stdout.write(
            '    {0} {1} 0m    |'.format(
                value,                            # 0
                Color.bold(' bold ', color),    # 1
            )
        )
        # Background colors
        value = background_dict[color].replace('\033[', '')
        sys.stdout.write(
            '    {0} {1} 0m     |'.format(
                value,                                      # 0
                Color.background(' background ', color),    # 1
            )
        )
        # Color name
        sys.stdout.write('    {}\n'.format(color))
