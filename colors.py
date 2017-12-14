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
        self.__colors = {
            'none': '0m',
            'black': '30m',
            'red': '31m',
            'green': '32m',
            'yellow': '33m',
            'blue': '34m',
            'purple': '35m',
            'cyan': '36m',
            'white': '37m',
        }

        self.__prefix = '\033['

    def normal(self, string, color='none'):
        """Return string argv with light weight color argv
        """
        return '{0}{1}{0}{2}'.format(
            self.__prefix,                    # 0
            self.__colors[color] + string,    # 1
            self.__colors['none']             # 2
        )

    def bold(self, string, color='none'):
        """Return string argv with bold weight color argv
        """
        color = self.__colors[color]
        if  color == '0m':
            color = '1m'
        return '{0}{1}{0}{2}'.format(
            self.__prefix,             # 0
            '1;' + color + string,     # 1
            self.__colors['none']      # 2
        )

    def background(self, string, color='none'):
        """Return string argv with background color argv
        """
        return '{0}{1}{0}{2}'.format(
            self.__prefix,                                      # 0
            self.__colors[color].replace('3', '4') + string,    # 1
            self.__colors['none']                               # 2
        )

    def get_colors_dict(self):
        return self.__colors

if __name__ == '__main__':
    import sys

    Color = Color()

    colors_dict = Color.get_colors_dict()
    colors = list(colors_dict.keys())

    for color in colors:
        # Normal colors
        sys.stdout.write(
            '    {0:3} {1} 0m    |'.format(
                colors_dict[color],                 # 0
                Color.normal(' normal ', color),    # 1
            )
        )
        # Bold colors
        value = colors_dict[color]
        if value == '0m':
            value = '1m'
        sys.stdout.write(
            '    {0:5} {1} 0m    |'.format(
                '1;' + value,                   # 0
                Color.bold(' bold ', color),    # 1
            )
        )
        # Background colors
        sys.stdout.write(
            '    {0:3} {1} 0m     |'.format(
                colors_dict[color].replace('3', '4'),       # 0
                Color.background(' background ', color),    # 1
            )
        )
        # Color name
        sys.stdout.write('    {}\n'.format(color))
