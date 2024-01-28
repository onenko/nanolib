import os
import subprocess
import sys

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
def process_current_folder(filter, rename):
   dir = os.getcwd()
   filter_lambda = eval(f"lambda base, ext, Base, Ext, BASE, EXT: {filter}")
   rename_lambda = eval(f"lambda base, ext, Base, Ext, BASE, EXT: {rename}")

   print(f"\nren-lambda.py\t\t Procession files with filter expr '{filter}' and rename expr '{rename}''")
   for child in os.listdir(dir):
      print("child:" + child)
      child_path = dir + '\\' + child
      if not os.path.isdir(child_path):
         Base, Ext = os.path.splitext(child)
         base = Base.lower()
         ext = Ext.lower()
         BASE = Base.upper()
         EXT = Ext.upper()
         if filter_lambda(base, ext, Base, Ext, BASE, EXT):
            new_name = rename_lambda(base, ext, Base, Ext, BASE, EXT)
            print(f"Renaming {child} to {new_name}")
            new_full_name = dir + '\\' + new_name
            try:
               os.rename(child_path, new_full_name)
            except FileNotFoundError:
               print(f"Error: File '{child_path}' not found.")
            except Exception as e:
               print(f"An error occurred: {e}")
         else:
            print(f"Ignoring {child}")

if __name__ == '__main__':
   ''' script works in the current directory
      first argument - lambda expression to select files that should be renamed
      second argument - lambda expression that generates new file name from old filename's base and ext
   '''
   if len(sys.argv) != 3:
      print("Usage: python ren-lambda.py \"filter-expression\" \"new-name-expression\"")
      print("\tor from Windows command line:")
      print("ren-lambda.bat \"filter-expression\" \"new-name-expression\"")
   else:
      process_current_folder(sys.argv[1], sys.argv[2])
