import unittest

# TODO

class testCases(unittest.TestCase):

    # occures when YouTube Title is converted to windows format, so converter recives previous title of video, not converted one
    # so name of Mp3 file is different than converter searching
    def giveConverterWrongFilename(self):
        link = "https://www.youtube.com/watch?v=uTBDGoJIPOo"
        test_path = ""
        self.assertEqual(True, False)  # add assertion here

# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()
