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

from pprune import publication_maps
from pprune import write_html
from pprune.common import log_config
from pprune.common import read_html
from pprune.common import thread_struct
from pprune.common import words

logger = logging.getLogger(__file__)


def main():
    parser = argparse.ArgumentParser(description='Rewrite a pprune thread to local storage.')
    parser.add_argument(
        'archives',
        type=str,
        nargs='+',
        help=(
            'Archive directory of the thread.'
            ' Multiple threads will be added in order.'
        )
    )
    # TODO: Default to docs/gh-pages/thread-name
    parser.add_argument(
        'output',
        type=str,
        help=(
            'Directory to write the output to.'
            ' [default: %(default)s].'
        )
    )
    parser.add_argument(
        '--thread-name',
        type=str,
        help=(
            'This decides the thread publication map.'
            ' Supported values are "Concorde", "AI171".'
            ' [default: %(default)s].'
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
            "Add posts by author."
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

    os.makedirs(args.output, exist_ok=True)

    t_start = time.perf_counter()
    thread = thread_struct.Thread()
    for archive in args.archives:
        read_html.update_whole_thread(archive, thread)
    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    logger.info('Number of posts: {:d} Number of words: {:d}'.format(len(thread), word_count))
    common_words = words.read_common_words_file(args.common_words)
    logger.info('Read: {:d} common words from "{:s}" to "{:s}".'.format(
        len(common_words), common_words[0], common_words[-1],
    )
    )
    # write_html.pass_one(thread, common_words)
    common_words = set(common_words)
    if args.thread_name == 'Concorde':
        pub_map = publication_maps.ConcordePublicationMap()
        words_required = pub_map.get_set_of_words_required()
        common_words -= words_required
        logger.info('Common words now length {:d}'.format(len(common_words)))
        write_html.write_whole_thread(thread, common_words, pub_map, args.output)
    elif args.thread_name == 'AI171':
        pub_map = publication_maps.AirIndia171()
        words_required = pub_map.get_set_of_words_required()
        common_words -= words_required
        logger.info('Common words now length {:d}'.format(len(common_words)))
        write_html.write_whole_thread(thread, common_words, pub_map, args.output)
    else:
        logger.error(f'Do not know thread {args.thread_name}')
        return -1
    t_elapsed = time.perf_counter() - t_start
    logger.info('Processed %d posts in %.3f (s)', len(thread), t_elapsed, )
    print('Bye, bye!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
