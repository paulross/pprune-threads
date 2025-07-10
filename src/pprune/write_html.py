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
import datetime
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


def format_datetime(dt: datetime.datetime) -> str:
    """Return a human readable datetime."""
    return dt.strftime('%B %d, %Y, %H:%M:%S')


class PassOneResult:
    def __init__(self):
        # Map of {subject: [post_index in Thread.posts, ...], ...}
        self.subject_post_map: typing.Dict[str, typing.List[int]] = {}
        # Map of {post_sequence_number: [subjects, ...], ...}
        self.post_subject_map: typing.Dict[int, typing.Set[str]] = {}
        # Map of {username: [subjects, ...], ...}
        self.user_subject_map: typing.Dict[str, typing.Set[str]] = collections.defaultdict(set)
        # Map of {username: [post_index in Thread.posts, ...], ...}
        self.user_ordinal_map: typing.Dict[str, typing.List[int]] = collections.defaultdict(list)
        # Dict of {(sequence_number, subject) : page_link_to_post_on_subject_page, ...}
        self.sequence_num_subject_link_map = {}

    def add_subject_post(
            self,
            subjects: typing.Set[str],
            post_index: int,
            sequence_num: int,
            user_name: str,
    ) -> None:
        for subject in subjects:
            if subject not in self.subject_post_map:
                self.subject_post_map[subject] = []
            self.subject_post_map[subject].append(post_index)
        self.post_subject_map[sequence_num] = subjects
        self.user_subject_map[user_name.strip()] |= subjects
        self.user_ordinal_map[user_name.strip()].append(post_index)

    def add_sequence_num_subject_link(self, sequence_num: int, subject: str, link: str) -> None:
        """Populated by write_a_subject_page()."""
        self.sequence_num_subject_link_map[(sequence_num, subject)] = link


def pass_one(
        thread: thread_struct.Thread,
        common_words: typing.Set[str],
        publication_map: publication_maps.PublicationMap,
) -> PassOneResult:
    """Works through every post in the thread and returns a PassOneResult."""
    logger.info('Starting pass one...')
    t_start = time.perf_counter()
    pass_one_result = PassOneResult()
    for i, post in enumerate(thread.posts):
        subjects: typing.Set[str] = set()
        subjects |= analyse_thread.match_words(
            post, common_words, publication_map.get_lowercase_word_to_subject_map()
        )
        subjects |= analyse_thread.match_all_caps(
            post, common_words, publication_map.get_uppercase_word_to_subject_map()
        )
        for phrase_length in publication_map.get_phrase_lengths():
            phrase_map = publication_map.get_phrases_to_subject_map(phrase_length)
            subjects |= analyse_thread.match_phrases(
                post, common_words, phrase_length, phrase_map,
            )
        if post.permalink in publication_map.get_specific_posts_to_subject_map():
            subjects.add(publication_map.get_specific_posts_to_subject_map()[post.permalink])
        # Add duplicate subjects, for example: 'RAT (Deployment)': {'RAT (All)', }
        dupe_subjects = set()
        for subject in subjects:
            dupe_subjects |= publication_map.get_duplicate_subjects(subject)
        subjects |= dupe_subjects
        pass_one_result.add_subject_post(subjects, i, post.sequence_num, post.user.name.strip())
    all_subject_titles = publication_map.get_all_subject_titles()
    for subject_title in sorted(all_subject_titles):
        if subject_title not in pass_one_result.subject_post_map:
            logger.warning('No post with subject title "%s"', subject_title)
    # Add the links from the message sequence number + subject to the planned subject page.
    for subject_title_has_posts in pass_one_result.subject_post_map.keys():
        _posts = pass_one_result.subject_post_map[subject_title_has_posts]
        pages = [_posts[i:i + POSTS_PER_PAGE] for i in range(0, len(_posts), POSTS_PER_PAGE)]
        for page_index, page in enumerate(pages):
            for post_index in page:
                post = thread.posts[post_index]
                pass_one_result.add_sequence_num_subject_link(
                    post.sequence_num,
                    subject_title_has_posts,
                    f'{_page_name(subject_title_has_posts, page_index)}#{post.sequence_num}',
                )
    logger.info('Pass one complete in %.3f (s)', time.perf_counter() - t_start)
    return pass_one_result


def _page_name(subject, page_num):
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


