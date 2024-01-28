set PYTHONPATH=C:\Prjs\nanolib;%PYTHONPATH%
echo %PYTHONPATH%
set "CURRENT_DIR=%CD%"
cd ..\..
py -m unittest nanolib.nano_file_utils_test.filename_processing_test 
cd /d "%CURRENT_DIR%"
