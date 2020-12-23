# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:38:10 2020

@author: Frederik
"""

import os


class FileRenamer:

    def __init__(self):
        self._path = None
        self._valid_types = ['jpg', 'JPG', 'AVI', 'avi', 'mp4', 'png', 'PNG']
        if self._only_folders():
            self._file_list = self._make_list_of_files_from_folders()
        else:
            self._file_list = self._make_list_of_files()
        self._prefix = 'Urlaub'

    def _only_folders(self):
        for item in os.scandir(self._path):
            if os.path.isfile(item.path):
                return False
        return True

    def _make_pre_zeros(self, idx):
        zeros = (len(str(len(self._file_list))) - len(str(idx))) * '0'
        return zeros

    def _make_list_of_files(self):

        file_list = []
        for item in os.scandir(self._path):
            suffix = item.path.split('.')[-1]
            if os.path.isfile(item.path) and suffix in self._valid_types:
                file_list.append(item.path)
        return sorted(file_list)

    def _make_list_of_files_from_folders(self):

        folder_list = [folder.path for folder in os.scandir(self._path)]
        file_list = []
        for folder in sorted(folder_list):
            folder_files = [file.path for file in os.scandir(folder)]
            for file in sorted(folder_files):
                suffix = file.split('.')[-1]
                if os.path.isfile(file) and suffix in self._valid_types:
                    file_list.append(file)
        return file_list

    def _move_file_to_new(self):

        new_dir = self._path + '\\' + self._prefix + '_renamed'
        os.mkdir(new_dir)

        for idx, file in enumerate(self._file_list):
            suffix = '.' + file.split('.')[-1]
            pre_zeros = self._make_pre_zeros(idx + 1)
            new_name = self._prefix + '_' + pre_zeros + str(idx + 1) + suffix
            new_path = new_dir + '\\' + new_name
            os.replace(file, new_path)