def write_index_significant_posts(
        thread: thread_struct.Thread,
        publication_map: publication_maps.PublicationMap,
        index: typing.TextIO,
):
    """Optionally, writes out a list of significant posts."""
    significant_posts = publication_map.get_significant_posts_permalinks()
    if significant_posts:
        with element(index, 'h1'):
            index.write('Significant Posts')
        with element(index, 'p'):
            index.write('These are worth reading before you go any further.')
        post_ordinals = []
        for permalink in significant_posts:
            try:
                post_ordinals.append(thread.post_map[permalink])
            except KeyError:
                logger.error('Can not find permalink %s', permalink)
        post_ordinals.sort()
        with element(index, 'ul'):
            for post_ordinal in post_ordinals:
                post = thread.posts[post_ordinal]
                with element(index, 'li'):
                    subject = post.subject.strip()
                    if not subject:
                        subject = 'No Subject'
                    index.write(
                        f'Permalink: <a href="{post.permalink}">{subject}</a> User: <a href="{post.user.href}">{post.user.name}</a>')


def write_index_main_subject_table(
        subject_post_map: typing.Dict[str, typing.List[int]],
        index: typing.TextIO,
):
    """Write out the main table of subjects."""
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
                                     href=_page_name(subject, 0)):
                            index.write('{:s} [{:d}]'.format(subject,
                                                             len(subject_post_map[subject])))
                    # print(subject, subject_map[subject])
                    subject_index += 1


def write_index_most_upvoted_posts_table(
        thread: thread_struct.Thread,
        publication_map: publication_maps.PublicationMap,
        index: typing.TextIO,
):
    """Posts by most up-voted."""
    # dict of {votes : [post_ordinals, ...], ...}
    liked_by_users_dict = collections.defaultdict(list)
    total_upvotes = 0
    for i, post in enumerate(thread.posts):
        if len(post.liked_by_users) > 0:
            liked_by_users_dict[len(post.liked_by_users)].append(i)
            total_upvotes += len(post.liked_by_users)
    if liked_by_users_dict:
        keys = sorted(liked_by_users_dict.keys(), reverse=True)
        post_count = 0
        for k in keys:
            post_count += len(liked_by_users_dict[k])
            if post_count >= publication_map.get_upvoted_post_count_limit():
                break
        with element(index, 'h1'):
            index.write(f'The {post_count} Most Up-voted Posts')
        with element(index, 'p'):
            index.write(
                'This list the posts that have the largest number of up-votes.'
                ' They are <i>likely</i> to be more important than others.'
                f' There are {total_upvotes:d} up-votes on {len(thread.posts)} posts.'
                ' "User Name" links are to the pprune user.'
                ' "Permalink" links is to the post on pprune.'
            )
        post_count = 0
        with element(index, 'table', _class="indextable"):
            _write_table_header(['Up-votes', 'Text (Quoted Text Removed)', 'User Name', 'Permalink', ], index)
            for k in keys:
                for post_ordinal in liked_by_users_dict[k]:
                    post = thread.posts[post_ordinal]
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write(f'{len(post.liked_by_users)}')
                        # post_subject_line = post.subject.strip()
                        # if not post_subject_line:
                        #     # post_subject_line = 'No Subject'
                        #     post_subject_line = post.text_stripped[:64]

                        # post_subject_line = post.text_stripped[:publication_map.get_upvoted_post_text_limit()]

                        post_subject_line = post.text_stripped_without_quoted_message[
                                            :publication_map.get_upvoted_post_text_limit()
                                            ]
                        with element(index, 'td', _class='indextable'):
                            index.write(post_subject_line)
                        with element(index, 'td', _class='indextable'):
                            with element(index, 'a', href=post.user.href):
                                index.write(post.user.name)
                        with element(index, 'td', _class='indextable'):
                            with element(index, 'a', href=post.permalink):
                                index.write('Permalink')
                    post_count += 1
                    if post_count >= publication_map.get_upvoted_post_count_limit():
                        break
                if post_count >= publication_map.get_upvoted_post_count_limit():
                    break
    else:
        assert 0


def _write_table_header(headers: typing.List[str], index: typing.TextIO):
    with element(index, 'tr'):
        for header in headers:
            with element(index, 'th', _class='indextable'):
                index.write(header)


