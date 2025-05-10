# -*- coding: utf-8 -*-

from file_renamer import FileRenamer
from unittest_data.unit_test_result import result_name_sort, result_date_sort, result_homonymity_date_sort
from unittest_data.unit_test_result import result_name_sort_offset, result_date_sort_offset, result_homonymity_date_sort_offset


if __name__ == "__main__":
    """
    unit test
    """
    
    fr = FileRenamer()
    fr._basepath = r"unittest_data/unittest_data_1"
    fr._make_list_of_files()
    fr._sort_by_name()
    print("_sort_by_name")
    assert fr._file_list == result_name_sort
    for item in fr._file_list:
        print(item)
    print(10 * '*')
    fr._sort_by_date()
    print("_sort_by_date")
    assert fr._file_list == result_date_sort
    for item in fr._file_list:
        print(item)
    print(10 * '*')
    fr._sort_by_date_and_homonymity()
    print("_sort_by_date_and_homonymity")
    assert fr._file_list == result_homonymity_date_sort
    for item in fr._file_list:
        print(item)
    print(10 * '*')
    print(10 * '*')
    print("DSC = IMG + 117s")
    fr = FileRenamer()
    fr._basepath = r"unittest_data/unittest_data_2"
    fr._time_offsets = [{'identifier': 'IMG', 'seconds': 117}]
    fr._make_list_of_files()
    fr._sort_by_name()
    print("_sort_by_name")
    for item in fr._file_list:
        print(item)
    assert fr._file_list == result_name_sort_offset
    print(10 * '*')
    fr._sort_by_date()
    print("_sort_by_date")
    for item in fr._file_list:
        print(item)
    assert fr._file_list == result_date_sort_offset
    print(10 * '*')
    fr._sort_by_date_and_homonymity()
    print("_sort_by_date_and_homonymity")
    for item in fr._file_list:
        print(item)
    assert fr._file_list == result_homonymity_date_sort_offset
    print(10 * '*')
    print("!!!No Assertion Errors!!!")
    print(10 * '*')