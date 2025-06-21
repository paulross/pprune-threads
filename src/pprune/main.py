"""MIT License

Copyright (c) 2017 Paul Ross https://github.com/paulross

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = 'Paul Ross'
__date__ = '2017-01-01'
__version__ = '0.0.1'
__rights__ = 'Copyright (c) 2017 Paul Ross'

import argparse
import logging
import os
import sys
import time

import pprune
import write_html
from pprune.common import read_html
from pprune.common import thread_struct
from pprune.common import log_config
import publication_maps

def common_words_file():
    return os.path.normpath(os.path.join(os.path.dirname(__file__), 'count_1w.txt'))


def main():
    parser = argparse.ArgumentParser(description='Perform research on a pprune thread to local storage.')
    parser.add_argument(
        'archives',
        type=str,
        nargs='+',
        help=(
            'Archive directory of the thread.'
            ' Multiple threads will be added in order.'
        )
    )
    parser.add_argument(
        '--thread',
        type=str,
        help=(
            'This decides the thread publication map..'
        )
    )
    parser.add_argument(
        "--common-words",
        type=int,
        default=1000,
        help="Number of common words to exclude. [default: %(default)d]",
    )
    parser.add_argument(
        "--authors",
        action="store_true",
        help=(
            "Add posts by author. "
        )
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="log_level",
        type=int,
        default=20,
        help="Log level. [default: %(default)d]",
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=args.log_level,
        format=log_config.DEFAULT_OPT_LOG_FORMAT_NO_PROCESS,
        stream=sys.stdout,
    )

    t_start = time.perf_counter()
    thread = thread_struct.Thread()
    for archive in args.archives:
        pprune.common.read_html.update_whole_thread(archive, thread)
    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    print('Number of words: {:d}'.format(word_count))
    common_words = read_html.read_common_words(common_words_file(), args.common_words)
    # write_html.pass_one(thread, common_words)
    if args.thread == 'Concorde'
        write_html.write_whole_thread(thread, common_words, publication_maps.ConcordePublicationMap())
    elif args.thread == 'AI171':
        write_html.write_whole_thread(thread, common_words, publication_maps.AirIndia171())
    else:
        print(f'Do not know thread {args.thread}')
        return -1
    t_elapsed = time.perf_counter() - t_start
    print('Processed %d posts in %.3f (s)', len(thread), t_elapsed, )
    print('Bye, bye!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
