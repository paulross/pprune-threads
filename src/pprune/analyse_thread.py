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

import collections
import typing

import pprune.common.thread_struct


def filter_counter(
        word_counter: collections.Counter,
        freq_ge: int,
) -> collections.Counter:
    # Filter by frequency count.
    wc = collections.Counter()
    for w, c in word_counter.most_common():
        if c >= freq_ge:
            wc[w] = c
    return wc


def count_non_cap_words(
        thread: pprune.common.thread_struct.Thread,
        common_words: typing.Sequence[str],
        freq_ge: int,
) -> typing.Dict[typing.Hashable, int]:
    """This takes a thread and a set of common words (must be lower case)
    to remove and a frequency lower limit.
    This also ignores all uppercase words and usernames in the text.
    The case of the return word(s) is lowercase.
    It returns a dict of {word : count}."""
    word_counter = collections.Counter()
    all_users = thread.all_users
    for post in thread.posts:
        trimmed_words = [
            word for word in post.words
            # Eliminate common words.
            if word.lower() not in common_words
               # And eliminate words in users.
               and word not in all_users
               # And eliminate all capital words.
               and word.upper() != word
        ]
        word_counter.update(trimmed_words)
    return filter_counter(word_counter, freq_ge)


def count_phrases(
        thread: pprune.common.thread_struct.Thread,
        common_words: typing.Sequence[str],
        phrase_length: int,
        freq_ge: int,
) -> typing.Dict[typing.Hashable, int]:
    """This takes a thread and a set of common words (must be lower case).
    This also ignores all uppercase words and usernames in the text.
    The case of the return word(s) is lowercase.
    It returns a dict of {phrase : count}."""
    phrase_counter = collections.Counter()
    for post in thread.posts:
        trimmed_words = post.significant_words(common_words)
        phrases = []
        for i in range(len(trimmed_words) - (phrase_length - 1)):
            phrase = tuple(trimmed_words[i:i + phrase_length])
            # if all([len(w) > 1 for w in phrase]):
            #     phrases.append(phrase)
            phrases.append(phrase)
        phrase_counter.update(phrases)
    return filter_counter(phrase_counter, freq_ge)


def count_all_caps(
        thread: pprune.common.thread_struct.Thread,
        min_size: int,
        freq_ge: int,
) -> typing.Dict[typing.Hashable, int]:
    """Returns a dict of {word : count} for all thd uppercase words in the thread."""
    word_counter = collections.Counter()
    for post in thread.posts:
        words = post.cap_words(min_size)
        word_counter.update(words)
    return filter_counter(word_counter, freq_ge)


def match_words(post, common_words, word_map) -> typing.Set[str]:
    """For a given post this strips the common_words and returns the set of word_map values
    that match any word that is in word_map."""
    trimmed_words = post.words_removed(common_words, True)
    ret = {word_map[w] for w in trimmed_words if w in word_map}
    return ret


def match_all_caps(post, common_words, caps_map):
    """For a given post this strips the common_words and returns the set of phrase_map values
    that match any upper case words that are in caps_map."""
    trimmed_words = post.words_removed(common_words, False)
    return {caps_map[w] for w in trimmed_words if w.upper() == w and len(w) > 1 and w in caps_map}


def match_phrases(post, common_words, phrase_length, phrase_map):
    """For a given post this strips the common_words and returns the phrase_map values
    that match for any phrases of length phrase_length."""
    result = set()
    trimmed_words = post.words_removed(common_words, True)
    for i in range(len(trimmed_words) - (phrase_length - 1)):
        phrase = tuple(trimmed_words[i:i + phrase_length])
        try:
            result.add(phrase_map[phrase])
        except KeyError:
            pass
    return result
