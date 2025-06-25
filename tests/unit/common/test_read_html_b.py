import datetime

import pytest

from pprune.common import read_html
from pprune.common import thread_struct


@pytest.mark.parametrize(
    'file_name, expected',
    (
            ('423988-concorde-question-2.html', ('423988', '-concorde-question-', '2')),
            ('423988-concorde-question.html', ('423988', '-concorde-question', None)),
    )
)
def test_user_attributes(file_name, expected):
    match = read_html.RE_FILENAME.match(file_name)
    assert match is not None
    assert match.groups() == expected


@pytest.mark.parametrize(
    'filename, expected',
    (
            (
                    '423988-concorde-question.html',
                    ('423988', '-concorde-question', None),
            ),
            (
                    '423988-concorde-question-2.html',
                    ('423988', '-concorde-question-', '2'),
            ),
            (
                    '666472-plane-crash-near-ahmedabad.html',
                    ('666472', '-plane-crash-near-ahmedabad', None),
            ),
            (
                    '666472-plane-crash-near-ahmedabad-2.html',
                    ('666472', '-plane-crash-near-ahmedabad-', '2'),
            ),
            (
                    '666472-plane-crash-near-ahmedabad-87.html',
                    ('666472', '-plane-crash-near-ahmedabad-', '87'),
            ),
            (
                    '666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html',
                    ('666581', '-air-india-ahmedabad-accident-12th-june-2025-part-2-a', None),
            ),
            (
                    '666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-20.html',
                    ('666581', '-air-india-ahmedabad-accident-12th-june-2025-part-2-a-', '20'),
            ),
    ),
)
def test_RE_FILENAME(filename, expected):
    m = read_html.RE_FILENAME.match(filename)
    assert m is not None
    assert m.groups() == expected


# Taken from tests/integration/example_pages/666472-plane-crash-near-ahmedabad-2.html with tabs replaced by '    '.
HTML_SINGLE_POST = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en" class="no-js">
<body>
                    <!-- post #11898940 -->

<div id="edit11898940">
<!-- this is not the last post shown on the page -->



<div id="post11898940">
    <div class="tpost">
        
        <div class="trow-group">
            <div class="trow thead smallfont">
                <div class="tcell"  style="width:175px;">
                    <!-- status icon and date -->
                    <a name="post11898940"><img class="inlineimg" src="https://www.pprune.org/images/statusicon/post_old.gif" alt="Old" /></a>
                    12th Jun 2025, 09:35
                    
                    <!-- / status icon and date -->
                </div>
                <div class="tcell text-right">
                    &nbsp;
                    #<a href="https://www.pprune.org/11898940-post21.html" target="new" rel="nofollow" id="postcount11898940" name="21" target="new" rel="nofollow"><strong>21</strong></a> (<b><a href="https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898940" title="Link to this Post">permalink</a></b>) &nbsp;
                    
                </div>
            </div>
        
            <div class="trow">
                <div class="tcell alt2" style="width:175px;">
                    <script type="application/ld+json">{"@context":"https:\/\/schema.org","@type":"Person","name":"autobrake3","memberOf":"Registered Member","url":"https:\/\/www.pprune.org\/members\/41169-autobrake3"}</script>
                    <div id="postmenu_11898940">
                        
                        <a rel="nofollow" class="bigusername" href="https://www.pprune.org/members/41169-autobrake3">autobrake3</a>
                        
                        
                    </div>

                    
                    
                    
                    
                    

                    

                    <div class="smallfont">
                        &nbsp;<br />
                        <div>Join Date: Oct 2001</div>
                        <div>Location: A25R</div>
                        
                        <div>
                            Posts: 172
                        </div>
                         
    <div>
        
        Likes: 0
        
    </div>
    <div>
    Received 30 Likes
    on
    <a rel="nofollow" href="https://www.pprune.org/post_thanks.php?do=findthanks&amp;u=41169" title="Find all liked posts by autobrake3">
    1 Post
    </a>
    </div>

                        
                        
                        

                        
                        <div>          </div>
                    </div>

                </div>

                <div class="tcell alt1" id="td_post_11898940">
                    
                    

                    <!-- message -->
                    <div id="post_message_11898940">
                        
                        <div style="margin:1rem; margin-top:0.3rem;">
    <div><label>Quote:</label></div>
    <div class="panel alt2" style="border:1px inset">
    
        <span style="color:#000000">Brits will be on board.</span>
    
    </div>
