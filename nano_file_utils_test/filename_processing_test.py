import unittest
from ..nano_file_utils.filename_processing import generate_new_aligned_filenames

class TestFilename_processingFunctions(unittest.TestCase):

    def test_generate_new_aligned_filenames(self):
        old_filenames = ["abc1.txt", "abc2.txt", "abc10.txt", "abc11.txt"]
        new_filenames = generate_new_aligned_filenames(old_filenames)
        self.assertEqual(len(new_filenames), len(old_filenames))
        self.assertEqual(new_filenames[0], "abc01.txt")
        self.assertEqual(new_filenames[1], "abc02.txt")
        self.assertEqual(new_filenames[2], "abc10.txt")
        self.assertEqual(new_filenames[3], "abc11.txt")

    def test_generate_new_aligned_filenames_2patterns(self):
        old_filenames = ["abc1.txt", "abc2.txt", "abc10.txt", "abc11.txt", "abc1X1.txt", "abc2X1.txt", "abc10X1.txt", "abc11X1.txt"]
        new_filenames = generate_new_aligned_filenames(old_filenames)
        self.assertEqual(len(new_filenames), len(old_filenames))
        self.assertEqual(new_filenames[0], "abc01.txt")
        self.assertEqual(new_filenames[1], "abc02.txt")
        self.assertEqual(new_filenames[2], "abc10.txt")
        self.assertEqual(new_filenames[3], "abc11.txt")
        self.assertEqual(new_filenames[4], "abc01X1.txt")
        self.assertEqual(new_filenames[5], "abc02X1.txt")
        self.assertEqual(new_filenames[6], "abc10X1.txt")
        self.assertEqual(new_filenames[7], "abc11X1.txt")

    def test_generate_new_aligned_filenames_2patterns_1permitted(self):
        old_filenames = ["abc1.txt", "abc2.txt", "abc10.txt", "abc11.txt", "abc1X1.txt", "abc2X1.txt", "abc10X1.txt", "abc11X1.txt"]
        with self.assertRaises(ValueError) as context:
           new_filenames = generate_new_aligned_filenames(old_filenames, max_number_of_patterns = 1)
        self.assertEqual(str(context.exception), "Too many different file patterns, max 1 allowed")

if __name__ == '__main__':
    unittest.main()
