#!/usr/bin/env python
# -*- coding:Utf-8 -*-
#
# Dialogue Gtk3 de déconnexion pour OpenBox
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
Dialogue Gtk3 de déconnexion pour OpenBox 
+ Compte à rebours d'extinction.

Dependances:
    @ python >= 3
    @ systemd
    @ gtk3 >= 3
    @ libnotify >= 0.7

Auteur  : Joffrey Darcq
License : GPL3
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Gdk, Notify
from os import environ, system


class Elements(object):
    """
    Define window elements class object
    """
    def add_hbox(self, parent, homogeneous):
        box = Gtk.HBox(homogeneous)
        parent.pack_start(box, False, False, 0)

        return box

    def add_label(self, parent, ch):
        label = Gtk.Label(ch)
        parent.pack_start(label, True, True, 0)

        return label

    def add_separator(self, parent):
        separator = Gtk.HSeparator()
        parent.pack_start(separator, False, False, 10)

        return separator

    def add_button(self, parent, label, icon_name, method):
        button, icon = Gtk.Button(label), Gtk.Image()

        icon.set_from_icon_name(icon_name, 48)
        icon.set_pixel_size(48)

        button.set_image(icon)
        button.set_image_position(2)
        button.set_always_show_image(True)
        button.connect('clicked', method)

        parent.pack_start(button, True, True, 0)

        return button

    def add_stock_button(self, parent, label, stock, method):
        button = Gtk.Button(label, stock)
        button.connect('clicked', method)

        parent.pack_end(button, False, False, 0)

        return button

    def dialog_error(self, error, msg_error):
        """
        Open Dialog with message error
        """
        dialog = Gtk.MessageDialog(self, 0,
                                   Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK,
                                   error,
                                   decorated=True)

        dialog.format_secondary_text(msg_error)
        dialog.run()
        dialog.destroy()

    def display_notification(self, text):
        Notify.init('OpenBox Logout')
        notif = Notify.Notification.new('OpenBox Logout', text,
                                        'system-shutdown')

        notif.show()


class Window(Gtk.Window, Elements):
    """
    Derived class of Gtk.Window and Elements
    """
    def __init__(self):
        Gtk.Window.__init__(self)
        Elements.__init__(self)
        self.set_title('OpenBox Logout')
        self.set_icon_name('system-log-out')
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)

    # PARENT CONTAINER #

        vbox = Gtk.VBox()
        self.add(vbox)

        self.add_label(vbox, 'Openbox {} Session'.format(environ['USER']))

    # CHILDS CONTAINERS #

        self.add_separator(vbox)

        hbox1 = self.add_hbox(vbox, True)
        hbox2 = self.add_hbox(vbox, True)

        self.add_separator(vbox)

        hbox3 = self.add_hbox(vbox, False)

        self.add_separator(vbox)

        hbox4 = self.add_hbox(vbox, False)

    # BUTTONS #

        self.add_button(hbox1, 'Déconnexion', 'system-log-out',
                       self.on_logout_clicked)

        self.add_button(hbox1, 'Redémarrer', 'system-reboot',
                       self.on_reboot_clicked)

        self.add_button(hbox1, 'Éteindre', 'system-shutdown',
                       self.on_poweroff_clicked)

        self.add_button(hbox2, 'Veille', 'system-suspend',
                       self.on_suspend_clicked)

        self.add_button(hbox2, 'Hibernation', 'system-hibernate',
                       self.on_hibernate_clicked)

        self.add_stock_button(hbox4, 'Annuler', Gtk.STOCK_CANCEL, Gtk.main_quit)

        self.add_stock_button(hbox4, 'Démarrer', Gtk.STOCK_OK,
                            self.on_start_clicked)

    # COUNTDOWN #

        self.add_label(hbox3, 'Extinction')

        self.counter = Gtk.SpinButton()
        self.counter.set_adjustment(Gtk.Adjustment(0, 0, 480, 10, 0, 0))
        hbox3.pack_start(self.counter, False, True, 0)

        self.add_label(hbox3, 'minute(s)')

    # LOOPS #

        self.connect('delete-event', Gtk.main_quit)
        self.connect('key-press-event', self.on_key_pressed)

        self.show_all()

# EVENT #

    def on_key_pressed(self, widget, event):
        key = Gdk.keyval_name(event.keyval)

        if key == 'Escape':
            Gtk.main_quit()

# BUTTONS CONNECT #

    def on_logout_clicked(self, widget):
        system('openbox --exit')
        Gtk.main_quit()

    def on_reboot_clicked(self, widget):
        system('systemctl reboot')
        Gtk.main_quit()

    def on_poweroff_clicked(self, widget):
        system('systemctl poweroff')
        Gtk.main_quit()

    def on_suspend_clicked(self, widget):
        system('systemctl suspend')
        Gtk.main_quit()

    def on_hibernate_clicked(self, widget):
        system('systemctl hibernate')
        Gtk.main_quit()

    def on_start_clicked(self, widget):
        value = self.counter.get_value()
        unit = 'minute'

        if value > 1:
            unit = unit + 's'

        if value > 0:
            system('shutdown +%d' % (value))

            text = 'Extinction dans %d %s \n shutdown -c pour annuler'\
                   % (value, unit)

            self.display_notification(text)
            Gtk.main_quit()

        else:
            self.dialog_error('Mauvais compte à rebours',
                              'Nombre positif uniquement')


Window()
Gtk.main()
