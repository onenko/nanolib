import os
import subprocess

### Script to rename files in current directory
###
### Files with extension 'ext' in current directory are processed.
### new_name(old) generate new name for the file.
### It is assumed that rules of renaming are coded every time in new_name() function.


### Defines the rules to rename a file, 'old' is simple file name with extension
def new_name(old):
  file_base_name, file_extension = os.path.splitext(old)
#  prefix = file_base_name[:1]
  prefix = file_base_name[6:]
  return prefix + file_extension


### This function does the files enumeration and renaming
### Normally you do not need to change it
def process_current_folder(ext):
   print(f"\nrenamer.py\t\t Procession files with extension .{ext}")
   ext = ext.lower()
   dir = os.getcwd()
   for child in os.listdir(dir):
      print("child:" + child)
      child_path = dir + '\\' + child;
      if not os.path.isdir(child_path) and child.lower().endswith(ext):
         new_nam = new_name(child)
         print(f"Renaming {child} to {new_nam}")
         new_full_name = dir + '\\' + new_nam
         try:
            os.rename(child_path, new_full_name)
         except FileNotFoundError:
            print(f"Error: File '{child_path}' not found.")
         except Exception as e:
            print(f"An error occurred: {e}")


def main(args):
   ''' script works in the current directory
       single argument - extension without dot
       rename logic is defined in new_name(old_name) function
   '''
   process_current_folder(args[1])

if __name__ == '__main__':
   import sys
   main(sys.argv)
