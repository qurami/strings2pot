# -*- coding: utf-8 -*-

import os
import unittest
import ios

class iOSExtractorTest(unittest.TestCase):
    def setUp(self):
        self.mock_source_file = 'mock_source_ios.strings'
        self.mock_destination_file = 'mock_destination_ios.pot'
        def mock_context_id_generator(s): return 'MOCK_CONTEXT_ID'
        self.mock_context_id_generator = mock_context_id_generator

        with open(self.mock_source_file, 'a') as source_file:
            source_file.write("""
/* Test string with a placeholder */

"Test string with a \"%@\" here" = "Test string with a \"%@\" here";
            """)
    
    def tearDown(self):
        try:
            os.unlink(self.mock_source_file)
            os.unlink(self.mock_destination_file)
        except Exception, e:
            pass

    # test that the iOSExtractor class constructor sets source_file and destination_file attributes
    def test_ctor(self):
        sut = ios.iOSExtractor(
            self.mock_source_file,
            self.mock_destination_file,
            self.mock_context_id_generator
        )

        self.assertEqual(sut.source_file, self.mock_source_file)
        self.assertEqual(sut.destination_file, self.mock_destination_file)
    
    # test that iOSExtractor parse_string method converts string in POT format 
    def test_parse_string(self):
        sut = ios.iOSExtractor('', '', self.mock_context_id_generator)

        single_line_string = "\' \" %@"
        self.assertEqual(
            sut.parse_string(single_line_string),
            '"\' \" %s"'
        )

        multi_line_string = "\' \" \\n %@"
        self.assertEqual(
            sut.parse_string(multi_line_string),
            '''""
"\' \" \\n"
" %s"'''
        )
    
    # test that iOSExtractor run method converts an input file in POT format
    def test_run(self):
        sut = ios.iOSExtractor(
            self.mock_source_file,
            self.mock_destination_file,
            self.mock_context_id_generator
        )

        sut.run()

        with open(self.mock_destination_file, 'r') as destination_file:
            lines = destination_file.readlines()
            pot_content_as_string = "".join(lines)

            self.assertEqual(
                pot_content_as_string,
                '''
#: mock_source_ios.strings:4
msgctxt "MOCK_CONTEXT_ID"
msgid "Test string with a \"%s\" here"
msgstr ""
'''
            )

if __name__ == '__main__':
    unittest.main()