import datetime

import bs4
import pytest
from pprune.common import thread_struct


@pytest.mark.parametrize(
    'attr, expected',
    (
            ('href', "https://www.pprune.org/members/219249-nicolai"),
            ('name', "nicolai"),
            ('user_id', "219249-nicolai"),
            ('user_int', 219249),
    )
)
def test_user_attributes(attr, expected):
    user = thread_struct.User(href="https://www.pprune.org/members/219249-nicolai", name="nicolai")
    assert hasattr(user, attr)
    assert getattr(user, attr) == expected


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


EXAMPLE_SINGLE_PPRUNE_POST = """<!-- post #10994338 -->
<div id="edit10994338">
    <!-- this is not the last post shown on the page -->

    <div id="post10994338">
        <div class="tpost">

            <div class="trow-group">
                <div class="trow thead smallfont">
                    <div class="tcell" style="width:175px;">
                        <!-- status icon and date -->
                        <a name="post10994338">
                            <img class="inlineimg" src="https://www.pprune.org/images/statusicon/post_old.gif" alt="Old"/>
                        </a>

                                            20th Feb 2021, 22:11

                                            <!-- / status icon and date -->
                    </div>
                    <div class="tcell text-right">

                                            &nbsp;
                                            #
                        <a href="https://www.pprune.org/10994338-post1.html" target="new" id="postcount10994338" name="1">
                            <strong>1</strong>
                        </a>
                         (
                        <b>
                            <a href="https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338" title="Link to this Post">permalink</a>
                        </b>
                        ) &nbsp;


                    </div>
                </div>

                <div class="trow">
                    <div class="tcell alt2" style="width:175px;">
                        <script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"nicolai","memberOf":"Registered Member","url":"https://www.pprune.org/member.php?u=219249"}</script>
                        <div id="postmenu_10994338">

                            <a rel="nofollow" class="bigusername" href="https://www.pprune.org/members/219249-nicolai">nicolai</a>
                            <script type="2054ed5ceb28d642617005d7-text/javascript">
                            vbmenu_register("postmenu_10994338", true);
                            </script>

                        </div>

                        <div class="smallfont">
                            <span class="alt2 threadstarter">Thread Starter</span>
                        </div>

                        <div class="smallfont">

                                                    &nbsp;
                            <br/>
                            <div>Join Date: Jan 2008</div>
                            <div>Location: It used to be an island...</div>

                            <div>
                                                        Posts: 233
                                                    </div>

                            <div></div>
                        </div>

                    </div>

                    <div class="tcell alt1" id="td_post_10994338">

                        <!-- icon and title -->
                        <div class="smallfont">

                            <strong>United B777 engine failure</strong>
                        </div>
                        <hr/>
                        <!-- / icon and title -->

                        <!-- message -->
                        <div id="post_message_10994338">


                                                    Reports on Twitter that a UAL 777-200 has had an uncontained engine failure on the way from DEN (Denver, Colorado, USA) to HNL (Honolulu, Hawai'i, USA) and returned safely to DEN. Local news report:
                            <a href="https://thepostmillennial.com/colorado-residents-shocked-falling-debris-united-airlines" target="_blank">https://thepostmillennial.com/colora...nited-airlines</a>
                            <br/>
                            <br/>
                             There's a twitter post by user @stillgray with video of the failed engine from in the aircraft that PPRuNe doesn't seem to want to include here...
                            <br/>
                            <br/>
                            <img src="https://cimg6.ibsrv.net/gimg/pprune.org-vbulletin/800x400/1613859028_bfa90ab22ac53d454b9d408b228b58c1bbed57fd.jpeg" alt="" class="post_inline_image"/>
                            <br/>
                            <i>UAL 777</i>
                            <br/>
                            <img src="https://cimg0.ibsrv.net/gimg/pprune.org-vbulletin/2000x1504/eusp_qruuaiubbl_jpeg_3753a703c961585ca56d2e7fcd59348e31d1b385.jpg" alt="" class="post_inline_image"/>
                            <br/>
                            <i>Ground debris</i>
                            <br/>

                        </div>
                        <!-- / message -->

                    </div>
                </div>
                <div class="trow">
                    <div class="tcell alt2">
                        <img class="inlineimg" src="https://www.pprune.org/images/statusicon/user_offline.gif" alt="nicolai is offline"/>

                        <a href="https://www.pprune.org/report.php?p=10994338" rel="nofollow">
                            <img class="inlineimg" src="https://www.pprune.org/images/buttons/report.gif" alt="Report Post"/>
                        </a>


                                            &nbsp;

                    </div>

                    <div class="tcell alt1 text-right">
                        <!-- controls -->

                        <a class="button hollow primary" href="https://www.pprune.org/newreply.php?do=newreply&amp;p=10994338" rel="nofollow">
                            <i class="fas fa-quote-right"></i>
                             Quote
                        </a>

                        <a class="button hollow primary" href="https://www.pprune.org/newreply.php?do=newreply&amp;p=10994338" rel="nofollow" id="qr_10994338" onclick="if (!window.__cfRLUnblockHandlers) return false; return false" data-cf-modified-2054ed5ceb28d642617005d7-="">
                            <i class="fas fa-bolt"></i>
                             Quick Reply
                        </a>

                        <!-- / controls -->
                    </div>
                </div>
            </div>
            <!-- trow-group -->
        </div>
        <!-- tbox -->
    </div>

    <!-- post 10994338 popup menu -->
    <div class="vbmenu_popup" id="postmenu_10994338_menu" style="display:none">
        <div class="tbox">
            <div class="trow thead">
                <div class="tcell">nicolai</div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a rel="nofollow" href="https://www.pprune.org/members/219249-nicolai">View Public Profile</a>
                </div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a href="https://www.pprune.org/private.php?do=newpm&amp;u=219249" rel="nofollow">Send a private message to nicolai</a>
                </div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a href="https://www.pprune.org/search.php?do=finduser&amp;u=219249" rel="nofollow">Find More Posts by nicolai</a>
                </div>
            </div>

            <div class="trow">
                <div class="tcell vbmenu_option">
                    <a rel="nofollow" href="https://www.pprune.org/profile.php?do=addlist&amp;userlist=buddy&amp;u=219249">Add nicolai to Your Contacts</a>
                </div>
            </div>

        </div>
    </div>
    <!-- / post 10994338 popup menu -->

</div>

<!-- / post #10994338 -->
"""

