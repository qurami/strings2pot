# -*- coding: utf-8 -*-

import re
import json

class ArbExtractor:
    def __init__(self, source_file, destination_file, context_id_generator):
        self.source_file = source_file
        self.destination_file = destination_file
        self._create_context_id = context_id_generator
    
    def parse_string(self, string, placeholder_list):
        for placeholder in placeholder_list:
            string = string.replace("{%s}" % placeholder, '%s')
        
        s = string.replace('"', '\"')
        s = s.replace("''", "'")
        s = s.replace("\\n", "\n")

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
    
    def split_plural_string(self, plural_string, plural_placeholder, placeholders):
        split_strings = []

        pattern = r"^{"+ plural_placeholder +",plural, (?P<imploded_string>.*)}"
        prog = re.compile(pattern)

        match = prog.match(plural_string)
        if not match:
            return []

        imploded_string = match.groupdict()['imploded_string']

        for placeholder in placeholders:
            imploded_string = imploded_string.replace("{%s}" % placeholder, "_#|%s|#_" % placeholder)

        while imploded_string != '':
            entry = imploded_string[imploded_string.find('{')+1:imploded_string.find('}')]
            for placeholder in placeholders:
                entry = entry.replace("_#|%s|#_" % placeholder, "{%s}" % placeholder)
            
            split_strings.append(entry)
            imploded_string = imploded_string[imploded_string.find('}')+1:]

        return split_strings

    def run(self):
        with open(self.destination_file, 'a') as pot:
            # open the arb file and convert it to a dictionary
            # using json.load (arb is JSON in fact)
            with open(self.source_file, 'r') as source:
                source_as_dict = json.load(source)

            # parse the arb dictionary
            for key in source_as_dict:
                # keys with @ prefix hold the placeholders,
                # keys without it hold the string

                # get placeholders for current key
                placeholders = []
                if key[0] == '@':
                    for placeholder in source_as_dict[key]['placeholders']:
                        placeholders.append(placeholder)

                    # get string...
                    source_string = source_as_dict[key[1:]]

                    # check if it's a plural string
                    strings_to_parse = [source_string]

                    for placeholder in placeholders:
                        if "{%s,plural" % placeholder in source_string:
                            strings_to_parse = self.split_plural_string(source_string, placeholder, placeholders)
                            break

                    # then parse and add to pot found strings
                    for string in strings_to_parse:
                        parsed_string = self.parse_string(string, placeholders)
                        message_id = parsed_string[1:len(parsed_string)-1]

                        content = "\n#: %s:%s\nmsgctxt \"%s\"\nmsgid %s\nmsgstr \"\"\n" % (
                            self.source_file,
                            key,
                            self._create_context_id(message_id),
                            parsed_string
                        )
                        pot.write(content)
            pot.close()