</div>Yes, Indians and other nationalities too. &#8220;Brits&#8221; not more or less relevant.<br />
<br />
 
                    </div>
                    <!-- / message -->

                    

                    
                    

                    

                    

                    

                </div>
            </div>
            <div class="trow">
                <div class="tcell alt2">
                    <img class="inlineimg" src="https://www.pprune.org/images/statusicon/user_offline.gif" alt="autobrake3 is offline" />


                    
                    
                    
                    
                    &nbsp;
                </div>

                <div class="tcell alt1 text-right">
                    <!-- controls -->
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                        
                    
                    
                    <!-- / controls -->
                </div>
            </div>
        </div><!-- trow-group -->
    </div><!-- tbox -->
</div>

 <div id="post_thanks_box_11898940"><div class="tbox">
    <div class="trow">
        <div class="tcell alt2" style="width: 175px">
            
                <strong>The following 30 users liked this post by autobrake3:</strong>
            
            
            
        </div>
        <div class="tcell alt1" style="vertical-align: top"><div> <a href="https://www.pprune.org/members/20986-2-sheds" rel="nofollow" rel="nofollow">2 sheds</a>, <a href="https://www.pprune.org/members/2175-alpine-flyer" rel="nofollow" rel="nofollow">Alpine Flyer</a>, <a href="https://www.pprune.org/members/394438-ambient-sheep" rel="nofollow" rel="nofollow">Ambient Sheep</a>, <a href="https://www.pprune.org/members/249228-andonip" rel="nofollow" rel="nofollow">AndoniP</a>, <a href="https://www.pprune.org/members/98839-atnotts" rel="nofollow" rel="nofollow">ATNotts</a>, <a href="https://www.pprune.org/members/78882-avrostar" rel="nofollow" rel="nofollow">avrostar</a>, <a href="https://www.pprune.org/members/16435-brupax" rel="nofollow" rel="nofollow">BRUpax</a>, <a href="https://www.pprune.org/members/472053-bucoops" rel="nofollow" rel="nofollow">bucoops</a>, <a href="https://www.pprune.org/members/79793-captain-kaboom" rel="nofollow" rel="nofollow">Captain Kaboom</a>, <a href="https://www.pprune.org/members/306115-crhedbngr" rel="nofollow" rel="nofollow">crHedBngr</a>, <a href="https://www.pprune.org/members/482832-curlyb" rel="nofollow" rel="nofollow">CurlyB</a>, <a href="https://www.pprune.org/members/430314-euclideanplane" rel="nofollow" rel="nofollow">Euclideanplane</a>, <a href="https://www.pprune.org/members/308319-flash131" rel="nofollow" rel="nofollow">Flash131</a>, <a href="https://www.pprune.org/members/370742-flyangry" rel="nofollow" rel="nofollow">Flyangry</a>, <a href="https://www.pprune.org/members/27950-fright-level" rel="nofollow" rel="nofollow">Fright Level</a>, <a href="https://www.pprune.org/members/385185-ggr155" rel="nofollow" rel="nofollow">GGR155</a>, <a href="https://www.pprune.org/members/336272-golfbananajam" rel="nofollow" rel="nofollow">golfbananajam</a>, <a href="https://www.pprune.org/members/3098-greek-god" rel="nofollow" rel="nofollow">Greek God</a>, <a href="https://www.pprune.org/members/354947-hifly787" rel="nofollow" rel="nofollow">hifly787</a>, <a href="https://www.pprune.org/members/246749-i-ainc" rel="nofollow" rel="nofollow">I-AINC</a>, <a href="https://www.pprune.org/members/31984-ifollowroads" rel="nofollow" rel="nofollow">IFollowRoads</a>, <a href="https://www.pprune.org/members/521016-kraftstoffvondesibel" rel="nofollow" rel="nofollow">Kraftstoffvondesibel</a>, <a href="https://www.pprune.org/members/413451-michaelkpit" rel="nofollow" rel="nofollow">MichaelKPIT</a>, <a href="https://www.pprune.org/members/445033-oldngrounded" rel="nofollow" rel="nofollow">OldnGrounded</a>, <a href="https://www.pprune.org/members/73392-sky-blue-and-black" rel="nofollow" rel="nofollow">Sky blue and black</a>, <a href="https://www.pprune.org/members/185037-stoatsbrother" rel="nofollow" rel="nofollow">stoatsbrother</a>, <a href="https://www.pprune.org/members/546554-sunnythesemen" rel="nofollow" rel="nofollow">SunnyTheSemen</a>, <a href="https://www.pprune.org/members/429112-theap" rel="nofollow" rel="nofollow">theAP</a>, <a href="https://www.pprune.org/members/316152-thebat" rel="nofollow" rel="nofollow">TheBat</a>, <a href="https://www.pprune.org/members/413833-una-due-tfc" rel="nofollow" rel="nofollow">Una Due Tfc</a></div></div>
    </div>
