# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import datetime
import hashlib
import xml.etree.ElementTree as ET

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


def _usage():
    print "Usage:", sys.argv[0], "<STRINGS_FILE> <POT_FILE>\n"


def _init_pot(potFilePath):
    try:
        with open(potFilePath, 'w+') as pot:
            pot.write(POT_HEADER %
                      (datetime.datetime.now().strftime("%Y-%m-%d %H:%M%z")))
    except Exception, e:
        return False

    return True


def _create_context_id(string):
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


def _parse_string_for_android(string):
    s = string.replace("\\'", "'")
    s = s.replace("\"", "\\\"")
    s = s.replace("\\n", "\n")
    s = re.sub(r'%\d\$s', '%s', s)
    s = re.sub(r'%\d\$d', '%d', s)

    if "\n" in s:
        s = s.replace("\n", "\\n\n")
        parts = s.split("\n")
        new_parts = ["\"\""]
        for line in parts:
            new_parts.append("\"%s\"" % line)

        s = "\n".join(new_parts)
    else:
        s = "\"%s\"" % s
    return s


def _parse_string_for_apple(string):
    s = string.replace("\\'", "'")
    s = s.replace("\\n", "\n")
    s = s.replace('%@', '%s')

    if "\n" in s:
        s = s.replace("\n", "\\n\n")
        parts = s.split("\n")
        new_parts = ["\"\""]
        for line in parts:
            new_parts.append("\"%s\"" % line)

        s = "\n".join(new_parts)
    else:
        s = "\"%s\"" % s
    return s


def extract_for_android(sourceFile, destinationFile):
    if not _init_pot(destinationFile):
        return False, "Unable to initialize destination file"

    with open(destinationFile, 'a') as pot:
        root = ET.parse(sourceFile)
        counter = 3

        for el in root.findall('./string'):
            parsed_string = _parse_string_for_android(el.text)
            message_id = parsed_string[1:len(parsed_string)-1]

            counter += 1
            content = "\n#: %s:%d\nmsgctxt \"%s\"\nmsgid %s\nmsgstr \"\"\n" % (
                sourceFile,
                counter,
                el.attrib.get('name', _create_context_id(message_id)),
                parsed_string )
            pot.write(content)

    return True, "OK"


def extract_for_apple(sourceFile, destinationFile):
    if not _init_pot(destinationFile):
        return False, "Unable to initialize destination file"

    pattern = r"\"(?P<msgid>.*)\" = \"(?P<msgstr>.*)\";"
    prog = re.compile(pattern)

    with open(destinationFile, 'a') as pot:
        with open(sourceFile, 'r') as source:
            counter = 0

            for l in source:
                counter += 1
                match = prog.match(l)

                if match:
                    result = match.groupdict()

                    parsed_string = _parse_string_for_apple(result['msgid'])
                    message_id = parsed_string[1:len(parsed_string)-1]

                    content = "\n#: %s:%d\nmsgctxt \"%s\"\nmsgid %s\nmsgstr \"\"\n" % (
                        sourceFile,
                        counter,
                        _create_context_id(message_id),
                        parsed_string )
                    pot.write(content)

    return True, "OK"


def run(sourceFile, destinationFile):
    if not os.path.isfile(sourceFile):
        return False, "Source file %s doesn't exist\n" % (sourceFile)

    if os.path.splitext(sourceFile)[1] == ".xml":
        return extract_for_android(sourceFile, destinationFile)
    elif os.path.splitext(sourceFile)[1] == ".strings":
        return extract_for_apple(sourceFile, destinationFile)
    else:
        return False, "File format not recognized for source file %s\n" % (sourceFile)


def main():
    if len(sys.argv) == 3:
        output, message = run(sys.argv[1], sys.argv[2])
        print message
    else:
        _usage()


if __name__ == '__main__':
    main()
