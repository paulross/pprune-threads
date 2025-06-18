import datetime

import pytest

from pprune.common import thread_struct


@pytest.mark.parametrize(
    'permalink, expected',
    (
            ('http://www.pprune.org/tech-log/423988-concorde-question.html#post5866333', ('5866333',)),
    )
)
def test_RE_PERMALINK_TO_POST_NUMBER(permalink, expected):
    m = thread_struct.RE_PERMALINK_TO_POST_NUMBER.match(permalink)
    assert m is not None
    assert m.groups() == expected


@pytest.mark.parametrize(
    'href, expected',
    (
            ("https://www.pprune.org/members/219249-nicolai", ('219249', 'nicolai')),
    )
)
def test_RE_USER_HREF_TO_USER_ID(href, expected):
    m = thread_struct.RE_USER_HREF_TO_USER_ID.match(href)
    assert m is not None
    assert m.groups() == expected


@pytest.mark.parametrize(
    'href, name, expected',
    (
            ("https://www.pprune.org/members/219249-nicolai", 'nicolai', '219249-nicolai'),
    )
)
def test_user_user_id(href, name, expected):
    user = thread_struct.User(href, name)
    assert user.user_id == expected


@pytest.mark.parametrize(
    'href, name, expected',
    (
            ("https://www.pprune.org/members/219249-nicolai", 'nicolai', 219249),
    )
)
def test_user_user_int(href, name, expected):
    user = thread_struct.User(href, name)
    assert user.user_int == expected


@pytest.mark.parametrize(
    'href, name',
    (
            ("https://www.pprune.org/members/219249-nicolai", 'nicolai',),
    )
)
def test_user_hashable(href, name):
    user = thread_struct.User(href, name)
    hash(user)


# NOTE: Typical permalink: "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338"

@pytest.mark.parametrize(
    'args, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This is the post text.",
                            42,  # Sequence number
                    ),
                    'Timestamp: 2020-01-01 05:32:14, Permalink: https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338, User: nicolai, Sequence: 42',
            ),
    )
)
def test_post_ctor(args, expected):
    post = thread_struct.Post(*args)
    print()
    print(post)
    assert str(post) == expected


@pytest.mark.parametrize(
    'args, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This is the post text.",
                            42,  # Sequence number
                    ),
                    'This is the post text.',
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            """
                            This is the post text.
                            
                            
                            """,
                            42,  # Sequence number
                    ),
                    'This is the post text.',
            ),
            # Check inter-word spacing.
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This   is    the post text.",
                            42,  # Sequence number
                    ),
                    'This   is    the post text.',
            ),
    )
)
def test_post_text_stripped(args, expected):
    post = thread_struct.Post(*args)
    assert post.text_stripped == expected


@pytest.mark.parametrize(
    'args, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This, is the post text. See:",
                            42,  # Sequence number
                    ),
                    ['This', 'is', 'the', 'post', 'text', 'See', ],
            ),
    )
)
def test_post_words(args, expected):
    post = thread_struct.Post(*args)
    assert post.words == expected


@pytest.mark.parametrize(
    'args, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This, is the post text. See:",
                            42,  # Sequence number
                    ),
                    10994338,
            ),
    )
)
def test_post_post_number(args, expected):
    post = thread_struct.Post(*args)
    assert post.post_number == expected


@pytest.mark.parametrize(
    'args, remove_these, lower_case, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This, is the post text. See:",
                            42,  # Sequence number
                    ),
                    set(),
                    True,
                    ['this', 'is', 'the', 'post', 'text', 'see'],
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This, is the post text. See:",
                            42,  # Sequence number
                    ),
                    set(),
                    False,
                    ['This', 'is', 'the', 'post', 'text', 'See'],
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This, is the post text. See:",
                            42,  # Sequence number
                    ),
                    {'this', 'the'},
                    True,
                    ['is', 'post', 'text', 'see'],
            ),
            # Example of when lower_case is False and the remove_these set is lower case. Some removal.
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            "This, is the post text. See:",
                            42,  # Sequence number
                    ),
                    {'this', 'the'},
                    False,
                    ['This', 'is', 'post', 'text', 'See'],
            ),
    )
)
def test_post_words_removed(args, remove_these, lower_case, expected):
    post = thread_struct.Post(*args)
    assert post.words_removed(remove_these, lower_case) == expected


