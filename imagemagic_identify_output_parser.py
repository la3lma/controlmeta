#!/usr/bin/python

import fileinput
import re



def parse_stdin():
    for line in fileinput.input():
        pass

class LineSource:
    def get_line(self):
        return None

class Parser:


    def get_indentation_of_line(self, txt):
        m = re.match('^\s+', txt)
        if not m:
            return 0
        else:
            return len(m.group())

    def split(self, txt):
        index = self.get_indentation_of_line(txt)
        return (index, txt[index:])


    def parse_line_content(self, line):
       "Parse the line, add to indentation if necessary"
       m = re.match('^.+: ', line)
       if m:
           index = len(m.group())
           tag = line[:index - 2]
           content = line[index:]
           return tag, content
       m = re.match('^.+:', line)
       index = len(m.group())
       tag = line[:index - 1]
       return tag, None

    def parse_lines(self, line_source):
        result = {}
        line = line_source.get_line()
        if not line:
            return result
        return None
        




        