def write_index_user_subject_table(
        thread: thread_struct.Thread,
        user_subject_map: typing.Dict[str, typing.Set[str]],
        publication_map: publication_maps.PublicationMap,
        index: typing.TextIO,
):
    """Posts by user, including the subjects they covered."""
    with element(index, 'h1'):
        index.write('Posts by User on a Subject')
    # MOST_COMMON_COUNT = 40
    user_count = collections.Counter([post.user for post in thread.posts])
    # print(user_count)
    with element(index, 'p'):
        index.write(
            'The most prolific {:d} posters in the original thread:'.format(publication_map.get_number_of_top_authors())
        )
        index.write(
            'The User Name links to the User page (below).'
            'The "Subjects" links to the first page on that subject.'
        )
    upvotes_dict: typing.Dict[thread_struct.User, int] = {}
    for post in thread.posts:
        if post.user not in upvotes_dict:
            upvotes_dict[post.user] = len(post.liked_by_users)
        else:
            upvotes_dict[post.user] += len(post.liked_by_users)

    with element(index, 'table', _class="indextable"):
        _write_table_header(['User Name', 'Number of Posts', 'Total Up-votes', 'Up-votes/post', 'Subjects'], index)
        for user, post_count in user_count.most_common(publication_map.get_number_of_top_authors()):
            with element(index, 'tr'):
                # User name
                with element(index, 'td', _class='indextable'):
                    # with element(index, 'a', href=user.href):
                    #     index.write(user.name)
                    # Link to users page below in write_user_post_table()
                    with element(index, 'a', href=_page_name('USER_' + user.name, 0)):
                        index.write(user.name)
                # Count of posts
                with element(index, 'td', _class='indextable'):
                    index.write('{:d}'.format(post_count))
                # Count of up-votes
                with element(index, 'td', _class='indextable'):
                    index.write('{:d}'.format(upvotes_dict[user]))
                # 'Up-votes/post'
                with element(index, 'td', _class='indextable'):
                    index.write('{:.1f}'.format(upvotes_dict[user] / post_count))
                # Comma separated list of subjects that they are identified with
                with element(index, 'td', _class='indextable'):
                    subjects = sorted(user_subject_map[user.name])
                    for subject in subjects:
                        with element(index, 'a',
                                     href=_page_name(subject, 0)):
                            index.write(subject)
                        index.write('&nbsp; ')


def write_index_user_post_table(
        thread: thread_struct.Thread,
        user_ordinal_map: typing.Dict[str, typing.List[int]],
        publication_map: publication_maps.PublicationMap,
        index: typing.TextIO,
):
    """Write a table with links to pages that have all user posts."""
    with element(index, 'h1'):
        index.write('Users Posts')
    with element(index, 'p'):
        index.write(
            f'Here are posts by users that have made >= {publication_map.get_minimum_number_username_posts():d} posts.'
            f' If a post matches a subject there will be a link to the subject page which has that post so the post can be seen in context.'
            f' Sorted by user name with [post count]:'
        )
    with element(index, 'table', _class="indextable"):
        COLUMNS = 8
        filtered_users = []
        for user_name in user_ordinal_map.keys():
            if len(user_ordinal_map[user_name]) >= publication_map.get_minimum_number_username_posts():
                filtered_users.append(user_name)
        filtered_users.sort()
        rows = [filtered_users[i:i + COLUMNS] for i in range(0, len(filtered_users), COLUMNS)]
        subject_index = 0
        for row in rows:
            with element(index, 'tr'):
                for _cell in row:
                    user_name = filtered_users[subject_index]
                    if len(user_ordinal_map[user_name]) >= publication_map.get_minimum_number_username_posts():
                        with element(index, 'td', _class='indextable'):
                            with element(index, 'a', href=_page_name('USER_' + user_name, 0)):
                                index.write('{:s} [{:d}]'.format(user_name, len(user_ordinal_map[user_name])))
                        subject_index += 1


