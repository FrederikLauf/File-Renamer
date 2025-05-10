# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:38:10 2020

@author: Frederik
"""

import datetime
import logging
import os
import re
import shutil

from PIL import Image, ExifTags

IMAGE_TYPES = ['jpg', 'JPG', 'png', 'PNG']

class FileRenamer:

    def __init__(self):
        self._basepath = None
        self._file_list = []  # list of original files in basepath as tuples (<name>, <date>[, <corrected date>])
        self._new_names = []  # contructed list of new names
        self._preserve_homonymity = True
        self._namepattern = {"prefix": "", "digits": "1", "startnum": "1"}  # format configuration for renaming
        self._time_offsets = [{'identifier': None, 'seconds': 0}]  # e.g. [{'identifier': 'DSC_', 'seconds': 40}], list type for future use

    def _make_list_of_files(self):
        '''populate self._file_list with files in self._basepath'''
        file_list = []
        for file in os.scandir(self._basepath):
            file_path, file_name = file.path, file.name
            if os.path.isfile(file_path):
                suffix = _filename_extension(file_name)
                if False:  # suffix in self._image_types:
                    date = _get_exif_date(file_path)
                    if date is None:
                        date = _get_modified_date(file_path)
                else:
                    date = _get_modified_date(file_path)
                file_list.append((file_name, date))
        self._file_list = file_list[:]

    def _make_list_of_files_with_time_correction(self):
        result = []
        for item in self._file_list:
            for option in self._time_offsets:
                if option['identifier'] is not None and option['identifier'] in item[0]:
                    orig_time = datetime.datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S')
                    time_delta = datetime.timedelta(minutes=0, seconds=option['seconds'])
                    corr_time = (orig_time + time_delta).strftime('%Y-%m-%d %H:%M:%S')
                    result.append((*item[:2], corr_time))
                    break
            else:
                result.append((*item[:2], item[1]))
        self._file_list = result[:]

    def _sort_by_date(self):
        self._make_list_of_files_with_time_correction()
        self._file_list.sort(key=lambda item: item[2])
        self._file_list = [item[:2] for item in  self._file_list]

    def _sort_by_name(self):
        self._file_list.sort(key=lambda item: item[0])

    def _get_homonymity_groups(self):
        groups = set(
            frozenset(j for j in self._file_list
                if _filename_name(j[0]) == _filename_name(i[0]))
            for i in self._file_list)
        return [list(item) for item in groups]

    def _sort_by_date_and_homonymity(self):
        self._make_list_of_files_with_time_correction()
        hom_groups = self._get_homonymity_groups()
        hom_groups.sort(key=lambda x: min(e[2] for e in x))
        hom_groups = [sorted(i, key=lambda x: x[1]) for i in hom_groups]
        self._file_list = [i[:2] for j in hom_groups for i in j]

    def _make_new_names(self):
        self._new_names = []
        prefix = self._namepattern["prefix"]
        start = self._namepattern["startnum"]
        digits = self._namepattern["digits"]
        previous_name = ""
        idx = 0
        for item in self._file_list:
            current_name, suffix = _filename_name_and_extension(item[0])
            if self._preserve_homonymity is True and current_name == previous_name:
                new_name = previous_new_name
            else:
                zeros = _make_pre_zeros(int(digits), int(start) + idx)
                number = str(int(start) + idx)
                idx += 1
                new_name = prefix + zeros + number
                previous_new_name = new_name
            self._new_names.append(new_name + "." + suffix)
            previous_name = current_name

    def _rename_copy(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_folder = os.path.join(self._basepath, "renamed_files_" + time)
        os.mkdir(new_folder)
        for i, (old, new) in enumerate(zip(self._file_list, self._new_names)):
            try:
                old_path = os.path.join(self._basepath, old[0])
                new_path = os.path.join(new_folder, new)
                shutil.copy2(old_path, new_path)
            except Exception as err:
                print("An Error occurred:", err)

#--------------utility functions-----------------------------------------------
def _filename_name(filename):
    return '.'.join(filename.split('.')[:-1])

def _filename_extension(filename):
    return filename.split('.')[-1]

def _filename_name_and_extension(filename):
    *name, ext = filename.split('.')
    return '.'.join(name), ext

def _make_pre_zeros(digits, idx):
    return (digits - len(str(idx))) * '0'

def _get_exif_date(image_path):
    img = Image.open(image_path)
    exif_raw = img._getexif()
    if not exif_raw:
        return None
    tags = ExifTags.TAGS
    exif_data = {tags[k]: v for k, v in exif_raw.items() if k in tags}
    if 'DateTimeOriginal' in exif_data:
        day, time = exif_data['DateTimeOriginal'].split(' ')
        date = day.replace(":", "-") + " " + time
        return date
    return None

def _get_modified_date(file_path):
    mtime = os.stat(file_path).st_mtime
    return datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
#------------------------------------------------------------------------------
