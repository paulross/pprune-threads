import dataclasses
import datetime
import re
import string
import typing

import bs4

# Matches 'http://www.pprune.org/tech-log/423988-concorde-question.html#post5866333'
# Gives one group: ('5866333',)
RE_PERMALINK_TO_POST_NUMBER = re.compile(r'\S+post(\d+)')

# Matches "https://www.pprune.org/members/219249-nicolai"
# To: ("219249", "nicolai")
RE_USER_HREF_TO_USER_ID = re.compile(r'.+?/(\d+)-(\S+)')


@dataclasses.dataclass(frozen=True)
class User:
    """Represents a user. Taken from a node such as:
    <a rel="nofollow" class="bigusername" href="https://www.pprune.org/members/219249-nicolai">nicolai</a>
    """
    href: str
    name: str

    @property
    def user_id(self) -> typing.Optional[str]:
        m = RE_USER_HREF_TO_USER_ID.match(self.href)
        if m:
            return f'{m.group(1)}-{m.group(2)}'

    @property
    def user_int(self) -> typing.Optional[int]:
        m = RE_USER_HREF_TO_USER_ID.match(self.href)
        if m:
            return int(m.group(1))


PUNCTUATION_TABLE = str.maketrans({key: None for key in string.punctuation})


@dataclasses.dataclass
class Post:
    """Represents a single post in a thread."""
    timestamp: datetime.datetime
    permalink: str
    user: User
    node: bs4.element.Tag
    sequence_num: int

    # def __post_init__(self):
    #     """Do some sanity checking on the node.
    #
    #     Expects::
    #
    #         <div id="edit10994338">
    #
    #     """
    #     if self.node.name != 'div':
    #         raise ValueError(f'{self.node.name} does not appear to be a post')
    #     if 'id' not in self.node.attrs:
    #         raise ValueError(f'Node does not have an "id" attribute')
    #     node_id = self.node.attrs['id']
    #     if not node_id.startswith('edit'):
    #         raise ValueError(f'Node "id" atributes does not start with "edit"')
    #     if int(node_id[len('edit')]) != self.sequence_num:
    #         raise ValueError(f'Node "id" attribute "{self.node.attrs['id']}" does not match {self.sequence_num}')
    #     # Check the permalink matches
    #     permalink_node = self.node.find('a', title="Link to this Post")
    #     if permalink_node is None:
    #         raise ValueError(f'no permalink node for {self.permalink}')
    #     permalink = permalink_node.attrs['href']
    #     if permalink != self.permalink:
    #         raise ValueError(f'permalink node href="{permalink}" != {self.permalink}')

    def __str__(self):
        return (
            f'Timestamp: {self.timestamp},'
            f' Permalink: {self.permalink},'
            f' User: {self.user},'
            f' Sequence: {self.sequence_num}'
            # f' Text: {self.text}'
        )

    @property
    def subject(self) -> str:
        """Look for ``<div class="smallfont">`` in::

            <div class="tcell alt1" id="td_post_11003611">

                <!-- icon and title -->
                <div class="smallfont">
                    <strong>BSCU Fault?</strong>
                </div>
                <hr/>
                <!-- / icon and title -->

                <!-- message -->
                <div id="post_message_11003611">
                </div>
                <!-- / message -->
            </div>

        The test is as-is, so not stripped.
        """
        subject_node = self.node.find('div', **{'class': 'smallfont'})
        if subject_node is not None:
            return subject_node.get_text()
        return ''

    @property
    def text(self) -> str:
        """The text in the node, this does not include the subject line.
        From:
        <div id="post_message_10994338">
        """
        text_node = self.node.find('div', **{'id': f'post_message_{self.sequence_num}'})
        if text_node is None:
            raise RuntimeError(f'No text node for post {self.sequence_num}')
        return text_node.get_text()

    @property
    def text_stripped(self) -> str:
        """The text in the node with blank lines and pre/post whitespace removed.
        Inter-word spaces are maintained."""
        ret = []
        for line in self.text.split('\n'):
            line = line.strip()
            if len(line):
                ret.append(line)
        return '\n'.join(ret)

    @property
    def words(self) -> typing.List[str]:
        txt = self.text_stripped.translate(PUNCTUATION_TABLE)
        return txt.split()

    @property
    def post_number(self) -> typing.Optional[int]:
        m = RE_PERMALINK_TO_POST_NUMBER.match(self.permalink)
        if m is not None:
            return int(m.group(1))

    def words_removed(self, remove_these: typing.Set[str], lower_case: bool) -> typing.List[str]:
        """Return the words in the post having removed all specified words and made lower case if required.
        NOTE: The case of remove_these must match lower_case if that it to be effective."""
        result = []
        for w in self.words:
            if lower_case:  # and w.upper() != w:
                w = w.lower()
            if w not in remove_these:
                result.append(w)
        return result

    def cap_words(self, min_size: int) -> typing.List[str]:
        """Return the words in the post that are all capitals with a minimum size."""
        result = []
        for w in self.words:
            if w.upper() == w and len(w) >= min_size:
                result.append(w)
        return result

    def significant_words(self, remove_these: typing.Set[str]) -> typing.List[str]:
        """Return the 'significant' words in the post.
        Ignore a word (lowercase) in remove_these.
        Maintain words that are all uppercase."""
        result = []
        for w in self.words:
            if w.lower() not in remove_these:  # or w.upper() == w:
                result.append(w)
        return result


class Thread:
    """Represents a thread of ordered posts with some internal indexing."""

    def __init__(self):
        # Ordered list of posts
        self.posts: typing.List[Post] = []
        # Map of {permalink : post_ordinal, ...}
        self.post_map: typing.Dict[str, int] = {}
        # Map of {User : [post_ordinal, ...], ...}
        self.user_post_indexes: typing.Dict[User, typing.List[int]] = {}

    def __len__(self) -> int:
        return len(self.posts)

    def __getitem__(self, item) -> Post:
        return self.posts[item]

    def add_post(self, post: Post):
        """Add a post."""
        if post.permalink in self.post_map:
            raise ValueError('permalink already in post_map. Trying to add: {:s}'.format(post.permalink))
        self.post_map[post.permalink] = len(self.posts)
        if post.user not in self.user_post_indexes:
            self.user_post_indexes[post.user] = []
        self.user_post_indexes[post.user].append(len(self.posts))
        self.posts.append(post)

    @property
    def all_users(self) -> typing.Set[User]:
        """All the users in this thread."""
        return set([p.user for p in self.posts])

    def get_post(self, permalink: str) -> Post:
        """Given a permalink this returns the Post object corresponding to that permalink.
        May raise KeyError if the permalink is unknown."""
        return self.posts[self.post_map[permalink]]

    def get_post_ordinals(self, user: User) -> typing.List[int]:
        """Given a user what posts have they made, by ordinal.
        May raise KeyError if user unknown."""
        return self.user_post_indexes[user]
