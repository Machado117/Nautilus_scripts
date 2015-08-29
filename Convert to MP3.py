#!/usr/bin/python3
__author__ = 'diogo'
import subprocess
import time
import os
import os.path
import dbus
session_bus = dbus.SessionBus()
proxy = session_bus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
notification = dbus.Interface(proxy, 'org.freedesktop.Notifications')

file_paths = os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS']
file_paths = file_paths.splitlines()
files_not_converted = []
for file in file_paths:
    file_name = os.path.basename(file)
    extension_index = file_name.rfind(".")
    if extension_index == -1:
        output_file_name = file_name
    else:
        output_file_name = file_name[:extension_index]
    output_file_name_temp = output_file_name + ".mp3"
    i = 1
    while os.path.isfile(os.path.basename(output_file_name_temp)):
        output_file_name_temp = output_file_name + "({}).mp3".format(i)
        i += 1
    output_file_name = output_file_name_temp
    try:
        subprocess.check_call(["ffmpeg", "-i", file, "-codec:a", "libmp3lame", "-qscale:a", "2", output_file_name])
    except:
        files_not_converted.append(file_name)
        if os.path.isfile(output_file_name):
            os.remove(output_file_name)
if files_not_converted:
    notification_message = "Not all files were converted successfully."
    notification_icon = "dialog-warning"
    error_file = "conversion-" + time.strftime("%y%m%d%H%M%S") + ".txt"
    error_file = open(error_file, "w")
    error_file.write("Error converting files:\n" + "\n".join(files_not_converted))
    error_file.close()
else:
    notification_message = "All files were converted successfully."
    notification_icon = "dialog-information"
notification.Notify('Convert to MP3', 0, notification_icon,"Conversion finished", notification_message,[],{},-1)