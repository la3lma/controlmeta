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
from  imagemagic_identify_output_parser import Parser, LineSource, ListLineSource, NamedFileLineSource, ImagemagickIdentifyOutput


class SimpleCrudCases(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.full_file_expected_result = \
            { "Image" : 
              { "Artifacts" : { "filename" : "tests/images/lena1.jpeg",
                                "verbose" : "true"
                                },
                "Background color" : "white",
                "Border color" : "srgb(223,223,223)",
                "Channel depth" : { "blue" : "8-bit",
                                    "green" : "8-bit",
                                    "red" : "8-bit"
                                    },
                "Channel statistics" : { "Blue" : { "kurtosis" : "1.43816",
                                                    "max" : "220 (0.862745)",
                                                    "mean" : "68.011 (0.26671)",
                                                    "min" : "0 (0)",
                                                    "skewness" : "1.0309",
                                                    "standard deviation" : "31.4847 (0.123469)"
                                                    },
                                         "Green" : { "kurtosis" : "0.140211",
                                                     "max" : "232 (0.909804)",
                                                     "mean" : "82.3407 (0.322905)",
                                                     "min" : "0 (0)",
                                                     "skewness" : "0.553692",
                                                     "standard deviation" : "37.9124 (0.148676)"
                                                     },
                                         "Red" : { "kurtosis" : "-0.782758",
                                                   "max" : "255 (1)",
                                                   "mean" : "136.073 (0.53362)",
                                                   "min" : "3 (0.0117647)",
                                                   "skewness" : "-0.169742",
                                                   "standard deviation" : "51.494 (0.201937)"
                                                   }
                                         },
                "Chromaticity" : { "blue primary" : "(0.15,0.06)",
                                   "green primary" : "(0.3,0.6)",
                                   "red primary" : "(0.64,0.33)",
                                   "white point" : "(0.3127,0.329)"
                                   },
                "Class" : "DirectClass",
                "Colorspace" : "sRGB",
                "Compose" : "Over",
                "Compression" : "JPEG",
                "Depth" : "8-bit",
                "Dispose" : "Undefined",
                "Elapsed time" : "0:01.009",
                "Endianess" : "Undefined",
                "Filesize" : "7.99KB",
                "Format" : "JPEG (Joint Photographic Experts Group JFIF format)",
                "Gamma" : "0.454545",
                "Geometry" : "300x168+0+0",
                "Image statistics" : { "Overall" : { "kurtosis" : "3.16837",
                                                     "max" : "255 (1)",
                                                     "mean" : "95.4749 (0.374411)",
                                                     "min" : "0 (0)",
                                                     "skewness" : "1.28073",
                                                     "standard deviation" : "41.1512 (0.161377)"
                                                     } },
                "Intensity" : "Undefined",
                "Interlace" : "None",
                "Iterations" : "0",
                "Matte color" : "grey74",
                "Mime type" : "image/jpeg",
                "Number pixels" : "50.4K",
                "Orientation" : "Undefined",
                "Page geometry" : "300x168+0+0",
                "Pixels per second" : "5.04MB",
                "Properties" : { "date:create" : "2014-05-27T22:32:43+02:00",
                                 "date:modify" : "2014-05-27T22:32:43+02:00",
                                 "jpeg:colorspace" : "2",
                                 "jpeg:sampling-factor" : "2x2,1x1,1x1",
                                 "signature" : "2596eb6ff77d0f1906f1923d0b7c98a352227fff88eab4cbb523dc26622d6e7f"
                                 },
                "Quality" : "74",
                "Rendering intent" : "Perceptual",
                "Tainted" : "False",
                "Transparent color" : "black",
                "Type" : "TrueColor",
                "Units" : "Undefined",
                "User time" : "0.000u",
                "Version" : "ImageMagick 6.8.8-9 Q16 x86_64 2014-03-23 http://www.imagemagick.org"
                } 
              }

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


    def test_parsing_imagemagic_output_from_static_file(self):
        ls = NamedFileLineSource("tests/imagemagick-identify-output.txt")
        result = self.parser.parse_lines(ls)
        self.assertEqual(self.full_file_expected_result, result)


##
## TODO
##


    def test_parsing_imagemagic_output_from_running_process(self):
        ls = ImagemagickIdentifyOutput("tests/images/lena1.jpeg")
        result = self.parser.parse_lines(ls)
        self.assertEqual(self.full_file_expected_result, result)



if __name__ == '__main__':
    unittest.main()
