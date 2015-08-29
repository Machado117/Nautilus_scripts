__author__ = 'diogo'
import os
import dbus


def get_selected_files():
    return os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS'].splitlines()


def get_notification_interface():
    session_bus = dbus.SessionBus()
    proxy = session_bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    return dbus.Interface(proxy, 'org.freedesktop.Notifications')
