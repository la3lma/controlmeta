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
from  imagemagic_identify_output_parser import Parser, LineSource, ListLineSource, FileLineSource


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

    def test_parse_single_line(self):
        ls = ListLineSource(["a: b"])
        result = self.parser.parse_lines(ls)
        self.assertEqual({"a":"b"}, result)

    def test_parse_two_lines_same_indentation_level(self):
        ls = ListLineSource(["a: b", "c: d"])
        result = self.parser.parse_lines(ls)
        self.assertEqual({"a":"b", "c": "d"}, result)

    def test_parse_two_lines_different_indent_levels(self):
        ls = ListLineSource(["f:", "  g: h"])
        result = self.parser.parse_lines(ls)
        self.assertEqual({"f":{"g": "h"}}, result)

    def test_parsing_channel_statistics(self):
        stats = ["Channel statistics:",
                 "  Red:",
                 "    min: 3 (0.0117647)",
                  "    max: 255 (1)",
                  "    mean: 136.073 (0.53362)",
                  "    standard deviation: 51.494 (0.201937)",
                  "    kurtosis: -0.782758",
                  "    skewness: -0.169742",
                  "  Green:",
                  "    min: 0 (0)",
                  "    max: 232 (0.909804)",
                  "    mean: 82.3407 (0.322905)",
                  "    standard deviation: 37.9124 (0.148676)",
                  "    kurtosis: 0.140211",
                  "    skewness: 0.553692",
                  "  Blue:",
                  "    min: 0 (0)",
                  "    max: 220 (0.862745)",
                  "    mean: 68.011 (0.26671)",
                  "    standard deviation: 31.4847 (0.123469)",
                  "    kurtosis: 1.43816",
                  "    skewness: 1.0309"
                 ]
        stats_as_dictionary =  \
        {'Channel statistics': 
         {'Blue': 
          {'skewness': '1.0309', 
           'min': '0 (0)', 
           'max': '220 (0.862745)', 
           'standard deviation': '31.4847 (0.123469)', 
           'kurtosis': '1.43816', 
           'mean': '68.011 (0.26671)'}, 
          'Green': {'skewness': '0.553692', 
                    'min': '0 (0)', 
                    'max': '232 (0.909804)', 
                    'standard deviation': '37.9124 (0.148676)', 
                    'kurtosis': '0.140211', 
                    'mean': '82.3407 (0.322905)'}, 
          'Red': {'skewness': '-0.169742', 
                  'min': '3 (0.0117647)', 
                  'max': '255 (1)', 
                  'standard deviation': '51.494 (0.201937)', 
                  'kurtosis': '-0.782758', 
                  'mean': '136.073 (0.53362)'}
          }
         }

        ls = ListLineSource(stats)
        result = self.parser.parse_lines(ls)
        self.assertEqual(stats_as_dictionary, result)

    def test_parsing_image_doc(self):
        image_doc = ["Image: tests/images/lena1.jpeg",
                     "  Format: JPEG (Joint Photographic Experts Group JFIF format)"]
        # We expect the original attribute of "Image:" to be replaced by what's in the
        # sub parts.  That's not  awfully nice, but in practice, for images from
        # imagemagic, it's ok.
        parsed_image = {'Image': {'Format': 'JPEG (Joint Photographic Experts Group JFIF format)'}}

        ls = ListLineSource(image_doc)

        result = self.parser.parse_lines(ls)
        self.assertEqual(parsed_image, result)

##
## TODO
##

    def test_parsing_imagemagic_output_from_static_file(self):
        ls = FileLineSource("tests/imagemagick-identify-output.txt")
        result = self.parser.parse_lines(ls)
        print "Result = ", result

    def test_parsing_imagemagic_output_from_running_process(self):
        pass



if __name__ == '__main__':
    unittest.main()
