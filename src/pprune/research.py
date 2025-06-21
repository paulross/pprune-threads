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
import collections
import logging
import pprint
import sys
import time

import analyse_thread
import pprune.common.log_config
import pprune.common.read_html
import pprune.common.thread_struct
import pprune.common.words

logger = logging.getLogger(__file__)


def print_non_cap_words(thread, common_words, freq_ge: int):
    print(' print_non_cap_words(): freq_ge={:d} '.format(freq_ge).center(75, '-'))
    word_counter = analyse_thread.count_non_cap_words(thread, common_words, freq_ge)
    print(f'Words counted: {sum(word_counter.values())}')
    # pprint.pprint(word_counter.most_common(400))
    pprint.pprint(word_counter)
    # print('print_words(): sorted')
    pprint.pprint(sorted(word_counter))
    # pprint.pprint(sorted(word_counter.most_common(400)))
    print(' print_non_cap_words(): freq_ge={:d} DONE '.format(freq_ge).center(75, '-'))


def print_phrases(thread, common_words, phrase_length, most_common_count: int, freq_ge: int):
    print(
        ' print_phrases(): len={:d} most_common={:d} freq_ge={:d} '.format(
            phrase_length, most_common_count, freq_ge).center(75, '-')
    )
    word_counter = analyse_thread.count_phrases(thread, common_words, phrase_length, freq_ge=freq_ge)
    # pprint.pprint(word_counter.most_common(most_common_count))
    for words, count in word_counter.most_common(most_common_count):
        print(f'{" ".join(words):32} : {count:4d}')
    print(
        ' print_phrases(): len={:d} most_common={:d} freq_ge={:d} DONE '.format(
            phrase_length, most_common_count, freq_ge).center(75, '-')
    )
    print(
        ' print_phrases(): len={:d} most_common={:d} freq_ge={:d} sorted '.format(
            phrase_length, most_common_count, freq_ge).center(75, '-')
    )
    # pprint.pprint(sorted(word_counter.most_common(most_common_count)))
    for words, count in sorted(word_counter.most_common(most_common_count)):
        print(f'{" ".join(words):32} : {count:4d}')
    print(
        ' print_phrases(): len={:d} most_common={:d} freq_ge={:d} sorted DONE '.format(
            phrase_length, most_common_count, freq_ge).center(75, '-')
    )


def print_all_caps(thread, most_common_count: int, freq_ge: int):
    print(' print_all_caps(): most_common={:d} freq_ge={:d} '.format(most_common_count, freq_ge).center(75, '-'))
    word_counter = analyse_thread.count_all_caps(thread, min_size=2, freq_ge=freq_ge)
    pprint.pprint(word_counter.most_common(most_common_count))
    print(' print_all_caps(): most_common={:d} freq_ge={:d} DONE '.format(most_common_count, freq_ge).center(75, '-'))
    print(' print_all_caps(): most_common={:d} freq_ge={:d} sorted '.format(most_common_count, freq_ge).center(75, '-'))
    pprint.pprint(sorted(word_counter.most_common(most_common_count)))
    print(' print_all_caps(): most_common={:d} freq_ge={:d} sorted DONE '.format(most_common_count, freq_ge).center(75, '-'))


def print_authors(thread: pprune.common.thread_struct.Thread, most_common_count: int):
    user_count = collections.Counter()
    for user in thread.all_users:
        for _post_ordinal in thread.get_post_ordinals(user):
            user_count.update([user.name])
    print(' print_authors(): most_common({:d}) '.format(most_common_count).center(75, '-'))
    # pprint.pprint(user_count.most_common(most_common_count))
    total = 0
    for user_name, count in user_count.most_common(most_common_count):
        print(f'{user_name:32} : {count:4d}')
        total += count
    print(f'TOTAL: {total:4d}')
    print(' print_authors(): most_common({:d}) DONE '.format(most_common_count).center(75, '-'))
    print(' print_authors(): most_common({:d}) sorted '.format(most_common_count).center(75, '-'))
    # pprint.pprint(user_count.most_common(most_common_count))
    for user_name, count in sorted(user_count.most_common(most_common_count)):
        print(f'{user_name:32} : {count:4d}')
    print(' print_authors(): most_common({:d}) sorted DONE '.format(most_common_count).center(75, '-'))


def print_research(thread, common_words, most_common_count: int, freq_ge: int,
                   non_cap_words: bool, all_cap_words: bool, phrases: int, authors: bool):
    if non_cap_words:
        print_non_cap_words(thread, common_words, freq_ge)
    if all_cap_words:
        print_all_caps(thread, most_common_count, freq_ge)
    if phrases > 0:
        print_phrases(thread, common_words, phrases, most_common_count, freq_ge)
    if authors:
        print_authors(thread, most_common_count)


def main():
    parser = argparse.ArgumentParser(description='Archive a pprune thread to local storage.')
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
        "--common-words",
        type=int,
        default=1000,
        help="Number of common words to exclude. [default: %(default)d]",
    )
    parser.add_argument(
        "--most-common-count",
        type=int,
        default=100,
        help="Limit the report to this many of the highest frequency. [default: %(default)d]",
    )
    parser.add_argument(
        "--freq-ge",
        type=int,
        default=10,
        help="Limit the report to frequencies >= this value. [default: %(default)d]",
    )
    parser.add_argument(
        "--non-cap-words",
        action="store_true",
        help=(
            "Report the frequency of non-cap words. "
        )
    )
    parser.add_argument(
        "--all-cap-words",
        action="store_true",
        help=(
            "Report the frequency of all-cap words. "
        )
    )
    parser.add_argument(
        "--phrases",
        type=int,
        default=0,
        help="If >0 then report the frequency of phrases of this length. [default: %(default)d]",
    )
    parser.add_argument(
        "--authors",
        action="store_true",
        help=(
            "Show the count of posts by author. "
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
        format=pprune.common.log_config.DEFAULT_OPT_LOG_FORMAT_NO_PROCESS,
        stream=sys.stdout,
    )

    # print(args)

    t_start = time.perf_counter()
    thread = pprune.common.thread_struct.Thread()
    for archive in args.archives:
        pprune.common.read_html.update_whole_thread(archive, thread)

    print(f'Number of posts: {len(thread)}')
    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    print('Number of words: {:d}'.format(word_count))
    common_words = pprune.common.words.read_common_words_file(args.common_words)

    print_research(
        thread, common_words, args.most_common_count, args.freq_ge,
        args.non_cap_words, args.all_cap_words, args.phrases, args.authors,
    )

    t_elapsed = time.perf_counter() - t_start
    logger.info('Read %d posts in %.3f (s)', len(thread), t_elapsed, )


if __name__ == '__main__':
    main()
