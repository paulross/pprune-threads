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
import zoneinfo
from contextlib import contextmanager

from pprune.common import styles
from pprune.common import analyse_thread
from pprune.common import thread_struct
from pprune.publication_maps import publication_map_abc

logger = logging.getLogger(__file__)

PUNCTUATION_TABLE = str.maketrans({key: '-' for key in string.punctuation})
POSTS_PER_PAGE = 20
# +/- Links to other pages
PAGE_LINK_COUNT = 10


def get_out_path(thread: str):
    """Return the path of the output directory for the given thread."""
    return os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, 'gh-pages', thread))


@contextmanager
def element(_stream, _name, **attributes):
    """Simple context manager for XML elements."""
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
    """Return a human-readable datetime."""
    if dt.tzinfo is None:
        return dt.strftime('%B %d, %Y, %H:%M:%S')
    gmt = dt.astimezone(zoneinfo.ZoneInfo('GMT'))
    return gmt.strftime('%B %d, %Y, %H:%M:%S %Z')


def format_datetime_as_date(dt: datetime.datetime) -> str:
    """Return a human-readable date, if dt has a timezone it will be converted to GMT."""
    if dt.tzinfo is None:
        return dt.strftime('%B %d, %Y')
    gmt = dt.astimezone(zoneinfo.ZoneInfo('GMT'))
    return gmt.strftime('%B %d, %Y')


def format_date_as_date(dt: datetime.date) -> str:
    """Return a human-readable date."""
    return dt.strftime('%B %d, %Y')


def format_timedelta(td: datetime.timedelta) -> str:
    """Return a human-readable timedelta."""
    return f'{td.days} Days, {td.seconds // 3600} Hours, {(td.seconds % 3600) // 60} Minutes and {td.seconds % 60} Seconds'


class PassOneResult:
    """Collects together some data structures that are used when creating the final output."""

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
        """Adds information about a post. Populated by pass_one().

        :param subjects: The set of subjects this post is categorised in.
        :param post_index: The index of the post in the thread.
        :param sequence_num: The pprune sequence number of the post. This is unique to pprune.
        :param user_name: The name of the user.
        :return: None
        """
        for subject in subjects:
            if subject not in self.subject_post_map:
                self.subject_post_map[subject] = []
            self.subject_post_map[subject].append(post_index)
        self.post_subject_map[sequence_num] = subjects
        self.user_subject_map[user_name.strip()] |= subjects
        self.user_ordinal_map[user_name.strip()].append(post_index)

    def add_sequence_num_subject_link(self, sequence_num: int, subject: str, link: str) -> None:
        """Populated by pass_one()."""
        key = (sequence_num, subject)
        if key in self.sequence_num_subject_link_map:
            raise ValueError(f'Duplicate key {key} in sequence_num_subject_link_map')
        self.sequence_num_subject_link_map[key] = link


