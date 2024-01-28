# nanolib
Few Python modules to solve typical tasks of file processing

## Package nano_file_utils

### Module filename_processing.py

#### numerize_filenames_for_proper_ordering(directory, max_number_of_patterns = 999)

Despite the fact that humans work with computers for many decades,
they stubbornly step on the same rake - they start enumerate files with
abc1.ext, abc2.ext, and so on, ultimately getting the list (of 12 files) sorted as:
```
abc1.ext
abc10.ext
abc11.ext
abc12.ext
abc2.ext
...
abc9.ext
```

```numerize_filenames_for_proper_ordering()``` function solve this problem,
it detects numeric sequence in the file names and left pad this numeric part with
zeros, for above example giving
```
abc01.ext
abc02.ext
...
abc09.ext
abc10.ext
abc11.ext
abc12.ext
```
First argument is ```directory``` like 'C:\ABC' under Windows.
Second optional argument is ```max_number_of_patterns = 999```.
For above listed example all file names exibit the same single pattern -
```
abc<number>.ext
```
but the directory with files
```
abc1.ext
abc2.ext
report1.txt
report1.doc
```
is described with 3 different patterns.

If you want to limit the "diversity" of processed files in the directory
to only one pattern, that is all file names differ only by numeric part,
you should call the function as
```numerize_filenames_for_proper_ordering("dir", max_number_of_patterns = 1)```
If the function detects more than one pattern, it will raise
```
ValueError(f"Too many different file patterns, max {max_number_of_patterns} allowed")
```
All these details are complicated, to simplify the understanding of the
functionlity check ```../nano_file_utils_test/filename_processing_test.py```


### Module file_operations.py

#### import get_names_of_directory_items(directory)

This is helper function, that reads given 'directory' and returns the list
of items with names that do not start with dot (returns all non hidden items).

#### batch_file_rename(directory, original_filenames, new_filenames)

This function renames files in given 'directory', every file 'original_filenames[i]'
is renamed to 'new_filenames[i]'. Naturally expected that len(original_filenames) is
equal to the len(new_filenames). Before making the rename, the function check that
new filename is different from the old one.


## Package scripts

### Module renamer.py

Simple script to rename files in a directory. Windows gives very specific and
hard to understand facilities of group files renaming, this script can simplify
this task.

This script is called from BAT file which resides in system PATH:

```
rem Should be present one argument which is file extension without dot
rem How to use:
rem	Update C:\Prjs\nanolib\scripts\renamer.py, function new_name(old)
rem	Cd into directory with files to be renamed
rem	Run this script like
rem			renamer EXT
set PYTHONPATH=C:\Prjs\nanolib;%PYTHONPATH%
echo %PYTHONPATH%
py -m scripts.renamer %*
```

### Module ren-lambda.py

If the 'renamer' script (see above) is configured for specific rules of
renaming by editing Python file, this 'ren-lambda' script is made flexible
by passing rules as lambda expresssions through command line options.

```
rem
rem ren-lambda renames files in the current directory
rem How to use:
rem	Cd into directory with files to be renamed
rem	Run this script like
rem			ren-lambda "filter-expression" "new-name-expression"
rem Both command line options are expressions in Python syntax, that take 2 arguments:
rem	base - base name of the filename
rem	ext - extension of filename without .
rem filter-expression returns boolean true if the file should be renamed
rem new-name-expression returns string as new name, constructed from 'base' and 'ext'
rem
rem Actually both lambda expressions get not 2 but 6 arguments:
rem     base, ext, Base, Ext, BASE, EXT
rem which correspond to lower case, original and upper case variations of filename.

set PYTHONPATH=C:\Prjs\nanolib;%PYTHONPATH%
echo %PYTHONPATH%
py -m scripts.ren-lambda %*
```

Examples:
For all files with extension ```.png``` or ```.PNG``` or  ```.pNg```
set the extension to ```.JPG``` 
```
ren-lambda "ext == '.png'" "Base + '.JPG'"
```
Hollow filter and action:
```
ren-lambda "1==2" "Base + Ext"
```
Example of useful filter:
```
ren-lambda "Base.startswith('IMG')" "Base + Ext"
```


