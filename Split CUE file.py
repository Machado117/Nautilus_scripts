#!/usr/bin/python3
__author__ = 'diogo'
import subprocess
import dbus
session_bus = dbus.SessionBus()
proxy = session_bus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
notification = dbus.Interface(proxy, 'org.freedesktop.Notifications')

file_paths = os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS']