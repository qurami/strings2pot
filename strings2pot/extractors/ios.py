# -*- coding: utf-8 -*-

import re

class iOSExtractor:
    def __init__(self, source_file, destination_file, context_id_generator):
        self.source_file = source_file
        self.destination_file = destination_file
        self._create_context_id = context_id_generator
    
    def parse_string(self, string):
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
    
    def run(self):
        pattern = r"\"(?P<msgid>.*)\" = \"(?P<msgstr>.*)\";"
        prog = re.compile(pattern)

        with open(self.destination_file, 'a') as pot:
            with open(self.source_file, 'r') as source:
                counter = 0

                for l in source:
                    counter += 1
                    match = prog.match(l)

                    if match:
                        result = match.groupdict()

                        parsed_string = self.parse_string(result['msgid'])
                        message_id = parsed_string[1:len(parsed_string)-1]

                        content = "\n#: %s:%d\nmsgctxt \"%s\"\nmsgid %s\nmsgstr \"\"\n" % (
                            self.source_file,
                            counter,
                            self._create_context_id(message_id),
                            parsed_string )
                        pot.write(content)
                source.close()
            pot.close()