def write_index_page(
        thread: thread_struct.Thread,
        pass_one_result: PassOneResult,
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
                with element(index, 'p'):
                    index.write(
                        ' Any post that refers to a subject is included in a page in the original order of the posts.'
                    )
                with element(index, 'p'):
                    index.write(' Posts that mention multiple subjects are duplicated appropriately.')
                    index.write(' I have not changed the content of any post and this includes links and images.')
                with element(index, 'p'):
                    index.write(' Each post is linked to the original so that you can check ;-)')
                with element(index, 'note'):
                    index.write(' NOTE: No AI was used during this.')
                with element(index, 'p'):
                    posts_inc, posts_exc = get_count_of_posts_included(thread, pass_one_result.subject_post_map)
                    index.write(
                        f'Total Posts: {len(thread)}'
                        f', posts included: {posts_inc}'
                        f', excluded: {posts_exc}'
                        f', proportion included: {posts_inc / len(thread):.1%}'
                        f', proportion rejected: {1 - posts_inc / len(thread):.1%}'
                    )
                with element(index, 'p'):
                    index.write(
                        f'Posts on the thread start at {format_datetime(thread.posts[0].timestamp)}'
                        f' and finish at {format_datetime(thread.posts[-1].timestamp)}.'
                        f' This build was made at {format_datetime(datetime.datetime.now())}.'
                    )
                with element(index, 'p'):
                    index.write('Project is here: ')
                    with element(index, 'a', href="https://github.com/paulross/pprune-threads"):
                        index.write('https://github.com/paulross/pprune-threads.')
                    index.write('Issues can be raised here: ')
                    with element(index, 'a', href="https://github.com/paulross/pprune-threads/issues"):
                        index.write('https://github.com/paulross/pprune-threads/issues.')

                write_index_significant_posts(thread, publication_map, index)

                write_index_main_subject_table(pass_one_result.subject_post_map, index)

                write_index_most_upvoted_posts_table(thread, publication_map, index)

                write_index_user_subject_table(thread, pass_one_result.user_subject_map, publication_map, index)

                write_index_user_post_table(thread, pass_one_result.user_ordinal_map, publication_map, index)


def _write_page_links(subject: str, page_num: int, page_count: int, out_file: typing.TextIO) -> None:
    with element(out_file, 'p', _class='page_links'):
        out_file.write('Page Links:&nbsp;')
        if page_count > 1:
            with element(out_file, 'a', href=_page_name(subject, 0)):
                out_file.write('First')
            if page_num > 0:
                out_file.write('&nbsp;')
                with element(out_file, 'a', href=_page_name(subject, page_num - 1)):
                    out_file.write('Previous')
            page_start = max(0, page_num - PAGE_LINK_COUNT)
            page_end = min(page_count - 1, page_num + PAGE_LINK_COUNT)
            for p in range(page_start, page_end + 1):
                out_file.write('&nbsp;')
                with element(out_file, 'a', href=_page_name(subject, p)):
                    if p == page_num:
                        with element(out_file, 'b'):
                            out_file.write('{:d}'.format(p + 1))
                    else:
                        out_file.write('{:d}'.format(p + 1))
            if page_num < page_count - 1:
                out_file.write('&nbsp;')
                with element(out_file, 'a', href=_page_name(subject, page_num + 1)):
                    out_file.write('Next')
            out_file.write('&nbsp;')
            with element(out_file, 'a', href=_page_name(subject, page_count - 1)):
                out_file.write('Last')
            out_file.write('&nbsp;')
        with element(out_file, 'a', href='index.html'):
            out_file.write('Index Page')


def write_a_subject_page(
        thread: thread_struct.Thread,
        pass_one_result: PassOneResult,
        subject: str,
        out_path: str,
):
    """Writes all the pages for a single subject."""
    _posts = pass_one_result.subject_post_map[subject]
    pages = [_posts[i:i + POSTS_PER_PAGE] for i in range(0, len(_posts), POSTS_PER_PAGE)]
    for page_index, page in enumerate(pages):
        with open(os.path.join(out_path, _page_name(subject, page_index)), 'w') as out_file:
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
                            with element(out_file, 'tr', valign="top", _id=f'{post.sequence_num}'):
                                # with element(f, 'td', _class="alt2", style="border: 1px solid #000063; border-top: 0px; border-bottom: 0px"):
                                with element(out_file, 'td', _class="post"):
                                    with element(out_file, 'a', href=post.user.href):
                                        out_file.write(post.user.name.strip())
                                    out_file.write('<br/>')
                                    out_file.write(format_datetime(post.timestamp))
                                    with element(out_file, 'a', href=post.permalink):
                                        out_file.write('<br/>permalink')
                                    out_file.write(' Post: {:d}'.format(post.sequence_num))
                                with element(out_file, 'td', _class="post"):
                                    out_file.write(post.node.prettify(formatter='html'))
                                    if len(post.liked_by_users) == 1:
                                        with element(out_file, 'p'):
                                            out_file.write(f'{len(post.liked_by_users)} user liked this post.')
                                    elif len(post.liked_by_users) > 1:
                                        with element(out_file, 'p'):
                                            out_file.write(f'{len(post.liked_by_users)} users liked this post.')
                    _write_page_links(subject, page_index, len(pages), out_file)


def write_user_page(
        thread: thread_struct.Thread,
        pass_one_result: PassOneResult,
        user_name: str,
        out_path: str,
) -> None:
    """Writes a specific HTML page for the user posts.
    Each user page has all the posts from that user in order.
    If the post matches any subject then a link is made to that particular post in subject page so the post can be seen
    in context."""
    _posts = pass_one_result.user_ordinal_map[user_name]
    pages = [_posts[i:i + POSTS_PER_PAGE] for i in range(0, len(_posts), POSTS_PER_PAGE)]
    up_votes = sum(len(p.liked_by_users) for p in thread.posts if p.user.name == user_name)
    for page_index, page in enumerate(pages):
        with open(os.path.join(out_path, _page_name('USER_' + user_name, page_index)), 'w') as out_file:
            out_file.write(
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">')
            with element(out_file, 'html', xmlns="http://www.w3.org/1999/xhtml", dir="ltr", lang="en"):
                with element(out_file, 'head'):
                    with element(out_file, 'meta', name='keywords', content='pprune {:s}'.format(user_name)):
                        pass
                    with element(out_file, 'link', rel="stylesheet", type="text/css", href=styles.CSS_FILE):
                        pass
                with element(out_file, 'body'):
                    with element(out_file, 'h1'):
                        out_file.write(
                            'Posts by user "{:s}" [Posts: {:d} Total up-votes: {:d} Pages: {:d}]'.format(
                                user_name, len(_posts), up_votes, len(pages)
                            )
                        )
                    _write_page_links('USER_' + user_name, page_index, len(pages), out_file)
                    # with element(f, 'table', border="0", width="96%", cellpadding="0", cellspacing="0", bgcolor="#FFFFFF", align="center"):
                    with element(out_file, 'table', _class='posts'):
                        for post_index in page:
                            post = thread.posts[post_index]
                            with element(out_file, 'tr', valign="top"):
                                # with element(f, 'td', _class="alt2", style="border: 1px solid #000063; border-top: 0px; border-bottom: 0px"):
                                with element(out_file, 'td', _class="post"):
                                    with element(out_file, 'a', href=post.user.href):
                                        out_file.write(post.user.name.strip())
                                    out_file.write('<br/>')
                                    out_file.write(format_datetime(post.timestamp))
                                    with element(out_file, 'a', href=post.permalink):
                                        out_file.write('<br/>permalink')
                                    out_file.write(' Post: {:d}'.format(post.sequence_num))
                                with element(out_file, 'td', _class="post"):
                                    out_file.write(post.node.prettify(formatter='html'))

                                    # Subjects that this post covers.
                                    with element(out_file, 'p'):
                                        if len(pass_one_result.post_subject_map[post.sequence_num]):
                                            with element(out_file, 'b'):
                                                out_file.write('Subjects')
                                            out_file.write(
                                                ' (links are to this post in the relevant subject page so that this post can be seen in context): '
                                            )
                                            for i, subject in enumerate(
                                                    sorted(pass_one_result.post_subject_map[post.sequence_num])):
                                                if i:
                                                    out_file.write('&nbsp;')
                                                href = pass_one_result.sequence_num_subject_link_map[
                                                    (post.sequence_num, subject)]
                                                with element(out_file, 'a', href=href):
                                                    out_file.write(subject)
                                        else:
                                            with element(out_file, 'b'):
                                                out_file.write('Subjects:')
                                            out_file.write(' None')

                                    if len(post.liked_by_users) == 1:
                                        with element(out_file, 'p'):
                                            out_file.write(f'{len(post.liked_by_users)} user liked this post.')
                                    elif len(post.liked_by_users) > 1:
                                        with element(out_file, 'p'):
                                            out_file.write(f'{len(post.liked_by_users)} users liked this post.')
                    _write_page_links('USER_' + user_name, page_index, len(pages), out_file)


def write_whole_thread(
        thread: thread_struct.Thread,
        common_words: typing.Set[str],
        publication_map: publication_maps.PublicationMap,
        output_path: str
):
    logger.info('Starting write_whole_thread() to %s', output_path)
    t_start = time.perf_counter()
    pass_one_result = pass_one(thread, common_words, publication_map)
    total_posts = 0
    for subject in sorted(pass_one_result.subject_post_map.keys()):
        logger.info('Writing: "{:s}" [{:d}]'.format(subject, len(pass_one_result.subject_post_map[subject])))
        write_a_subject_page(thread, pass_one_result, subject, output_path)
        total_posts += len(pass_one_result.subject_post_map[subject])
    logger.info('Wrote %d posts including duplicates.', total_posts)
    for user_name in sorted(pass_one_result.user_ordinal_map.keys()):
        if len(pass_one_result.user_ordinal_map[user_name]) >= publication_map.get_minimum_number_username_posts():
            logger.info(
                'Writing: user page for "{:s}" [{:d}]'.format(
                    user_name, len(pass_one_result.user_ordinal_map[user_name]))
            )
            write_user_page(thread, pass_one_result, user_name, output_path)
    logger.info('Writing: {:s}'.format('index.html'))
    write_index_page(thread, pass_one_result, publication_map, output_path)
    logger.info('Writing thread done in %.3f (s)', time.perf_counter() - t_start)
