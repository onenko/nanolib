# file_operations.py
import os

def batch_file_rename(directory, original_filenames, new_filenames):
   """Assuming that both filenames lists have equal length, renames files one by one on disk.
      directory - location of the file, without trailing slash
      original_filenames - the list of names of existing, not locked files in 'directory'
      new_filenames - list of the same size and order as 'original_filename'
   """
   for index, filename in enumerate(original_filenames):
      old_full_name = directory + '/' + filename
      new_full_name = directory + '/' + new_filenames[index]
      if old_full_name != new_full_name:
         try:
            os.rename(old_full_name, new_full_name)
            print(f"File '{old_full_name}' has been successfully renamed to '{new_full_name}'.")
         except FileNotFoundError:
            print(f"Error: File '{old_full_name}' not found.")
         except Exception as e:
            print(f"An error occurred: {e}")

def get_names_of_directory_items(directory):
   items = os.listdir(directory)
   return [item for item in items if not item.startswith('.')]

def main(args):
   if len(args) == 5:
      print("file_operations.py: to run test, one need to have 2 test files in current directory!")
      old_names = [args[1], args[3]]
      new_names = [args[2], args[4]]
      batch_file_rename(".", old_names, new_names)
   else:
      curr_dir_list = get_names_of_directory_items(".")
#      for dir_item in curr_dir_list:
#         print(dir_item)

if __name__ == '__main__':
   import sys
   main(sys.argv)