EXAMPLE_SINGLE_PPRUNE_POST_MINIMAL_TEXT = """<!-- post #10994338 -->
<div id="edit10994338">
  <!-- this is not the last post shown on the page -->
  <div id="post10994338">
    <div class="tpost">
      <div class="trow-group">
        <div class="trow thead smallfont">
          <div class="tcell" style="width:175px;">
          <!-- status icon and date -->
          <a name="post10994338">
            <img class="inlineimg" src="https://www.pprune.org/images/statusicon/post_old.gif" alt="Old" />
          </a>20th Feb 2021, 22:11 
          <!-- / status icon and date --></div>
          <div class="tcell text-right">&#160; # 
          <a href="https://www.pprune.org/10994338-post1.html" target="new" id="postcount10994338" name="1">
            <strong>1</strong>
          </a>( 
          <b>
            <a href="https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338" title="Link to this Post">permalink</a>
          </b>) &#160;</div>
        </div>
        <div class="trow">
          <div class="tcell alt2" style="width:175px;">
            <script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"nicolai","memberOf":"Registered Member","url":"https://www.pprune.org/member.php?u=219249"}</script>
            <div id="postmenu_10994338">
              <a rel="nofollow" class="bigusername" href="https://www.pprune.org/members/219249-nicolai">nicolai</a>
              <script type="2054ed5ceb28d642617005d7-text/javascript">vbmenu_register("postmenu_10994338", true);</script>
            </div>
            <div class="smallfont">
              <span class="alt2 threadstarter">Thread Starter</span>
            </div>
            <div class="smallfont">&#160; 
            <br />
            <div>Join Date: Jan 2008</div>
            <div>Location: It used to be an island...</div>
            <div>Posts: 233</div>
            <div></div></div>
          </div>
          <div class="tcell alt1" id="td_post_10994338">
            <!-- icon and title -->
            <div class="smallfont">
              <strong>United B777 engine failure</strong>
            </div>
            <hr />
            <!-- / icon and title -->
            <!-- message -->
            <div id="post_message_10994338">Minimal text in this post.</div>
            <!-- / message -->
          </div>
        </div>
        <div class="trow">
          <div class="tcell alt2">
          <img class="inlineimg" src="https://www.pprune.org/images/statusicon/user_offline.gif" alt="nicolai is offline" />
          <a href="https://www.pprune.org/report.php?p=10994338" rel="nofollow">
            <img class="inlineimg" src="https://www.pprune.org/images/buttons/report.gif" alt="Report Post" />
          </a>&#160;</div>
          <div class="tcell alt1 text-right">
            <!-- controls -->
            <a class="button hollow primary" href="https://www.pprune.org/newreply.php?do=newreply&amp;p=10994338" rel="nofollow">
            <i class="fas fa-quote-right"></i>Quote</a>
            <a class="button hollow primary" href="https://www.pprune.org/newreply.php?do=newreply&amp;p=10994338" rel="nofollow" id="qr_10994338" onclick="if (!window.__cfRLUnblockHandlers) return false; return false" data-cf-modified-2054ed5ceb28d642617005d7-="">
            <i class="fas fa-bolt"></i>Quick Reply</a>
            <!-- / controls -->
          </div>
        </div>
      </div>
      <!-- trow-group -->
    </div>
    <!-- tbox -->
  </div>
  <!-- post 10994338 popup menu -->
  <div class="vbmenu_popup" id="postmenu_10994338_menu" style="display:none">
    <div class="tbox">
      <div class="trow thead">
        <div class="tcell">nicolai</div>
      </div>
      <div class="trow">
        <div class="tcell vbmenu_option">
          <a rel="nofollow" href="https://www.pprune.org/members/219249-nicolai">View Public Profile</a>
        </div>
      </div>
      <div class="trow">
        <div class="tcell vbmenu_option">
          <a href="https://www.pprune.org/private.php?do=newpm&amp;u=219249" rel="nofollow">Send a private message to nicolai</a>
        </div>
      </div>
      <div class="trow">
        <div class="tcell vbmenu_option">
          <a href="https://www.pprune.org/search.php?do=finduser&amp;u=219249" rel="nofollow">Find More Posts by nicolai</a>
        </div>
      </div>
      <div class="trow">
        <div class="tcell vbmenu_option">
          <a rel="nofollow" href="https://www.pprune.org/profile.php?do=addlist&amp;userlist=buddy&amp;u=219249">Add nicolai to Your Contacts</a>
        </div>
      </div>
    </div>
  </div>
  <!-- / post 10994338 popup menu -->
</div>
<!-- / post #10994338 -->
"""


