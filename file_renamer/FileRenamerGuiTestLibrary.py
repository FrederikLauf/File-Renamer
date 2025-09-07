import re
import time
import tkinter as tk
from unittest.mock import MagicMock

import file_renamer_gui
from unittest_data.unittest_data import FILE_LIST, result_name_sort, result_date_sort, result_homonymity_date_sort
from unittest_data.unittest_data import FILE_LIST_WITH_OFFSET, result_name_sort_offset, result_date_sort_offset, result_homonymity_date_sort_offset



class FileRenamerGuiTestLibrary:

    def __init__(self):
        self.root = tk.Tk()
        self.frg = file_renamer_gui.FileRenamerGUI(self.root)
        self.root.withdraw()

    def select_test_image_folder(self):
        """Mock folder selection and file list and call browse button callback."""
        self.frg._get_folder_directory = MagicMock(return_value="test_images")
        self.frg.fr._make_file_list = MagicMock(return_value=None)
        self.frg.fr._file_list = FILE_LIST
        self.frg._browse_button_clicked()

    def original_list_should_be_ordered_by(self, ordering):
        actual_list = list(self.frg._filebox_originals.get(0, tk.END))
        expected = {
                    "Name": result_name_sort,
                    "Date": result_date_sort,
                    "Homonymity And Date": result_homonymity_date_sort
                    }[ordering]
        if actual_list != expected:
            msg = "Wrong originals list displayed: {}".format(actual_list)
            raise AssertionError(msg)

    def select_sort_by(self, sorting):
        if sorting == "Name":
            self.frg._sortchoice_var.set(1)
        elif sorting == "Date":
            self.frg._sortchoice_var.set(2)
        elif sorting == "Homonymity And Date":
            self.frg._sortchoice_var.set(3)

    def digits_spinbox_should_have_value(self, n):
        print(list(self.frg._filebox_preview.get(0, tk.END)))
        expected = int(n)
        actual = int(self.frg._digitnumber_spinbox.get())
        print('A', actual)
        actual = int(self.frg._digits_var.get())
        print('b', actual)
        if expected != actual:
            msg = "Digits spinbox shows {} instead of {}.".format(actual, expected)
            raise AssertionError(msg)

    def select_strictly_increase(self):
        # self.frg._radio_homonymity_no.select()
        self.frg._homonymity_var.set(2)

    def select_preserve_homonymity(self):
        # self.frg._radio_homonymity_yes.select()
        self.frg._homonymity_var.set(1)

    def enter_start_number(self, n):
        # self.frg._startnumber_entry.insert(0, n)
        self.frg._startnumber_var.set(n)

    def enter_prefix(self, prefix):
        # self.frg._prefix_entry.insert(0, prefix)
        self.frg._prefix_var.set(prefix)

    def preview_list_numbers_should_start_from(self, n):
        n = int(n)
        actual_list = list(self.frg._filebox_preview.get(0, tk.END))
        actual_first = actual_list[0]
        m = re.match(r".*?(\d+).*", actual_first)
        if m is None:
            msg = "Preview names do not contain numbers."
            raise AssertionError(msg)
            return
        start = int(m.groups()[0])
        if start != n:
            msg = "Numbers start with {} instead of {}.".format(start, n)
            raise AssertionError(msg)

    def preview_list_prefixes_should_equal(self, prefix):
        actual_list = list(self.frg._filebox_preview.get(0, tk.END))
        actual_first = actual_list[0]
        if not actual_first.startswith(prefix):
            msg = "Preview name {} does not start with {}".format(actual_first, prefix)
            raise AssertionError(msg)