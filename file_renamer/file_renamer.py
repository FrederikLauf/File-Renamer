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


class FileRenamer:

    def __init__(self):
        self._basepath = None
        self._image_types = ['jpg', 'JPG', 'png', 'PNG']
        self._file_list = []
        self._new_names = []
        self._namepattern = {"prefix": "", "digits": "1", "startnum": "1"}
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
        self.logger = logging.getLogger("FileRenamer")

    @staticmethod
    def _make_pre_zeros(digits, idx):
        zeros = (digits - len(str(idx))) * '0'
        return zeros

    def _get_default_prefix(self):
        file_names = [item[0] for item in self._file_list]
        prefices = [re.search(r"(\D+).*\.\w+", item) for item in file_names]
        candidates = set(item.group(1) for item in prefices if item is not None)
        return candidates.pop() if len(candidates) == 1 else ""

    @staticmethod
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

    @staticmethod
    def _get_modified_date(file_path):
        mtime = os.stat(file_path).st_mtime
        timestamp_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        return timestamp_str

    def _make_list_of_files(self):

        file_list = []
        for file in os.scandir(self._basepath):
            file_path = file.path
            file_name = os.path.split(file_path)[-1]
            if os.path.isfile(file_path):
                suffix = file_name.split('.')[-1]
                if suffix in self._image_types:
                    date = self._get_exif_date(file_path)
                    if date is None:
                        date = self._get_modified_date(file_path)
                else:
                    date = self._get_modified_date(file_path)
                file_list.append((file_name, date))
        return file_list

    def _sort_by_date(self):
        self._file_list.sort(key=lambda item: item[1])

    def _sort_by_name(self):
        self._file_list.sort(key=lambda item: item[0])

    def _make_new_names(self):
        new_names = []
        prefix = self._namepattern["prefix"]
        start = self._namepattern["startnum"]
        digits = self._namepattern["digits"]
        for idx, item in enumerate(self._file_list):
            suffix = item[0].split(".")[-1]
            zeros = self._make_pre_zeros(int(digits), int(start) + idx)
            number = str(int(start) + idx)
            new_name = prefix + zeros + number + "." + suffix
            new_names.append(new_name)
        return new_names

    def _rename_override(self):
        for old, new in zip(self._file_list, self._new_names):
            try:
                old_path = os.path.join(self._basepath, old[0])
                new_path = os.path.join(self._basepath, new)
                os.rename(old_path, new_path)
            except Exception as err:
                print("An Error occurred:", err)

    def _rename_copy(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        new_folder = os.path.join(self._basepath, "renamed_files_" + time)
        os.mkdir(new_folder)
        for old, new in zip(self._file_list, self._new_names):
            try:
                old_path = os.path.join(self._basepath, old[0])
                new_path = os.path.join(new_folder, new)
                shutil.copy2(old_path, new_path)
            except Exception as err:
                print("An Error occurred:", err)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
    logging.info("Start")
    print(FileRenamer._get_exif_date(r"C:\Users\Frederik\Pictures\Fremde\Triest\Trieste 4\IMG_7461.JPG"))
    logging.info("Stop")

    fr = FileRenamer()
    fr._basepath = r"C:\Users\Frederik\Pictures\Fremde\Jamaika 2006"
    lof = fr._make_list_of_files()
    for item in lof:
        print(item)