def parse_string(html_string: str, features: str) -> bs4.element.Tag:
    parse_tree = bs4.BeautifulSoup(html_string, features=features)
    return parse_tree


# NOTE: Typical permalink: "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338"

@pytest.mark.parametrize(
    'args, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    'Timestamp: 2020-01-01 05:32:14, Permalink: https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338, User: nicolai, Sequence: 10994338',
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST, 'html.parser'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    'Timestamp: 2020-01-01 05:32:14, Permalink: https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338, User: nicolai, Sequence: 10994338',
            ),
    )
)
def test_post_ctor(args, expected):
    post = thread_struct.Post(*args)
    print()
    print(post)
    print(post.text_stripped)
    print(post.words)
    assert str(post) == expected


@pytest.mark.parametrize(
    'args, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    (
                            'Reports on Twitter that a UAL 777-200 has had an uncontained engine failure '
                            "on the way from DEN (Denver, Colorado, USA) to HNL (Honolulu, Hawai'i, USA) "
                            'and returned safely to DEN. Local news report:\n'
                            'https://thepostmillennial.com/colora...nited-airlines\n'
                            "There's a twitter post by user @stillgray with video of the failed engine "
                            "from in the aircraft that PPRuNe doesn't seem to want to include here...\n"
                            'UAL 777\n'
                            'Ground debris'
                    ),
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
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST_MINIMAL_TEXT, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    ['Minimal', 'text', 'in', 'this', 'post'],
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST_MINIMAL_TEXT, 'html.parser'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    ['Minimal', 'text', 'in', 'this', 'post'],
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
                            [],  # liked_by_users
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
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST_MINIMAL_TEXT, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    set(),
                    True,
                    ['minimal', 'text', 'in', 'this', 'post'],
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST_MINIMAL_TEXT, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    set(),
                    False,
                    ['Minimal', 'text', 'in', 'this', 'post'],
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST_MINIMAL_TEXT, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    {'this', 'the'},
                    True,
                    ['minimal', 'text', 'in', 'post'],
            ),
            # Example of when lower_case is False and the remove_these set is lower case. Some removal.
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST_MINIMAL_TEXT, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    {'this', 'the'},
                    False,
                    ['Minimal', 'text', 'in', 'post'],
            ),
    )
)
def test_post_words_removed(args, remove_these, lower_case, expected):
    post = thread_struct.Post(*args)
    assert post.words_removed(remove_these, lower_case) == expected


