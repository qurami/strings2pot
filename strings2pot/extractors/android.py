# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET

class AndroidExtractor:
    def __init__(self, source_file, destination_file, context_id_generator):
        self.source_file = source_file
        self.destination_file = destination_file
        self._create_context_id = context_id_generator
    
    def parse_string(self, string):
        s = string.replace("\\'", "'")
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
    
    def run(self):
        with open(self.destination_file, 'a') as pot:
            root = ET.parse(self.source_file)
            counter = 2

            for el in root.findall('./string'):
                parsed_string = self.parse_string(el.text)
                message_id = parsed_string[1:len(parsed_string)-1]

                counter += 1
                content = "\n#: %s:%d\nmsgctxt \"%s\"\nmsgid %s\nmsgstr \"\"\n" % (
                    self.source_file,
                    counter,
                    self._create_context_id(message_id), # was el.attrib.get('name')
                    parsed_string )
                pot.write(content)