EXAMPLE_THREAD_POSTS_SINGLE = [
    (
        datetime.datetime(2020, 1, 1, 5, 32, 14),
        # permalink
        "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
        'nicolai',
        "This, is the post text. See:",
        42,  # Sequence number
    ),
]


def test_thread_posts_single():
    post = thread_struct.Post(*EXAMPLE_THREAD_POSTS_SINGLE[0])
    assert post


EXAMPLE_THREAD_POSTS_TWO = [
    (
        datetime.datetime(2020, 1, 1, 5, 32, 14),
        # permalink
        "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
        'nicolai',
        "This, is the post text. See:",
        42,  # Sequence number
    ),
    (
        datetime.datetime(2020, 1, 1, 5, 32, 28),
        # permalink
        "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994339",
        'not-nicolai',
        "Totally different text.",
        142,  # Sequence number
    ),
]


@pytest.mark.parametrize(
    'posts, expected',
    (
            (EXAMPLE_THREAD_POSTS_SINGLE, 1,),
            (EXAMPLE_THREAD_POSTS_TWO, 2,),
    )
)
def test_thread(posts, expected):
    thread = thread_struct.Thread()
    for post_args in posts:
        thread.add_post(thread_struct.Post(*post_args))
    assert len(thread) == expected


@pytest.mark.parametrize(
    'posts, expected',
    (
            (EXAMPLE_THREAD_POSTS_SINGLE, {'nicolai'},),
            (EXAMPLE_THREAD_POSTS_TWO, {'not-nicolai', 'nicolai'},),
    )
)
def test_thread_all_users(posts, expected):
    thread = thread_struct.Thread()
    for post_args in posts:
        thread.add_post(thread_struct.Post(*post_args))
    assert thread.all_users == expected


@pytest.mark.parametrize(
    'posts, permalink, expected',
    (
            (
                    EXAMPLE_THREAD_POSTS_SINGLE,
                    "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                    thread_struct.Post(*EXAMPLE_THREAD_POSTS_SINGLE[0]),
            ),
    )
)
def test_thread_get_post(posts, permalink, expected):
    thread = thread_struct.Thread()
    for post_args in posts:
        thread.add_post(thread_struct.Post(*post_args))
    assert thread.get_post(permalink) == expected


@pytest.mark.parametrize(
    'posts, permalink, expected',
    (
            (
                    EXAMPLE_THREAD_POSTS_SINGLE,
                    "Some stuff",
                    "Some stuff",
            ),
    )
)
def test_thread_get_post_raises(posts, permalink, expected):
    thread = thread_struct.Thread()
    for post_args in posts:
        thread.add_post(thread_struct.Post(*post_args))
    with pytest.raises(KeyError) as err:
        thread.get_post(permalink)
    assert err.value.args[0] == expected


@pytest.mark.parametrize(
    'posts, user, expected',
    (
            (EXAMPLE_THREAD_POSTS_SINGLE, 'nicolai', [0,]),
            (EXAMPLE_THREAD_POSTS_TWO, 'nicolai', [0,]),
            (EXAMPLE_THREAD_POSTS_TWO, 'not-nicolai', [1,]),
    )
)
def test_thread_get_post_ordinals(posts, user, expected):
    thread = thread_struct.Thread()
    for post_args in posts:
        thread.add_post(thread_struct.Post(*post_args))
    assert thread.get_post_ordinals(user) == expected


@pytest.mark.parametrize(
    'posts, user, expected',
    (
            (EXAMPLE_THREAD_POSTS_SINGLE, 'foo', 'foo',),
    )
)
def test_thread_get_post_ordinals_raises(posts, user, expected):
    thread = thread_struct.Thread()
    for post_args in posts:
        thread.add_post(thread_struct.Post(*post_args))
    with pytest.raises(KeyError) as err:
        thread.get_post_ordinals(user)
    assert err.value.args[0] == expected


