# MIT License
#
# Copyright (c) 2025 Paul Ross https://github.com/paulross
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
"""
Support for word lists and common words.
"""
import logging
import os
import typing

logger = logging.getLogger(__file__)


def common_wordlists_file(file_name: str) -> str:
    """Returns the paths in  the common wordlists directory."""
    return os.path.normpath(os.path.join(os.path.dirname(__file__), 'wordlists', file_name))


def common_words_file():
    """Returns the common word lists file path."""
    return common_wordlists_file('count_1w.txt')


def read_common_words_file(limit: int) -> typing.List[str]:
    """Reads the common wordlists file and returns a list of lowercase words of size limit.
    If limit is <= 0 all words are read."""
    file_path = common_words_file()
    logger.debug('Reading words file: {}'.format(file_path))
    ret_list = []
    with open(file_path) as f:
        for line in f.readlines():
            if not line:
                break
            ret_list.append(line.split()[0].lower())
            if limit > 0 and len(ret_list) >= limit:
                break
    logger.debug('Read %d words from file: {}'.format(len(ret_list), file_path))
    return ret_list
