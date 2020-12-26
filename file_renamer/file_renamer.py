# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:38:10 2020

@author: Frederik
"""

import os
from PIL import Image, ExifTags
import logging
import re
import datetime

class FileRenamer:

    def __init__(self):
        self._basepath = None
        self._image_types = ['jpg', 'JPG', 'png', 'PNG']
        self._file_list = []
        self._namepattern = {"prefix": "", "digits": "1", "startnum": "1"}
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)
        self.logger = logging.getLogger("FileRenamer")

    def _only_folders(self):
        for item in os.scandir(self._basepath):
            if os.path.isfile(item.path):
                return False
        return True

    @staticmethod
    def _make_pre_zeros(digits, idx):
        zeros = (digits - len(str(idx))) * '0'
        return zeros

    # @staticmethod
    # def _get_photo_shooting_date(image_path):
    #     img = Image.open(image_path)
    #     exif_data = img._getexif()
    #     for k, v in ExifTags.TAGS.items():
    #         if v == 'DateTimeOriginal':
    #             day, time = exif_data[k].split(' ')
    #             day = '.'.join(reversed(day.split(':')))
    #             return day, time

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

    # def _make_list_of_files_from_folders(self):
    #
    #     folder_list = [folder.path for folder in os.scandir(self._basepath)]
    #     file_list = []
    #     for folder in sorted(folder_list):
    #         folder_files = [file.path for file in os.scandir(folder)]
    #         for file in sorted(folder_files):
    #             suffix = file.split('.')[-1]
    #             if os.path.isfile(file) and suffix in self._image_types:
    #                 file_list.append(file)
    #     return file_list

    def _move_file_to_new(self):
        pass


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
