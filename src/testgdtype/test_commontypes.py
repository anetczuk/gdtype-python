# MIT License
#
# Copyright (c) 2022 Arkadiusz Netczuk <dev.arnet@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import unittest

from gdtype.commontypes import Transform3D


#TODO: add tests for invalid input (check exceptions)
#TODO: add test for CONFIG_LIST: serialize and deserialize and compare results
#TODO: add tests inside GDScript (call python code from gdsript)


class Transform3DTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        pass

    def tearDown(self):
        ## Called after testfunction was executed
        pass

    def test_indexing_1d(self):
        raw_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        data = Transform3D( raw_data )

        self.assertEqual( data[0], 1 )
        self.assertEqual( data.get(0, 0), 1 )

        self.assertEqual( data[1], 2 )
        self.assertEqual( data.get(0, 1), 2 )

        self.assertEqual( data[2], 3 )
        self.assertEqual( data.get(0, 2), 3 )
