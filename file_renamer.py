# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:38:10 2020

@author: Frederik
"""


import os


class FileRenamer:

    def __init__(self):
        self._path = r'C:\Users\Frederik\Pictures\Fremde\Heidelberg'
        self._valid_types = ['jpg', 'JPG', 'AVI', 'avi', 'mp4']

    def _make_list_of_files(self):

        folder_list = [folder.path for folder in os.scandir(self._path)]
        file_list = []
        for folder in sorted(folder_list):
            if os.path.isdir(folder):
                folder_files = [file.path for file in os.scandir(folder)]
                for file in sorted(folder_files):
                    if file.split('.')[-1] in self._valid_types:
                        file_list.append(file)
        return file_list
