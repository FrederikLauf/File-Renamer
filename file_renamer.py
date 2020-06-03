# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:38:10 2020

@author: Frederik
"""


import os


class FileRenamer:

    def __init__(self):
        self._path = r'C:\Users\Frederik\Desktop\Bilder'

    def _make_list_of_files(self):

        file_list = []

        for folder in os.scandir(self._path):
            if os.path.isdir(folder.path):
                for file in os.scandir(folder.path):
                    file_list.append(file.path)
        return file_list
