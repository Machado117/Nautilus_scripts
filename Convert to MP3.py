#!/usr/bin/python3
__author__ = "Diogo Machado"
import script_helper
import subprocess
import time
import os
import os.path

notification = script_helper.get_notification_interface()
file_paths = script_helper.get_selected_files()

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
        output_file_name_temp = output_file_name + " ({}).mp3".format(i)
        i += 1
    output_file_name = output_file_name_temp
    if subprocess.call(["ffmpeg", "-i", file, "-codec:a", "libmp3lame", "-qscale:a", "2", output_file_name]):
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
notification.Notify('Convert to MP3', 0, notification_icon, "Conversion finished", notification_message, [], {}, -1)
