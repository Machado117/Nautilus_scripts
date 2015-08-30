#!/usr/bin/python3
__author__ = "Diogo Machado"
"""
dependencies: shntool, cuetools
optional: flac, mac, wavpack
"""
import script_helper
import subprocess
import os
import os.path
import shutil


def get_image_file(cue_file):
    f = open(cue_file, 'r')
    for line in f:
        line = line.lstrip(' \t')
        if line[:4] == "FILE":
            str_beg = line.find('"', 4) + 1
            if not str_beg == -1:
                str_end = line.find('"', str_beg)
                if not str_end == -1:
                    f.close()
                    return line[str_beg:str_end]
    f.close()


def create_utf8_version(cue_file):
    encodings = ['utf_8', 'latin_1']
    for i, encoding in enumerate(encodings):
        in_file = open(cue_file, 'r', encoding=encoding, errors='strict')
        try:
            file_text = in_file.read()
            if encoding == 'utf_8':
                return cue_file
            else:
                out_file = open("temp_utf8.cue", 'x', encoding='utf_8')
                out_file.write(file_text)
                out_file.close()
                return "temp_utf8.cue"
        except ValueError:
            pass
        finally:
            in_file.close()


def show_notification(notification_interface, summary, message, icon):
    notification_interface.Notify('Split CUE sheet', 0, icon, summary, message, [], {}, -1)


files = script_helper.get_selected_files()
notification = script_helper.get_notification_interface()

for cue_sheet in files:
    cue_utf8 = create_utf8_version(cue_sheet)
    file_name = os.path.basename(cue_sheet)
    if cue_utf8:
        image_file = get_image_file(cue_utf8)
        if image_file:
            existing_files = os.listdir('.')
            if subprocess.call(
                    ['shnsplit', '-f', cue_utf8, '-t', '%n. %t', '-o', 'flac flac -s -8 -o %f -', image_file]):
                show_notification(notification, file_name, "Error splitting CUE sheet.", 'dialog-warning')
                continue
            if os.path.isfile("00. pregap.flac"):
                os.remove("00. pregap.flac")
            current_files = os.listdir('.')
            new_files = []
            for file in current_files:
                if file not in existing_files and os.path.splitext(file)[1] == ".flac":
                    new_files.append(file)
            new_files.sort()
            if not os.path.splitext(cue_utf8)[1].lower() == ".cue":
                shutil.copy(cue_utf8, "temp_utf8.cue")
                cue_utf8 = "temp_utf8.cue"
            tag_error = subprocess.call(['cuetag.sh', cue_utf8, ] + new_files)
            if cue_utf8 == "temp_utf8.cue":
                if os.path.isfile(cue_utf8):
                    os.remove(cue_utf8)
            if tag_error:
                show_notification(notification, file_name, "Error tagging audio files.", 'dialog-warning')
            else:
                show_notification(notification, file_name, "CUE sheet split successfully.", 'dialog-information')

        else:
            show_notification(notification, file_name, "Invalid audio image file.", 'dialog-warning')

    else:
        show_notification(notification, file_name, "Unknown CUE sheet encoding.", 'dialog-warning')
