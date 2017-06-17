#!/usr/bin/env python

# Copyright (C) 2007-2017 Arjan Molenaar <gaphor@gmail.com>
#                         Artur Wroblewski <wrobell@pld-linux.org>
#                         Dan Yeaw <dan@yeaw.me>
#
# This file is part of Gaphor.
#
# Gaphor is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# Gaphor is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaphor.  If not, see <http://www.gnu.org/licenses/>.
"""
Basic stuff for toplevel windows.
"""

from __future__ import absolute_import
import os.path
import pkg_resources
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from zope import interface
from .interfaces import IUIComponent


ICONS = (
    'gaphor-24x24.png',
    'gaphor-48x48.png',
    'gaphor-96x96.png',
    'gaphor-256x256.png',
)


@interface.implementer(IUIComponent)
class ToplevelWindow(object):

    menubar_path = ''
    toolbar_path = ''
    resizable = True

    def __init__(self):
        self.window = None

    def ui_component(self):
        raise NotImplementedError

    def construct(self):

        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title(self.title)
        self.window.set_size_request(*self.size)
        self.window.set_resizable(self.resizable)

        # set default icons of gaphor windows
        icon_dir = os.path.abspath(pkg_resources.resource_filename('gaphor.ui', 'pixmaps'))
        icons = (GdkPixbuf.Pixbuf.new_from_file(os.path.join(icon_dir, f)) for f in ICONS)
        self.window.set_icon_list(*icons)

        self.window.add_accel_group(self.ui_manager.get_accel_group())

        
        if self.menubar_path or self.toolbar_path:
            # Create a full featured window.
            vbox = Gtk.VBox()
            self.window.add(vbox)
            vbox.show()

            menubar = self.ui_manager.get_widget(self.menubar_path)
            if menubar:
                vbox.pack_start(menubar, False, True, 0)
            
            toolbar = self.ui_manager.get_widget(self.toolbar_path)
            if toolbar:
                vbox.pack_start(toolbar, False, True, 0)

            vbox.pack_end(self.ui_component(, True, True, 0), expand=self.resizable)
            vbox.show()
            # TODO: add statusbar
        else:
            # Create a simple window.
            self.window.add(self.ui_component())
        self.window.show()


# vim:sw=4:et:ai