def pass_one(
        thread: thread_struct.Thread,
        common_words: typing.Set[str],
        publication_map: publication_map_abc.PublicationMapABC,
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
        if post.sequence_num in publication_map.get_specific_posts_to_subject_map():
            subjects.add(publication_map.get_specific_posts_to_subject_map()[post.sequence_num])
        # Add duplicate subjects, for example: 'RAT (Deployment)': {'RAT (All)', }
        dupe_subjects = set()
        for subject in subjects:
            dupe_subjects |= publication_map.get_duplicate_subjects(subject)
        subjects |= dupe_subjects
        subjects -= publication_map.get_set_of_removed_subjects()
        if post.user is not None:
            pass_one_result.add_subject_post(subjects, i, post.sequence_num, post.user.name.strip())
    # Sanity check, warn if there is a subject with no posts referring to it.
    all_subject_titles = publication_map.get_all_subject_titles()
    for subject_title in sorted(all_subject_titles):
        if subject_title not in pass_one_result.subject_post_map:
            logger.warning('No post with subject title "%s"', subject_title)
    # Add the links from the message sequence number + subject to the planned subject page.
    for subject_title in pass_one_result.subject_post_map.keys():
        post_indicies = pass_one_result.subject_post_map[subject_title]
        pages = [post_indicies[i:i + POSTS_PER_PAGE] for i in range(0, len(post_indicies), POSTS_PER_PAGE)]
        for page_index, page in enumerate(pages):
            for post_index in page:
                post = thread.posts[post_index]
                pass_one_result.add_sequence_num_subject_link(
                    post.sequence_num,
                    subject_title,
                    f'{_page_name(subject_title, page_index)}#{post.sequence_num}',
                )
    logger.info('Pass one complete in %.3f (s)', time.perf_counter() - t_start)
    return pass_one_result


def _page_name(subject, page_num):
    """Creates a name for a page, removing punctuation with '-', replacing spaces with '_' and
    appending the page number."""
    result = subject.translate(PUNCTUATION_TABLE) + '{:d}.html'.format(page_num)
    result = result.replace(' ', '_')
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


def write_index_h1(
        heading: str,
        heading_id: str,
        index: typing.TextIO,
):
    """Writes a <h1> heading with an internal link.

    For example from the Python documentation:

        <span id="re-syntax"></span>
        <h2>Regular Expression Syntax<a class="headerlink" href="#regular-expression-syntax" title="Link to this heading">¶</a></h2>

    The "headerlink" CSS is in basic.css:

        a.headerlink {
        visibility: hidden;
        }

        a:visited {
            color: #551A8B;
        }

        h1:hover > a.headerlink,
        h2:hover > a.headerlink,
        h3:hover > a.headerlink,
        h4:hover > a.headerlink,
        h5:hover > a.headerlink,
        h6:hover > a.headerlink,
        dt:hover > a.headerlink,
        caption:hover > a.headerlink,
        p.caption:hover > a.headerlink,
        div.code-block-caption:hover > a.headerlink {
            visibility: visible;
        }
    """
    heading_id = heading_id.replace(' ', '_').replace('"', '')
    with element(index, 'span', **{'id': heading_id}):
        pass
    with element(index, 'h1'):
        index.write(heading)
        with element(index, 'a',
                     **{'class': "headerlink", "href": f'"#{heading_id}"', 'title': '"Link to this heading"'}):
            index.write('\u00B6')


def write_index_significant_posts(
        thread: thread_struct.Thread,
        publication_map: publication_map_abc.PublicationMapABC,
        index: typing.TextIO,
):
    """Optionally, writes out a list of significant posts."""
    significant_posts = publication_map.get_significant_posts_permalinks()
    if significant_posts:
        write_index_h1('Significant Posts', 'significant_posts', index)
        with element(index, 'p'):
            index.write('These are worth reading before you go any further.')
        # post_ordinals = []
        for subject, post_id in significant_posts:
            if post_id not in thread.post_id_to_permalink_map:
                logger.error('Can not find post_id %s', post_id)
                continue
            permalink = thread.post_id_to_permalink_map[post_id]
            if permalink not in thread.post_map:
                logger.error('Can not find permalink %s', permalink)
                continue
            post_ordinal = thread.post_map[permalink]
            if post_ordinal < len(thread):
                with element(index, 'ul'):
                    post = thread.posts[post_ordinal]
                    with element(index, 'li'):
                        index.write(
                            f'Permalink: <a href="{post.permalink}">{subject}</a>'
                            f' User: <a href="{post.user.href}">{post.user.name}</a>'
                        )
            else:
                logger.warning(f'Can not write post {post_ordinal} most likely due to --limit-posts')


def write_index_main_subject_table(
        subject_post_map: typing.Dict[str, typing.List[int]],
        index: typing.TextIO,
):
    """Write out the main table of subjects."""
    if len(subject_post_map):
        write_index_h1('Posts by Subject', 'posts_by_subject', index)
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


def write_index_removed_subjects(
        publication_map: publication_map_abc.PublicationMapABC,
        index: typing.TextIO,
):
    """If there are removed subjects then list them here in tabular form."""
    removed_subjects = sorted(publication_map.get_set_of_removed_subjects())
    if removed_subjects:
        write_index_h1('Removed Subjects', 'removed_subjects', index)
        with element(index, 'p'):
            index.write('These are subjects that have been removed from previous versions of this build.')
        with element(index, 'table', _class="indextable"):
            COLUMNS = 4
            rows = [removed_subjects[i:i + COLUMNS] for i in range(0, len(removed_subjects), COLUMNS)]
            subject_index = 0
            for row in rows:
                with element(index, 'tr'):
                    for _cell in row:
                        subject = removed_subjects[subject_index]
                        with element(index, 'td', _class='indextable'):
                            index.write(subject)
                        subject_index += 1


def write_index_most_upvoted_posts_table(
        thread: thread_struct.Thread,
        publication_map: publication_map_abc.PublicationMapABC,
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
        write_index_h1(f'The {post_count} Most Up-voted Posts', 'most_upvoted_posts', index)
        with element(index, 'p'):
            index.write(
                'This list the posts that have the largest number of up-votes.'
                ' They are <i>likely</i> to be more important than others.'
                f' There are {total_upvotes:d} up-votes on {len(thread.posts)} posts.'
                ' "User Name" links are to the pprune user.'
                ' "Permalink" links is to the post on pprune.'
            )
        with element(index, 'p'):
            index.write('NOTE: Up-votes from closed threads maybe lost.')
        post_count = 0
        with element(index, 'table', _class="indextable"):
            _write_table_header(['Up-votes', 'Start Text (Quoted Text Removed)', 'User Name', 'Date', 'Permalink', ],
                                index)
            for k in keys:
                for post_ordinal in liked_by_users_dict[k]:
                    post = thread.posts[post_ordinal]
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write(f'{len(post.liked_by_users)}')
                        post_text = post.text_stripped_without_quoted_message.replace('\n', ' ')
                        if len(post_text) > publication_map.get_upvoted_post_text_limit():
                            post_text = post_text[:publication_map.get_upvoted_post_text_limit()]
                            post_text += '&nbsp;&#8230;'
                        if len(post_text) == 0:
                            post_text = 'N/A'
                        with element(index, 'td', _class='indextable'):
                            index.write(post_text)
                        with element(index, 'td', _class='indextable'):
                            with element(index, 'a', href=post.user.href):
                                index.write(post.user.name)
                        with element(index, 'td', _class='indextable'):
                            index.write(format_datetime(post.timestamp))
                        with element(index, 'td', _class='indextable'):
                            with element(index, 'a', href=post.permalink):
                                index.write('Permalink')
                    post_count += 1
                    if post_count >= publication_map.get_upvoted_post_count_limit():
                        break
                if post_count >= publication_map.get_upvoted_post_count_limit():
                    break
    else:
        logger.warning('Can not read up-votes from the thread. Is the thread closed (up-votes will not show)?')
        write_index_h1(f'The Most Up-voted Posts', 'most_upvoted_posts', index)
        with element(index, 'p'):
            index.write('This is not available, perhaps because the thread is closed.')


def _write_table_header(headers: typing.List[str], index: typing.TextIO):
    """Write the header row with <th> elements."""
    with element(index, 'tr'):
        for header in headers:
            with element(index, 'th', _class='indextable'):
                index.write(header)


def write_index_user_subject_table(
        thread: thread_struct.Thread,
        user_subject_map: typing.Dict[str, typing.Set[str]],
        publication_map: publication_map_abc.PublicationMapABC,
        index: typing.TextIO,
):
    """Posts by user, including the subjects they covered."""
    write_index_h1(f'Posts by User on a Subject', 'posts_by_user_subject', index)
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
    with element(index, 'p'):
        index.write('NOTE: Up-votes from closed threads maybe lost.')
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
        publication_map: publication_map_abc.PublicationMapABC,
        index: typing.TextIO,
):
    """Write a table with links to pages that have all user posts."""
    write_index_h1(f'Users Posts', 'posts_by_users', index)
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


# See: https://www.w3schools.com/charsets/ref_utf_geometric.asp
# Black square.
HISTOGRAM_CHARACTER = '&#x25A0;'


def write_index_histogram(
        heading: str,
        heading_id: str,
        intro: str,
        col_one_heading: str,
        table: typing.List[typing.Tuple[str, int]],
        divisor: int,
        index: typing.TextIO,
):
    """Writes a histogram table of posts typically over time such as date or hour of day.
    """
    write_index_h1(heading, heading_id, index)
    with element(index, 'p'):
        index.write(
            f'{intro} Each {HISTOGRAM_CHARACTER} represents {divisor} posts.'
        )
    with element(index, 'table', _class="indextable"):
        _write_table_header([col_one_heading, 'Post Count', 'Histogram', ], index)
        for name, post_count in table:
            with element(index, 'tr'):
                with element(index, 'td', _class='indextable'):
                    index.write(f'{name}')
                with element(index, 'td', _class='indextable'):
                    index.write(f'{post_count}')
                with element(index, 'td', _class='indextable'):
                    with element(index, 'tt'):
                        index.write(f'{HISTOGRAM_CHARACTER * (post_count // divisor)}')


def write_index_post_date_histogram(
        thread: thread_struct.Thread,
        publication_map: publication_map_abc.PublicationMapABC,
        index: typing.TextIO,
):
    """Writes a histogram table of posts by date."""
    post_count = collections.Counter()
    for post in thread.posts:
        td = post.timestamp - thread.posts[0].timestamp
        post_count[td.days] += 1
    max_daily_posts = max(post_count.values())
    divisor = 1 + max_daily_posts // 80
    table = []
    for day_inc in range(min(post_count.keys()), max(post_count.keys()) + 1):
        this_timestamp = thread.posts[0].timestamp + datetime.timedelta(days=day_inc)
        if publication_map.include_empty_post_dates_in_histogram() or post_count[day_inc]:
            table.append((format_datetime_as_date(this_timestamp), post_count[day_inc]))
    text = 'Here are the number of posts by date.'
    if publication_map.include_empty_post_dates_in_histogram():
        text += ' All dates are included even if there are no posts.'
    else:
        text += ' Only dates are included if there are posts.'
    write_index_histogram(
        'Number of Posts by Date (GMT)',
        'posts_by_date',
        text,
        'Date',
        table, divisor, index
    )


def write_index_post_time_histogram(
        thread: thread_struct.Thread,
        publication_map: publication_map_abc.PublicationMapABC,
        index: typing.TextIO,
):
    """Write a table with a histogram of posts by time of day (GMT)."""
    post_count = collections.Counter()
    for post in thread.posts:
        post_count[post.timestamp.hour] += 1
    max_daily_posts = max(post_count.values())
    divisor = 1 + max_daily_posts // 80
    table = []
    for hour in range(24):
        table.append((f'{hour}', post_count[hour],))
    write_index_histogram(
        'Number of Posts by Time of Day (GMT)',
        'posts_by_hour',
        'Here are the number of posts by time of day (GMT).',
        'Hour',
        table, divisor, index
    )


def write_index_page(
        thread: thread_struct.Thread,
        pass_one_result: PassOneResult,
        publication_map: publication_map_abc.PublicationMapABC,
        out_path: str,
):
    """Write the index.html page."""
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
                write_index_h1(publication_map.get_title(), 'introduction', index)
                with element(index, 'p'):
                    index.write(publication_map.get_introduction_in_html())
                with element(index, 'p'):
                    index.write(f"""These threads have {len(thread)} posts.
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
                # Write table of informational data.
                posts_inc, posts_exc = get_count_of_posts_included(thread, pass_one_result.subject_post_map)
                posts_in_open_threads = 0
                for post in thread.posts:
                    if post.thread_is_open:
                        posts_in_open_threads += 1
                with element(index, 'table', _class="indextable"):
                    with element(index, 'tr'):
                        with element(index, 'th'):
                            index.write('Info')
                        with element(index, 'th'):
                            index.write('Value')
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('Total posts')
                        with element(index, 'td', _class='indextable'):
                            index.write(f'{len(thread)}')
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('Posts in currently open threads')
                        with element(index, 'td', _class='indextable'):
                            index.write(
                                f'{posts_in_open_threads}'
                                f' ({posts_in_open_threads / len(thread):.1%})'
                            )
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('Posts in currently closed threads')
                        with element(index, 'td', _class='indextable'):
                            index.write(
                                f'{len(thread) - posts_in_open_threads}'
                                f' ({(len(thread) - posts_in_open_threads) / len(thread):.1%})'
                            )
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('Posts included')
                        with element(index, 'td', _class='indextable'):
                            index.write(f'{posts_inc} ({posts_inc / len(thread):.1%})')
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('Posts excluded')
                        with element(index, 'td', _class='indextable'):
                            index.write(f'{posts_exc} ({posts_exc / len(thread):.1%})')
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('Thread starts at')
                        with element(index, 'td', _class='indextable'):
                            index.write(
                                f'{format_datetime(thread.posts[0].timestamp)}'
                                f' '
                            )
                            with element(index, 'a', href=thread.posts[0].permalink):
                                index.write('First Post')
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('Thread finishes at')
                        with element(index, 'td', _class='indextable'):
                            index.write(
                                f'{format_datetime(thread.posts[-1].timestamp)}'
                                f' '
                            )
                            with element(index, 'a', href=thread.posts[-1].permalink):
                                index.write('Last Post')
                            index.write(
                                f' (Elapsed: {format_timedelta(thread.posts[-1].timestamp - thread.posts[0].timestamp)})'
                            )
                    with element(index, 'tr'):
                        with element(index, 'td', _class='indextable'):
                            index.write('This build')
                        with element(index, 'td', _class='indextable'):
                            datetime_now = datetime.datetime.now(tz=zoneinfo.ZoneInfo('GMT'))
                            index.write(
                                f'{format_datetime(datetime_now)}'
                                f' (From last post: {format_timedelta(datetime_now - thread.posts[-1].timestamp)})'
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

                write_index_removed_subjects(publication_map, index)

                write_index_most_upvoted_posts_table(thread, publication_map, index)

                write_index_user_subject_table(thread, pass_one_result.user_subject_map, publication_map, index)

                write_index_user_post_table(thread, pass_one_result.user_ordinal_map, publication_map, index)

                write_index_post_date_histogram(thread, publication_map, index)

                write_index_post_time_histogram(thread, publication_map, index)


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
                    heading_str = 'Posts about: "{:s}" [Posts: {:d} Page: {:d} of {:d}]'.format(
                        subject, len(_posts), page_index + 1, len(pages),
                    )
                    heading_id_str = f'{subject}_{page_index + 1}'
                    write_index_h1(heading_str, heading_id_str, out_file)

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
                                    if post.thread_is_open:
                                        if len(post.liked_by_users) == 1:
                                            with element(out_file, 'p'):
                                                with element(out_file, 'b'):
                                                    out_file.write(f'{len(post.liked_by_users)} user liked this post.')
                                        elif len(post.liked_by_users) > 1:
                                            with element(out_file, 'p'):
                                                with element(out_file, 'b'):
                                                    out_file.write(f'{len(post.liked_by_users)} users liked this post.')
                                        with element(out_file, 'p'):
                                            # https://www.pprune.org/newreply.php?do=newreply&p=11926646
                                            target_url = f'https://www.pprune.org/newreply.php?do=newreply&p={post.sequence_num}'
                                            with element(out_file, 'a', href=target_url):
                                                out_file.write(f'Reply to this quoting this original post.')
                                            out_file.write('You need to be logged in. Not available on closed threads.')
                                    else:
                                        with element(out_file, 'p'):
                                            with element(out_file, 'b'):
                                                out_file.write(
                                                    'The thread is closed so there are no user likes are available.')
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
    up_votes = sum(len(p.liked_by_users) for p in thread.posts if p.user is not None and p.user.name == user_name)
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
                    heading_str = 'Posts by user "{:s}" [Posts: {:d} Total up-votes: {:d} Page: {:d} of {:d}]'.format(
                        user_name, len(_posts), up_votes, page_index + 1, len(pages)
                    )
                    heading_id_str = f'User_{user_name}_{page_index + 1}'
                    write_index_h1(heading_str, heading_id_str, out_file)

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
        publication_map: publication_map_abc.PublicationMapABC,
        output_path: str
):
    """This is the main entry point for writing out the results."""
    logger.info('Starting write_whole_thread() to %s', output_path)
    t_start = time.perf_counter()
    pass_one_result = pass_one(thread, common_words, publication_map)
    total_posts = 0
    # Write out the subject pages.
    for subject in sorted(pass_one_result.subject_post_map.keys()):
        logger.info('Writing: "{:s}" [{:d}]'.format(subject, len(pass_one_result.subject_post_map[subject])))
        write_a_subject_page(thread, pass_one_result, subject, output_path)
        total_posts += len(pass_one_result.subject_post_map[subject])
    logger.info('Wrote %d posts including duplicates.', total_posts)
    # Write out the user pages.
    for user_name in sorted(pass_one_result.user_ordinal_map.keys()):
        if len(pass_one_result.user_ordinal_map[user_name]) >= publication_map.get_minimum_number_username_posts():
            logger.info(
                'Writing: user page for "{:s}" [{:d}]'.format(
                    user_name, len(pass_one_result.user_ordinal_map[user_name]))
            )
            write_user_page(thread, pass_one_result, user_name, output_path)
    logger.info('Writing: {:s}'.format('index.html'))
    # Write out the index page.
    write_index_page(thread, pass_one_result, publication_map, output_path)
    # Print out a histogram of subject -> count of posts.
    subject_counter = collections.Counter()
    for subject in pass_one_result.subject_post_map:
        subject_counter[subject] = len(pass_one_result.subject_post_map[subject])
        # for _post in pass_one_result.subject_post_map[subject]:
        #     subject_counter.update([subject])
    # print(subject_counter)
    print('Subjects by size:')
    for k, v in subject_counter.most_common():
        print(f'{k:40} [{v:3d}]: {"+" * v}')
    logger.info('Writing thread done in %.3f (s)', time.perf_counter() - t_start)
