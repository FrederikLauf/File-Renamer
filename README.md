# FileRenamer class

The module `file_renamer` contains the class `FileRenamer` which stores a file list based on a given folder path. Different kinds of sorting can be applied to the file list. A list of new filenames is constructed based on the applied sorting according to the configured formatting und numbering rules.

# File Renamer GUI

The File Renamer GUI is invoked by executing file_renamer_app.py.

# Features and use cases

In the following, all available sortings and options are described. Use cases concerning the creation of files by performing photography are given.

*Remark: The name and extension of a filename are defined like `<filename> = <name>.<extension>` such that `<name>` does not contain any dots. The motivation for this definition is that for example 'abc.jpg' and 'abc.jpg.xmp' should be considered to share the same name.*

## Sort by name

The files are sorted alphabetically by their name including extension.

**Use case:** The photos are already in alphabetical order which should be preserved.

## Sort by date

The files are sorted by their "modified date", also known as "mtime". (NB: The user is responsible for controlling the mtime of their files. The standard behaviour of file copying methods on different operationg systems has to be considered. For a photo file on Windows, the mtime will usually stay at the time when it was taken/saved in the camera. An option to use the EXIF time if available may be added in the future.)

**Use case:** The photos are taken with two different cameras and should be merged in chronological order.

## Sort by homonymity and date

Files with the same name (disregarding the extension) are grouped together and the resulting groups are ordered externally by the dates of their respective oldest members.

**Use case:** The photos are taken with two cameras in a "jpeg+RAW" format. The saving of a raw file can take a few seconds during which the other camera can take another picture. However, the jpg and RAW files of the same photo should not be separated when sorting by date. Furthermore, if the photos are developed and edited by some software creating associated files with another extension (e.g. .NEF.xmp), also these new files should be sorted together with the original images.

## Time offset

The time offset option consists of a string search tag and an integer for seconds. The time offset will be taken into account for files containing the search tag in their name   when sorting by (homonymity and) date. Example: For the option "DSC" and -114, the modified dates of files containing "DSC" will be decreased by 114 seconds and these modified dates will be used for sorting.

**Use case:** The photos have been taken with two cameras with differing system times.

## Renaming format

The new names are constructed as the given prefix plus an increasing number, starting from the given start number and being preceeded by the appropriate amount of zeros.

### Preserve homonymity

This option modifies the renaming pattern such that originally same-named files will obtain a same new name, but only if they are contigous in the applied sorting.

**Use case:** Selecting "sort by homonymity and date" (see above), the originally same-named jpg and RAW files should be same-named also after renaming.
