#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    Test parsing of output from imagemagick up to and including invoking
    imagemagick on an actual file.

    :copyright: (c) 2014 by Bjørn Remseth
    :license: All rights reserved (at least for now)
"""

import os
import unittest
import json
from  imagemagic_identify_output_parser import Parser, LineSource


class SimpleCrudCases(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def tearDown(self):
        pass

    def test_empty_string(self):
        rv = self.parser.get_indentation_of_line('')
        self.assertEqual(0, rv)

    def test_string_with_no_leading_spaces(self):
        rv = self.parser.get_indentation_of_line('xxx')
        self.assertEqual(0, rv)

    def test_string_with_one_leading_space(self):
        rv = self.parser.get_indentation_of_line(' ')
        self.assertEqual(1, rv)

    def test_string_with_one_leading_space_followed_by_something(self):
        rv = self.parser.get_indentation_of_line(' xxx')
        self.assertEqual(1, rv)

    def test_split_empty(self):
        idx, txt = self.parser.split('')
        self.assertEqual(0, idx)
        self.assertEqual('', txt)


    def test_split_leading_single_space(self):
        idx, txt = self.parser.split(' ')
        self.assertEqual(1, idx)
        self.assertEqual('', txt)

    def test_split_leading_single_space_followed_by_an_a(self):
        idx, txt = self.parser.split(' a')
        self.assertEqual(1, idx)
        self.assertEqual('a', txt)


    def test_parse_line_content_min(self):
        r = self.parser.parse_line_content("min: 0 (0)")
        self.assertEqual({"min": "0 (0)"}, r)


    def test_parse_line_content_min(self):
        tag, content = self.parser.parse_line_content("min: 0 (0)")

        self.assertEqual("min", tag)
        self.assertEqual("0 (0)", content)

    def test_parse_line_content_properties(self):
        tag, content = self.parser.parse_line_content("Properties:")
        self.assertEqual("Properties", tag)
        self.assertEqual(None, content)

    def test_parse_empty_lines(self):
        # An empty line source
        ls = LineSource()
        result = self.parser.parse_lines(ls)
        self.assertEqual({}, result)


if __name__ == '__main__':
    unittest.main()
