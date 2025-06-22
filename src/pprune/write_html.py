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
import io
import logging
import os
import string
import time
import typing
from contextlib import contextmanager

import analyse_thread
import publication_maps
import styles
from pprune.common import thread_struct

logger = logging.getLogger(__file__)

PUNCTUATION_TABLE = str.maketrans({key: '-' for key in string.punctuation})
POSTS_PER_PAGE = 20
# +/- Links to other pages
PAGE_LINK_COUNT = 10


def get_out_path(thread: str):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, 'gh-pages', thread))


@contextmanager
def element(_stream, _name, **attributes):
    _stream.write('<{}'.format(_name))
    # Sort attributes: {true_name : attribute key, ...}
    attr_dict = {}
    for k in attributes.keys():
        if k.startswith('_'):
            assert k[1:] not in attr_dict
            attr_dict[k[1:]] = k
        else:
            attr_dict[k] = k
    if len(attributes):
        for a in sorted(attr_dict.keys()):
            _stream.write(' {}={}'.format(a, attributes[attr_dict[a]]))
    _stream.write('>')
    yield
    _stream.write('</{}>\n'.format(_name))


def pass_one(
        thread: thread_struct.Thread,
        common_words: typing.Set[str],
        publication_map: publication_maps.PublicationMap,
) -> typing.Tuple[
    typing.Dict[str, typing.List[int]],
    typing.Dict[int, typing.Set[str]],
    typing.Dict[str, typing.Set[str]]
]:
    """Works through every post in the thread and returns a tuple of maps::

        (
            {subject : [post_ordinals, ...], ...}
            {post_ordinal : set([subject, ...]), ...}
            {user_name : set([subject, ...]), ...}
        )
    """
    logger.info('Starting pass one...')
    t_start = time.perf_counter()
    subject_post_map = collections.defaultdict(list)
    post_subject_map = {}
    user_subject_map = collections.defaultdict(set)
    for i, post in enumerate(thread.posts):
        subjects: typing.Set[str] = set()
        subjects |= analyse_thread.match_words(
            post, common_words, publication_map.get_lowercase_word_to_subject_map()
        )
        subjects |= analyse_thread.match_all_caps(
            post, common_words, publication_map.get_uppercase_word_to_subject_map()
        )
        for phrase_length in publication_map.get_phrase_lengths():
            subjects |= analyse_thread.match_phrases(
                post, common_words, phrase_length, publication_map.get_phrases_to_subject_map(phrase_length)
            )
        if post.permalink in publication_map.get_specific_posts_to_subject_map():
            subjects.add(publication_map.get_specific_posts_to_subject_map()[post.permalink])
        # Add duplicate subjects, for example: 'RAT (Deployment)': {'RAT (All)', }
        dupe_subjects = set()
        for subject in subjects:
            dupe_subjects |= publication_map.get_duplicate_subjects(subject)
        subjects |= dupe_subjects
        for subject in subjects:
            subject_post_map[subject].append(i)
        post_subject_map[post.sequence_num] = subjects
        user_subject_map[post.user.name.strip()] |= subjects
        # print('Post {:3d} subjects [{:3d}]: {}'.format(i, len(subjects), subjects))
    # pprint.pprint(subject_map, width=200)
    logger.info('Pass one complete in %.3f (s)', time.perf_counter() - t_start)
    return subject_post_map, post_subject_map, user_subject_map


def _subject_page_name(subject, page_num):
    result = subject.translate(PUNCTUATION_TABLE) + '{:d}.html'.format(page_num)
    result = result.replace(' ', '_')
    # print(subject, '->' , result)
    return result


def get_count_of_posts_included(
        thread: thread_struct.Thread,
        subject_post_map: typing.Dict[str, typing.List[int]],
) -> typing.Tuple[int, int]:
    """Returns a tuple of (number_of_posts_included, number_of_posts_ignored)."""
    ordinals_included = set()
    for subject in subject_post_map.keys():
        ordinals_included |= set(subject_post_map[subject])
    return len(ordinals_included), len(thread) - len(ordinals_included)


def write_significant_posts(
        thread: thread_struct.Thread,
        publication_map: publication_maps.PublicationMap,
        index: typing.TextIO,
):
    significant_posts = publication_map.get_significant_posts_permalinks()
    if significant_posts:
        with element(index, 'h1'):
            index.write('Significant Posts')
        with element(index, 'p'):
            index.write('These are worth reading before you go any further.')
    # TODO: Create pages and return link or links


