#!/usr/bin/python

import fileinput
import re



def parse_stdin():
    for line in fileinput.input():
        pass

class LineSource:
    def get_line(self):
        return None

class ListLineSource(LineSource):

    def __init__(self, lines):
        self.lines = lines
        self.index = 0

    def get_line(self):
        if self.index >= len(self.lines):
            return None
        else:
            returnvalue = self.lines[self.index]
            self.index = self.index + 1
            return returnvalue

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
        indent_stack = []
        result_stack = []
        tag_stack = []
        dangling_tag = None
        current_indent_level = 0
        line = line_source.get_line()
        while line:
            (line_indent_level, payload) = self.split(line)

            if (line_indent_level > current_indent_level):
                print "Case 2, increasing indent level"
                if not dangling_tag:
                    raise RuntimeError("No dangling tag available when increasing indent!")
                indent_stack.append(current_indent_level)
                tag_stack.append(dangling_tag)
                result_stack.append(result)
                current_indent_level = line_indent_level
                result = {}

            elif (line_indent_level < current_indent_level):
                print "case 3"
                while (line_indent_level < current_indent_level):
                    print "line_indent_level =", line_indent_level
                    print "current_indent_level =", current_indent_level
                    current_indent_level = indent_stack.pop()
                    dangling_tag = tag_stack.pop()
                    higher_result = result_stack.pop()
                    higher_result[dangling_tag] = result
                    result = higher_result

                if (line_indent_level != current_idnent_level):
                    raise RuntimeError("Dude,line_indent_level != current_idnent_level!")

            print "case 1"
            (tag, content) = self.parse_line_content(payload)
            print "  tag = ", tag
            print "  content = ", content
            if content:
                result[tag] = content
                dangling_tag = None
            else:
                dangling_tag = tag
                print "setting dangling tag to ", dangling_tag
                
            line = line_source.get_line()

            print "case 4, unwinding indent levels to top"
            print "  Pre: line_indent_level =", line_indent_level
            print "  Pre: current_indent_level =", current_indent_level
            print "  pre: Indent level stack =", indent_stack

            while (indent_stack):
                print "line_indent_level =", line_indent_level
                print "current_indent_level =", current_indent_level
                print "result =", result
                current_indent_level = indent_stack.pop()
                dangling_tag = tag_stack.pop()
                higher_result = result_stack.pop()
                print "higher_result =", higher_result
                higher_result[dangling_tag] = result
                result = higher_result

            print "  Post: line_indent_level =", line_indent_level
            print "  Post: current_indent_level =", current_indent_level
            print "  Post: Indent level stack =", indent_stack

                
            if (current_indent_level != 0):
                raise RuntimeError("Dude, top indent level is not zero, it's " + str(line_indent_level) + ", result is :" + str(result))

        return result
