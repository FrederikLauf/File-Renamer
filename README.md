# FileRenamer class

The module `file_renamer` contains the class `FileRenamer` which stores a file list based on a given folder path. Different kinds of sorting can be applied to the file list. A list of new filenames is constructed based on the applied sorting by using given formatting und numbering rules.

# File Renamer GUI

The File Renamer GUI is invoked by executing file_renamer_gui.py.

# Features and use cases

In the following, available sortings and options are described and use cases concerning the creation of files by doing photography are given.

## Sort by name

The files are sorted alphabetically by their name including extension.

**Use case:** The photos are already in alphabetical order which should be preserved.

## Sort by date

The files are sorted by their "modified date" (which for a photography usually coincides with the date and time when it was taken).

**Use case:** The photos are taken with two different cameras and should be merged by ordering them by creation date.

## Sort by homonymity and date

Files with the same name without extension are grouped and the resulting groups are ordered externally by the date of their respective oldest member.

**Use case:** The photos are taken with two cameras in a "jpeg+RAW" format. The saving of a raw file can take a few seconds during which the other camera can take a picture. However, the jpg and RAW files of the same photo should not be separated when sorting by date.

## Time offset

The time offset option consists of a string search tag and an integer in seconds. The time offset will be taken into account for files containing the search tag in their name, when sorting by (homonymity and) date. Example: For the option "DSC" and -114, the modified dates of files containing "DSC" will be decreased by 114 seconds and these new dates will be used for sorting.

**Use case:** The photos have been taken with two cameras with differing system times.

## Renaming format

The new names are contructed as the given prefix plus an increasing number starting from the given start number preceeded by the appropriate amount of zeros.

### Preserve homonymity

This option modifies the renaming pattern such that originally same-named files will obtain a same new name, but only if they are contigous in the current sorting.

**Use case:** Selecting "sort by homonymity and date" (see above), the originally same-named jpg and raw files should have the same name after renaming.