def write_index_page(
        thread: thread_struct.Thread,
        subject_post_map: typing.Dict[str, typing.List[int]],
        user_subject_map: typing.Dict[str, typing.Set[str]],
        publication_map: publication_maps.PublicationMap,
        out_path: str,
):
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    styles.writeCssToDir(out_path)
    with open(os.path.join(out_path, 'index.html'), 'w') as index:
        index.write(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
        with element(index, 'html', xmlns="http://www.w3.org/1999/xhtml", dir="ltr", lang="en"):
            with element(index, 'head'):
                with element(index, 'meta', name='keywords', content='pprune'):
                    pass
                with element(index, 'link', rel="stylesheet", type="text/css", href=styles.CSS_FILE):
                    pass
            with element(index, 'body'):
                # with element(index, 'table', border="0", width="96%", cellpadding="0", cellspacing="0", bgcolor="#FFFFFF", align="center"):
                with element(index, 'h1'):
                    index.write(publication_map.get_title())

                with element(index, 'p'):
                    index.write(publication_map.get_introduction_in_html())
                with element(index, 'p'):
                    index.write(f"""    
        These threads have {len(thread)} posts.
        Naturally enough it is ordered in time of each post but since it covers
        so many subjects it is a little hard to follow any particular subject.
""")

                with element(index, 'p'):
                    index.write(
                        'Here I have reorganised the original thread by subject.'
                    )
                    index.write(
                        ' Any post that refers to a subject is included in a page in the original order of the posts.'
                    )
                    index.write(' Posts that mention multiple subjects are duplicated appropriately.')
                    index.write(' I have not changed the content of any post and this includes links and images.')
                    index.write(' Each post is linked to the original so that you can check ;-)')
                with element(index, 'note'):
                    index.write(' NOTE: No AI was used during this.')
                with element(index, 'p'):
                    posts_inc, posts_exc = get_count_of_posts_included(thread, subject_post_map)
                    index.write(
                        f'Total Posts: {len(thread)}'
                        f', posts included: {posts_inc}'
                        f', excluded: {posts_exc}'
                        f', proportion included: {posts_inc / len(thread):.1%}'
                        f', proportion rejected: {1 - posts_inc / len(thread):.1%}'
                    )
                write_significant_posts(thread, publication_map, index)
                with element(index, 'h1'):
                    index.write('Posts by Subject')
                with element(index, 'p'):
                    index.write(
                        'Here are all {:d} subjects I have identified with the number of posts for each subject:'.format(
                            len(subject_post_map)))
                with element(index, 'table', _class="indextable"):
                    COLUMNS = 4
                    subjects = sorted(subject_post_map.keys())
                    rows = [subjects[i:i + COLUMNS] for i in range(0, len(subjects), COLUMNS)]
                    subject_index = 0
                    for row in rows:
                        with element(index, 'tr'):
                            for _cell in row:
                                subject = subjects[subject_index]
                                with element(index, 'td', _class='indextable'):
                                    with element(index, 'a',
                                                 href=_subject_page_name(subject, 0)):
                                        index.write('{:s} [{:d}]'.format(subject,
                                                                         len(subject_post_map[subject])))
                                # print(subject, subject_map[subject])
                                subject_index += 1
                # Posts by user, including the subjects they covered
                with element(index, 'h1'):
                    index.write('Posts by User on a Subject')
                MOST_COMMON_COUNT = 40
                user_count = collections.Counter([post.user.name.strip() for post in thread.posts])
                # print(user_count)
                with element(index, 'p'):
                    index.write('The most prolific {:d} posters in the original thread:'.format(MOST_COMMON_COUNT))
                with element(index, 'table', _class="indextable"):
                    with element(index, 'tr'):
                        with element(index, 'th', _class='indextable'):
                            index.write('User Name')
                        with element(index, 'th', _class='indextable'):
                            index.write('Number of Posts')
                        with element(index, 'th', _class='indextable'):
                            index.write('Subjects')
                    for k, v in user_count.most_common(MOST_COMMON_COUNT):
                        with element(index, 'tr'):
                            # User name
                            with element(index, 'td', _class='indextable'):
                                index.write(k)
                            # Count of posts
                            with element(index, 'td', _class='indextable'):
                                index.write('{:d}'.format(v))
                            # Comma separated list of subjects that they are identified with 
                            with element(index, 'td', _class='indextable'):
                                subjects = sorted(user_subject_map[k])
                                for subject in subjects:
                                    with element(index, 'a',
                                                 href=_subject_page_name(subject, 0)):
                                        index.write(subject)
                                    index.write('&nbsp; ')
                # TODO: Create author pages aof their posts and link to it.

def _write_page_links(subject, page_num, page_count, f):
    with element(f, 'p', _class='page_links'):
        f.write('Page Links:&nbsp;')
        if page_count > 1:
            with element(f, 'a', href=_subject_page_name(subject, 0)):
                f.write('First')
            if page_num > 0:
                f.write('&nbsp;')
                with element(f, 'a', href=_subject_page_name(subject, page_num - 1)):
                    f.write('Previous')
            page_start = max(0, page_num - PAGE_LINK_COUNT)
            page_end = min(page_count - 1, page_num + PAGE_LINK_COUNT)
            for p in range(page_start, page_end + 1):
                f.write('&nbsp;')
                with element(f, 'a', href=_subject_page_name(subject, p)):
                    if p == page_num:
                        with element(f, 'b'):
                            f.write('{:d}'.format(p + 1))
                    else:
                        f.write('{:d}'.format(p + 1))
            if page_num < page_count - 1:
                f.write('&nbsp;')
                with element(f, 'a', href=_subject_page_name(subject, page_num + 1)):
                    f.write('Next')
            f.write('&nbsp;')
            with element(f, 'a', href=_subject_page_name(subject, page_count - 1)):
                f.write('Last')
            f.write('&nbsp;')
        with element(f, 'a', href='index.html'):
            f.write('Index Page')


def write_subject_page(thread, subject_map, subject, out_path):
    _posts = subject_map[subject]
    pages = [_posts[i:i + POSTS_PER_PAGE] for i in range(0, len(_posts), POSTS_PER_PAGE)]
    for page_index, page in enumerate(pages):
        with open(os.path.join(out_path, _subject_page_name(subject, page_index)), 'w') as out_file:
            out_file.write(
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
            with element(out_file, 'html', xmlns="http://www.w3.org/1999/xhtml", dir="ltr", lang="en"):
                with element(out_file, 'head'):
                    with element(out_file, 'meta', name='keywords', content='pprune {:s}'.format(subject)):
                        pass
                    with element(out_file, 'link', rel="stylesheet", type="text/css", href=styles.CSS_FILE):
                        pass
                with element(out_file, 'body'):
                    with element(out_file, 'h1'):
                        out_file.write(
                            'Posts about: "{:s}" [Posts: {:d} Pages: {:d}]'.format(subject, len(_posts), len(pages)))
                    _write_page_links(subject, page_index, len(pages), out_file)
                    # with element(f, 'table', border="0", width="96%", cellpadding="0", cellspacing="0", bgcolor="#FFFFFF", align="center"):
                    with element(out_file, 'table', _class='posts'):
                        for post_index in page:
                            post = thread.posts[post_index]
                            with element(out_file, 'tr', valign="top"):
                                # with element(f, 'td', _class="alt2", style="border: 1px solid #000063; border-top: 0px; border-bottom: 0px"):
                                with element(out_file, 'td', _class="post"):
                                    out_file.write(post.user.name.strip())
                                    out_file.write('<br/>')
                                    out_file.write(post.timestamp.isoformat())
                                    with element(out_file, 'a', href=post.permalink):
                                        out_file.write('<br/>permalink')
                                    out_file.write(' Post: {:d}'.format(post.sequence_num))
                                with element(out_file, 'td', _class="post"):
                                    out_file.write(post.node.prettify(formatter='html'))
                    _write_page_links(subject, page_index, len(pages), out_file)


def write_whole_thread(
        thread: thread_struct.Thread,
        common_words: typing.Set[str],
        publication_map: publication_maps.PublicationMap,
        output_path: str
):
    logger.info('Starting write_whole_thread() to %s', output_path)
    t_start = time.perf_counter()
    # out_path = get_out_path(output_name)
    # shutil.rmtree(output_path, ignore_errors=True)
    subject_post_map, post_subject_map, user_subject_map = pass_one(thread, common_words, publication_map)
    #     pprint.pprint(user_subject_map)
    logger.info('Writing: {:s}'.format('index.html'))
    write_index_page(thread, subject_post_map, user_subject_map, publication_map, output_path)
    for subject in sorted(subject_post_map.keys()):
        logger.info('Writing: "{:s}" [{:d}]'.format(subject, len(subject_post_map[subject])))
        write_subject_page(thread, subject_post_map, subject, output_path)
    #     pprint.pprint(post_map)
    logger.info('Writing thread done in %.3f (s)', time.perf_counter() - t_start)
