# filename_processing.py
from .file_operations import batch_file_rename
from .file_operations import get_names_of_directory_items
from enum import Enum

class SubareaType(Enum):
    UNDEFINED = 0
    DIGIT = 1
    NONDIGIT = 2

def numerize_filenames_for_proper_ordering(directory, max_number_of_patterns = 999):
   """Renames filenames so that numeric part is aligned with zeros,
      and files are properly alphabetically sorted
   """
   original_filenames = get_names_of_directory_items(directory)
   new_filenames = generate_new_aligned_filenames(original_filenames, max_number_of_patterns)
   batch_file_rename(directory, original_filenames, new_filenames)

def generate_new_aligned_filenames(original_filenames, max_number_of_patterns = 999):
   """Detects numeric substrings in filenames, and leftpad with names so that
      proper ordering is guarantied
   """
   # The key is special filename PATTERN, the value - is list of filename subareas
   # Filename PATTERN - all nunnumeric chars preserved, numeric parts are replaced with char '0'
   # Example: filename 'book5section32.txt', pattern 'book0section0.txt'
   # Subareas list: nonnumeric sequences are preserved, numeric sequences are replaced with number,
   # which is the length of numeric sequence
   # Example: filename 'book5section32.txt', subareas list: ["book", 1, "section", 2, ".txt"]
   patterns_map = {}
   # During the first scan we build 'patterns_map', and for every subareas we calculate maximum numeric widths
   for filename in original_filenames:
      (current_pattern, current_subareas) = parse_filename(filename)
      subareas = patterns_map.get(current_pattern)
      if subareas is None:
         patterns_map[current_pattern] = current_subareas       # new pattern
      else:
         for index, subarea2 in enumerate(current_subareas):
            subarea1 = subareas[index]          # subareas may be updated in this loop
            if isinstance(subarea1, str):
               if subarea1 != subarea2:
                  raise ValueError(f"Something wrong: {subarea1} != {subarea2} !")
            elif isinstance(subarea1, int):
               if not isinstance(subarea2, int):
                  raise ValueError(f"Something wrong: type of {subarea2} must be int !")
               if subarea1 < subarea2:
                  subareas[index] = subarea2    # the length of numerical subarea
            else:
               raise ValueError(f"Something wrong: unexpected type of {subarea1}:  {type(subarea1)} !")
#   print(f"\nfilename processed: {filename}, and patterns_map is:")

   print("")
   for (key, val) in patterns_map.items():
      print(f"key={key}, val={val}")
   if len(patterns_map) > max_number_of_patterns:
      raise ValueError(f"Too many different file patterns, max {max_number_of_patterns} allowed")

   new_filenames = []
   #During the second scan we use subareas info and append 0s to lengthen numeric fields if necessary
   for filename in original_filenames:
      char_index = 0
      new_filename = ""
      (current_pattern, current_subareas) = parse_filename(filename)
      subareas = patterns_map.get(current_pattern)
      for subarea1, subarea2 in zip(subareas, current_subareas):
         if isinstance(subarea1, str):
            new_filename += subarea1
            char_index += len(subarea1)
         elif isinstance(subarea1, int):
            zeros = '0' * (subarea1 - subarea2)
            new_filename += zeros
            while subarea2 > 0:
               new_filename += filename[char_index]
               char_index += 1
               subarea2 -= 1
         else:
            raise ValueError(f"Something wrong: unexpected type of {subarea1}:  {type(subarea1)} !")
      new_filenames.append(new_filename)
   return new_filenames


def parse_filename(filename):
   pattern = ""
   subareas = []
   subarea_type = SubareaType.UNDEFINED

   for chr in filename:
      chr_type = type_of_character(chr)
      if subarea_type != chr_type:
         subarea_type = chr_type
         if chr_type == SubareaType.DIGIT:
            pattern += '0'
            subareas.append(1)
         else:
            pattern += chr
            subareas.append(chr)
      else:
         if chr_type == SubareaType.DIGIT:
            subareas[-1] += 1
         else:
            pattern += chr
            subareas[-1] += chr
#      print(f"chr={chr}, pattern={pattern}, subareas={subareas}")
   return (pattern, subareas)

def type_of_character(char):
   if char.isdigit():
      return SubareaType.DIGIT
   else:
      return SubareaType.NONDIGIT

def main(args):
#   if len(args) == 2:		# kind of test mode
#      (pattern, subareas) = parse_filename(args[1])
#      print(f"parse_filename() returns ({pattern}, {subareas})")
   if len(args) == 2:
      numerize_filenames_for_proper_ordering(args[1])
   elif len(args) == 1:
      numerize_filenames_for_proper_ordering(".")
   else:
      print("Proper command line: numerize_filenames_for_proper_ordering [directory]")
#   old_names = [args[1], args[3]]
#   new_names = [args[2], args[4]]
#   batch_file_rename(".", old_names, new_names)

if __name__ == '__main__':
   import sys
   main(sys.argv)
