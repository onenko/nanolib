import os
import subprocess

from nano_file_utils.filename_processing import numerize_filenames_for_proper_ordering

global folders

### Having a directory with subdirectories with JPG files,
### the script goes through directory tree, and every subdirectory, that:
### -- does not contain another subdirectories;
### -- contains only JPG files of single pattern (with changed number part)
### will be converted into CBR file, the name the same as directory name.
### JPG files within original subdirectory and subdirectory itself are deleted.

def process_folder(full_folder, folder_name):
   print(f"=== {folder_name} ===\n")
   jpg_count = 0
   nojpg_count = 0	# subdirs and non-jpg files
   for child in os.listdir(full_folder):
      print("child:" + child)
      child_path = full_folder + '\\' + child;
      if os.path.isdir(child_path):
         nojpg_count += 1
         try: 
            if process_folder(child_path, child) == 0:	# convert it to CBR
               # First normalize filenames for proper ordering
               numerize_filenames_for_proper_ordering(child_path, max_number_of_patterns = 1)
               # Run RAR command
               subprocess.call([r'C:\SRV\cbra.bat', child_path])
               # Finally delete this directory as it should be empty
               # add later
         except Exception as e:
            print(f"Exeption to process the folder: {child_path}, exc: {e}")
      elif child.lower().endswith(".jpg") or child.lower().endswith(".jpeg"):
         jpg_count += 1
      else:
         nojpg_count += 1
   return nojpg_count



def main(args):
   current_folder = os.getcwd()
   process_folder(current_folder, current_folder)

if __name__ == '__main__':
   import sys
   main(sys.argv)
