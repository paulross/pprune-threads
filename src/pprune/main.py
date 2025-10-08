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

from pprune.common import log_config
from pprune.common import read_html
from pprune.common import thread_struct
from pprune.common import words
from pprune.common import write_html
from pprune.publication_maps import air_india_171
from pprune.publication_maps import concorde
from pprune.publication_maps import example

logger = logging.getLogger(__file__)

# Map of thread name to a class declaration that can be created and
# eventually passed to write_html.write_whole_thread().
THREAD_NAME_TO_CLASS_MAP = {
    'AI171': air_india_171.AirIndia171,
    'Example': example.Example,
    'Concorde': concorde.Concorde,
}


def main():
    print(f'Command: {" ".join(sys.argv)}')
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
    parser.add_argument(
        '-o', '--output',
        type=str,
        nargs='?',
        default=None,
        help=(
            'Directory to write the output to.'
            ' If absent then this will be computed as docs/gh-pages/<THREAD_NAME>'
            ' [default: %(default)s].'
        )
    )
    supported_threads = ', '.join(sorted(f'"{v}"' for v in THREAD_NAME_TO_CLASS_MAP.keys()))
    parser.add_argument(
        '--thread-name',
        type=str,
        nargs='?',
        required=True,
        help=(
            'This decides the thread publication map.'
            f' Supported values are: [{supported_threads}].'
            ' [default: %(default)s].'
        )
    )
    parser.add_argument(
        "--common-words",
        type=int,
        default=1000,
        help="Number of common words to exclude. [default: %(default)d]",
    )
    # parser.add_argument(
    #     "--authors",
    #     action="store_true",
    #     help=(
    #         "Add posts by author."
    #     )
    # )
    parser.add_argument(
        "--limit-posts",
        type=int,
        default=0,
        help=(
            "Limit the thread to this number of posts."
            " Zero means all posts."
            " [default: %(default)d]"
        ),
    )
    parser.add_argument(
        "--min-likes",
        type=int,
        default=0,
        help=(
            "Limit the thread to posts than have at least this many likes."
            " This takes priority over --limit-posts."
            " Zero means all posts. [default: %(default)d]"
        ),
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
    # print(f'Args: {args}')
    logging.basicConfig(
        level=args.log_level,
        format=log_config.DEFAULT_OPT_LOG_FORMAT_NO_PROCESS,
        stream=sys.stdout,
    )
    if args.output is None:
        output_dir = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__), os.pardir, os.pardir, 'docs', 'gh-pages', args.thread_name
            )
        )
        logger.info("Computed output directory is %s", output_dir)
    else:
        output_dir = args.output
        logger.info("Given output directory is %s", output_dir)
    os.makedirs(output_dir, exist_ok=True)
    # Get to work.
    t_start = time.perf_counter()
    archive_post_count = {}
    # Compose the thread.
    thread = thread_struct.Thread()
    for archive in args.archives:
        prev_post_count = len(thread)
        read_html.update_whole_thread(archive, thread)
        archive_post_count[archive] = len(thread) - prev_post_count
    # Clean up the thread and remove unwanted posts.
    thread.sort_by_sequence_number()
    if args.min_likes:
        logger.info("Likes limiting, was %d posts.", len(thread))
        thread.posts = [post for post in thread.posts if len(post.liked_by_users) >= args.min_likes]
        logger.info("Likes limiting, now %d posts.", len(thread))
    if args.limit_posts > 0:
        logger.info("Post limiting, was %d posts.", len(thread))
        thread.posts = thread.posts[:args.limit_posts]
        logger.info("Post limiting, now %d posts.", len(thread))
    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    logger.info('Number of posts: {:d} Number of words: {:d}'.format(len(thread), word_count))
    common_words = words.read_common_words_file(args.common_words)
    logger.info(
        'Read: {:d} common words from "{:s}" to "{:s}".'.format(
            len(common_words), common_words[0], common_words[-1],
        )
    )
    for archive in archive_post_count:
        logger.info(
            'Read: {:d} posts, {:d} pages from "{:s}"'.format(
                archive_post_count[archive], 1 + archive_post_count[archive] // 20, archive,
            )
        )
    common_words = set(common_words)
    if args.thread_name in THREAD_NAME_TO_CLASS_MAP:
        pub_map = THREAD_NAME_TO_CLASS_MAP[args.thread_name]()
        words_required = pub_map.get_set_of_words_required()
        common_words -= words_required
        logger.info('Common words now length {:d}'.format(len(common_words)))
        write_html.write_whole_thread(thread, common_words, pub_map, output_dir)
    else:
        logger.error(
            f'Do not know of thread "{args.thread_name}".'
            f' Supported threads are: {supported_threads}'
        )
        return -1
    t_elapsed = time.perf_counter() - t_start
    logger.info('Processed %d posts in %.3f (s)', len(thread), t_elapsed, )
    print('Bye, bye!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
