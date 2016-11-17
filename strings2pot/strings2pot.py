# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import datetime
import hashlib

from extractors import android, ios, arb

class String2PotConverter:
    POT_HEADER = """msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\\n"
"Report-Msgid-Bugs-To: EMAIL@ADDRESS\\n"
"POT-Creation-Date: %s\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: strings2pot\\n"
    """
    extractor = None

    def __init__(self, source_file, destination_file):
        # verify if source_file exists
        if not os.path.isfile(source_file):
            raise Exception("Source file %s doesn't exist" % (source_file))

        # check for source file type
        if os.path.splitext(source_file)[1] == ".xml":
            self.extractor = android.AndroidExtractor(source_file, destination_file, self._create_context_id)
        elif os.path.splitext(source_file)[1] == ".strings":
            self.extractor = ios.iOSExtractor(source_file, destination_file, self._create_context_id)
        elif os.path.splitext(source_file)[1] == ".arb":
            self.extractor = arb.ArbExtractor(source_file, destination_file, self._create_context_id)
        else:
            raise Exception("File format not recognized for source file %s" % (source_file))

        # init the POT destination file
        with open(destination_file, 'w+') as pot:
            pot.write(self.POT_HEADER %
                    (datetime.datetime.now().strftime("%Y-%m-%d %H:%M%z")))
    
    def convert(self):
        self.extractor.run()

    def _create_context_id(self, string):
        """
        Context strings will be used as string keys,
        so it is important to keep them unique from others
        """

        s = string.replace(' ', '_')  # convert spaces to underscores
        s = re.sub(r'\W', '', s)      # strip any NON-word char
        s = re.sub(r'^\d+', '', s)    # strip digits at the beginning of a string
        s = s.upper()                 # uppercase everything

        h1 = hashlib.md5(string).hexdigest()[0:5]
        h2 = hashlib.md5(string).hexdigest()[5:10]

        if len(s) > 60:
            s = s[:55]

        s = "K%s_%s_%s" % (h1, s, h2)  # on Android, keys cannot begin with digits

        return s


def _usage():
    print "Usage:", sys.argv[0], "<STRINGS_FILE> <POT_FILE>\n"


def main():
    if len(sys.argv) == 3:
        try:
            c = String2PotConverter(sys.argv[1], sys.argv[2])
            c.convert()
            print "OK"
        except Exception, e:
            print e
    else:
        _usage()


if __name__ == '__main__':
    main()
