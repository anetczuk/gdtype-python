#!/usr/bin/python3
#
# MIT License
#
# Copyright (c) 2020 Arkadiusz Netczuk <dev.arnet@gmail.com>
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


import sys
import time
import logging
import argparse
import cProfile

import sys
import os

#### append source root
sys.path.append(os.path.abspath( os.path.join(os.path.dirname(__file__), "../src") ))


from worklog.main import create_parser, main


_LOGGER = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Application Profiler')
#parser.add_argument('--profile', action='store_const', const=True, default=True, help='Profile the code' )
parser.add_argument('--pfile', action='store', default=None, help='Profile the code and output data to file' )

create_parser( parser )

args = parser.parse_args()


starttime = time.time()
profiler = None

exitCode = 1

try:
    profiler_outfile = args.pfile

    _LOGGER.info( "Starting profiler" )
    profiler = cProfile.Profile()
    profiler.enable()

    exitCode = main( args )

except BaseException:
    exitCode = 1
    _LOGGER.exception("Exception occurred")
    raise

finally:
    _LOGGER.info( "" )                    ## print new line

    profiler.disable()
    if profiler_outfile is None:
        _LOGGER.info( "Generating profiler data" )
        profiler.print_stats(1)
    else:
        _LOGGER.info( "Storing profiler data to %s", profiler_outfile )
        profiler.dump_stats( profiler_outfile )
        _LOGGER.info( "to view output file run: pyprof2calltree -k -i %s", profiler_outfile )
        _LOGGER.info( "if missing then pyprof2calltree can be installed by: pip3 install --user pyprof2calltree" )

    timeDiff = (time.time() - starttime) * 1000.0
    _LOGGER.info( "Calculation time: {:13.8f}ms".format(timeDiff) )

    sys.exit(exitCode)