</div></div><aside class="text-center" style=""><div class="primis-video-wrapper"><script type="text/javascript" language="javascript" src="https://live.primis.tech/live/liveView.php?s=112613&floatVerticalOffset=60"></script></div>
<style>
.primis-video-wrapper{
max-width: 640px;
max-height: 460px;
margin: 0 auto;
}
</style></aside>


<!-- post 11898940 popup menu -->
<div class="vbmenu_popup" id="postmenu_11898940_menu" style="display:none">
<div class="tbox">
    <div class="trow thead">
        <div class="tcell">autobrake3</div>
    </div>
    
    <div class="trow"><div class="tcell vbmenu_option"><a rel="nofollow" href="https://www.pprune.org/members/41169-autobrake3">View Public Profile</a></div></div>
    
    
    
    
    
    <div class="trow"><div class="tcell vbmenu_option"><a href="https://www.pprune.org/search.php?do=finduser&amp;u=41169" rel="nofollow" rel="nofollow">Find More Posts by autobrake3</a></div></div>
    
    

    
</div>
</div>
<!-- / post 11898940 popup menu -->



</div>

<!-- / post #11898940 -->
</body>
</html>
"""


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (HTML_SINGLE_POST, 11898940, 'edit11898940',),
    ),
    ids=[
        'Single node.'
    ],
)
def test_html_node_post_id(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    result = read_html.html_node_post_id(post_node)
    print()
    print(result)
    assert result == expected


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (HTML_SINGLE_POST, 11898940, 11898940,),
    ),
    ids=[
        'Single node.'
    ],
)
def test_html_node_post_number(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    result = read_html.html_node_post_number(post_node)
    print()
    print(result)
    assert result == expected


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (HTML_SINGLE_POST, 11898940, datetime.datetime(2025, 6, 12, 9, 35),),
    ),
    ids=[
        'Single node.'
    ],
)
def test_html_node_date(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    result = read_html.html_node_date(post_node)
    print()
    print(result)
    assert result == expected


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (
                    HTML_SINGLE_POST, 11898940,
                    'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898940',
             ),
    ),
    ids=[
        'Single node.'
    ],
)
def test_html_node_permalink(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    result = read_html.html_node_permalink(post_node)
    print()
    print(result)
    assert result == expected


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (
                    HTML_SINGLE_POST, 11898940,
                    thread_struct.User(href='https://www.pprune.org/members/41169-autobrake3', name='autobrake3'),
             ),
    ),
    ids=[
        'Single node.'
    ],
)
def test_html_node_user(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    result = read_html.html_node_user(post_node)
    print()
    print(result)
    assert result == expected


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (
                    HTML_SINGLE_POST, 11898940,
                    'Quote:  Brits will be on board.  Yes, Indians and other nationalities too. “Brits” not more or less relevant.',
             ),
    ),
    ids=[
        'Single node.'
    ],
)
def test_get_post_text_from_node(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    result = read_html.get_post_text_from_node(post_node, node_id)
    print()
    print(result.strip().replace('\n', ' '))
    assert result.strip().replace('\n', ' ') == expected


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (HTML_SINGLE_POST, 11898940, 30,),
    ),
    ids=[
        'Single node.'
    ],
)
def test_html_node_like_usernames(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    likes = read_html.html_node_like_usernames(post_node)
    print()
    print(likes)
    assert len(likes) == expected


@pytest.mark.parametrize(
    'html_str, node_id, expected',
    (
            (HTML_SINGLE_POST, 11898940, '',),
    ),
    ids=[
        'Single node.'
    ],
)
def test_read_post_node(html_str, node_id, expected):
    doc = read_html.parse_str_to_beautiful_soup(html_str)
    assert doc is not None
    post_node = doc.find('div', id=f'edit{node_id}')
    assert post_node is not None
    post = read_html.post_from_html_node(post_node)
    assert post is not None
