import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(sys.path)
from file_renamer.file_renamer import FileRenamer
from test_data.unit_test_data import FILE_LIST, result_name_sort, result_date_sort, result_homonymity_date_sort
from test_data.unit_test_data import FILE_LIST_WITH_OFFSET, result_name_sort_offset, result_date_sort_offset, result_homonymity_date_sort_offset


class TestSortingMethods(unittest.TestCase):
    
    def test_sort_by_name(self):
        fr = FileRenamer()
        fr._file_list = FILE_LIST
        fr._sort_by_name()
        self.assertEqual(fr._file_list, result_name_sort)

    def test_sort_by_date(self):
        fr = FileRenamer()
        fr._file_list = FILE_LIST
        fr._sort_by_date()
        self.assertEqual(fr._file_list, result_date_sort)
        
    def test_sort_by_date_and_homonymity(self):
        fr = FileRenamer()
        fr._file_list = FILE_LIST
        fr._sort_by_date_and_homonymity()
        self.assertEqual(fr._file_list, result_homonymity_date_sort)

    def test_sort_by_name_with_offset(self):
        fr = FileRenamer()
        fr._file_list = FILE_LIST_WITH_OFFSET
        fr._time_offsets = [{'identifier': 'IMG', 'seconds': 117}]
        fr._sort_by_name()
        self.assertEqual(fr._file_list, result_name_sort_offset)

    def test_sort_by_date_with_offset(self):
        fr = FileRenamer()
        fr._file_list = FILE_LIST_WITH_OFFSET
        fr._time_offsets = [{'identifier': 'IMG', 'seconds': 117}]
        fr._sort_by_date()
        self.assertEqual(fr._file_list, result_date_sort_offset)

    def test_sort_by_date_and_homonymity_with_offset(self):
        fr = FileRenamer()
        fr._file_list = FILE_LIST_WITH_OFFSET
        fr._time_offsets = [{'identifier': 'IMG', 'seconds': 117}]
        fr._sort_by_date_and_homonymity()
        self.assertEqual(fr._file_list, result_homonymity_date_sort_offset)


if __name__ == '__main__':
    unittest.main()