@pytest.mark.parametrize(
    'args, min_size, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    0,
                    ['UAL', '777200', 'DEN', 'USA', 'HNL', 'USA', 'DEN', 'UAL', '777', ],
            ),
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    4,
                    ['777200', ],
            ),
    )
)
def test_post_cap_words(args, min_size, expected):
    post = thread_struct.Post(*args)
    assert post.cap_words(min_size) == expected


@pytest.mark.parametrize(
    'args, remove_these, expected',
    (
            (
                    (
                            datetime.datetime(2020, 1, 1, 5, 32, 14),
                            "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
                            'nicolai',
                            parse_string(EXAMPLE_SINGLE_PPRUNE_POST, 'lxml'),
                            10994338,  # Sequence number
                            [],  # liked_by_users
                    ),
                    {
                        'to', 'the', 'in', 'of', 'to', 'of', 'on', 'a', 'has', 'had', 'an', 'on', 'from', 'with',
                        'way', 'and', 'by', 'that',
                    },
                    [
                        'Reports',
                        'Twitter',
                        'UAL',
                        '777200',
                        'uncontained',
                        'engine',
                        'failure',
                        'DEN',
                        'Denver',
                        'Colorado',
                        'USA',
                        'HNL',
                        'Honolulu',
                        'Hawaii',
                        'USA',
                        'returned',
                        'safely',
                        'DEN',
                        'Local',
                        'news',
                        'report',
                        'httpsthepostmillennialcomcoloranitedairlines',
                        'Theres',
                        'twitter',
                        'post',
                        'user',
                        'stillgray',
                        'video',
                        'failed',
                        'engine',
                        'aircraft',
                        'PPRuNe',
                        'doesnt',
                        'seem',
                        'want',
                        'include',
                        'here',
                        'UAL',
                        '777',
                        'Ground',
                        'debris',
                    ],
            ),
    )
)
def test_post_significant_words(args, remove_these, expected):
    post = thread_struct.Post(*args)
    assert post.significant_words(remove_these) == expected


EXAMPLE_THREAD_POSTS_SINGLE = [
    (
        datetime.datetime(2020, 1, 1, 5, 32, 14),
        # permalink
        "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338",
        'nicolai',
        parse_string(EXAMPLE_SINGLE_PPRUNE_POST, 'lxml'),
        10994338,  # Sequence number
        [],  # liked_by_users
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
        [],  # liked_by_users
    ),
    (
        datetime.datetime(2020, 1, 1, 5, 32, 28),
        # permalink
        "https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994339",
        'not-nicolai',
        "Totally different text.",
        142,  # Sequence number
        [],  # liked_by_users
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
            (EXAMPLE_THREAD_POSTS_SINGLE, 'nicolai', [0, ]),
            (EXAMPLE_THREAD_POSTS_TWO, 'nicolai', [0, ]),
            (EXAMPLE_THREAD_POSTS_TWO, 'not-nicolai', [1, ]),
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
