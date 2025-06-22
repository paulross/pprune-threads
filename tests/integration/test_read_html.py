import datetime
import io
import pprint

import pytest
from pprune.common import read_html
from pprune.common import thread_struct

import example_data


@pytest.mark.parametrize(
    'html_str, expected',
    (
            (example_data.EXAMPLE_PAGES['example_page.html'], 20),
            (example_data.EXAMPLE_PAGES['example_page_four_posts.html'], 4),
            (example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad.html'], 20),
            (example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'], 20),
    ),
    ids=[
        'example_page.html',
        'example_page_four_posts.html',
        '666472-plane-crash-near-ahmedabad.html',
        '666472-plane-crash-near-ahmedabad-2.html',
    ],
)
def test_get_thread_from_html_string(html_str, expected):
    result = read_html.get_thread_from_html_string(html_str)
    assert result is not None
    assert len(result) == expected


@pytest.mark.parametrize(
    'html_str, expected',
    (
            (
                    example_data.EXAMPLE_PAGES['example_page_four_posts.html'],
                    [
                        'https://avherald.com/h?article=4e3fd7f4',
                        'They landed back 25 minutes after take off. That’s not a lot of time to DODAR/GRADE the malfunction, which has been an issue for years on the A320 and has often been attributed to a fault in the Brake Steering Control Unit (BSCU).\nA BSCU fault incident:\nhttps://www.skybrary.aero/index.php/...eles_USA,_2005',
                        'I like the comment in the Simple Flying article:\nThe aircraft involved will also need to undergo maintenance and repairs before returning to service.\nThere’s a surprise! The runway too judging from the picture.',
                        'This has happened to A320s before... 2005, Jet Blue BUR-JFK knew immediately after takeoff that there was a NG issue, burned fuel for three hours before heading into LAX.\nhttps://www.nydailynews.com/news/nat...ticle-1.607155'
                    ],
            ),
    ),
    ids=[
        'example_page_four_posts.html',
    ],
)
def test_get_thread_from_html_string_text_stripped(html_str, expected):
    thread = read_html.get_thread_from_html_string(html_str)
    texts_stripped = []
    for post in thread.posts:
        texts_stripped.append(post.text_stripped)
    print()
    print(texts_stripped)
    assert texts_stripped == expected


@pytest.mark.parametrize(
    'html_str, expected',
    (
            (
                    example_data.EXAMPLE_PAGES['example_page_four_posts.html'],
                    ['A320 Nose Gear Incident', 'BSCU Fault?', '', ''],
            ),
    ),
    ids=[
        'example_page_four_posts.html',
    ],
)
def test_get_thread_subjects_from_html_string(html_str, expected):
    thread = read_html.get_thread_from_html_string(html_str)
    result = []
    for post in thread.posts:
        result.append(post.subject.strip())
    print()
    print(result)
    assert result == expected


@pytest.mark.parametrize(
    'html_str, expected',
    (
            (
                    example_data.EXAMPLE_PAGES['example_page.html'],
                    {
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994338': 0,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994345': 1,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994356': 2,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994360': 3,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994361': 4,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994377': 5,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994382': 6,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994386': 7,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994389': 8,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994402': 9,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994403': 10,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994410': 11,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994411': 12,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994412': 13,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994413': 14,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994414': 15,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994416': 16,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994419': 17,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994423': 18,
                        'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html#post10994426': 19,
                    },
            ),
            (
                    example_data.EXAMPLE_PAGES['example_page_four_posts.html'],
                    {
                        'https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html#post11003559': 0,
                        'https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html#post11003611': 1,
                        'https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html#post11003660': 2,
                        'https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html#post11003938': 3
                    }
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad.html'],
                    {
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898891': 0,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898894': 1,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898897': 2,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898903': 3,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898905': 4,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898912': 5,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898915': 6,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898919': 7,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898923': 8,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898924': 9,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898927': 10,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898928': 11,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898929': 12,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898930': 13,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898932': 14,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898933': 15,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898935': 16,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898936': 17,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898938': 18,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html#post11898939': 19,
                    }
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'],
                    {
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898940': 0,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898942': 1,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898944': 2,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898952': 3,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898953': 4,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898954': 5,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898955': 6,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898956': 7,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898958': 8,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898962': 9,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898963': 10,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898965': 11,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898970': 12,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898971': 13,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898974': 14,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898976': 15,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898979': 16,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898980': 17,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898982': 18,
                        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898984': 19
                    },
            ),
    ),
    ids=[
        'example_page.html',
        'example_page_four_posts.html',
        '666472-plane-crash-near-ahmedabad.html',
        '666472-plane-crash-near-ahmedabad-2.html',
    ],
)
def test_get_thread_from_html_string_post_map(html_str, expected):
    result = read_html.get_thread_from_html_string(html_str)
    print()
    assert result is not None
    pprint.pprint(result.post_map)
    assert result.post_map == expected


@pytest.mark.parametrize(
    'html_str, expected',
    (
            (
                    example_data.EXAMPLE_PAGES['example_page.html'],
                    {
                        thread_struct.User(href='https://www.pprune.org/members/219249-nicolai',
                                           name='nicolai'): [0,
                                                             9],
                        thread_struct.User(href='https://www.pprune.org/members/492579-grav',
                                           name='Grav'): [1],
                        thread_struct.User(href='https://www.pprune.org/members/52796-atakacs',
                                           name='atakacs'): [2],
                        thread_struct.User(href='https://www.pprune.org/members/214423-flynerd',
                                           name='flynerd'): [3],
                        thread_struct.User(href='https://www.pprune.org/members/465087-armagnac2010',
                                           name='armagnac2010'): [4,
                                                                  7],
                        thread_struct.User(href='https://www.pprune.org/members/414340-tdracer',
                                           name='tdracer'): [5],
                        thread_struct.User(href='https://www.pprune.org/members/191275-dumbled0re',
                                           name='dumbled0re'): [6],
                        thread_struct.User(href='https://www.pprune.org/members/358492-mr-joshua',
                                           name='Mr Joshua'): [
                            8],
                        thread_struct.User(href='https://www.pprune.org/members/333150-krismiler',
                                           name='krismiler'): [
                            10],
                        thread_struct.User(href='https://www.pprune.org/members/98979-jewitts',
                                           name='jewitts'): [11],
                        thread_struct.User(href='https://www.pprune.org/members/343268-mlheliwrench',
                                           name='MLHeliwrench'): [12,
                                                                  16],
                        thread_struct.User(href='https://www.pprune.org/members/151984-back-at-nh',
                                           name='Back at NH'): [13],
                        thread_struct.User(href='https://www.pprune.org/members/161437-edml',
                                           name='EDML'): [14],
                        thread_struct.User(href='https://www.pprune.org/members/48942-lomapaseo',
                                           name='lomapaseo'): [
                            15],
                        thread_struct.User(href='https://www.pprune.org/members/174027-mike_uem',
                                           name='Mike_UEM'): [
                            17],
                        thread_struct.User(href='https://www.pprune.org/members/444861-phylosocopter',
                                           name='phylosocopter'): [18],
                        thread_struct.User(href='https://www.pprune.org/members/57500-568', name='568'): [
                            19],
                    },
            ),
            (
                    example_data.EXAMPLE_PAGES['example_page_four_posts.html'],
                    {
                        thread_struct.User(href='https://www.pprune.org/members/333150-krismiler',
                                           name='krismiler'): [
                            0],
                        thread_struct.User(href='https://www.pprune.org/members/3549-nightstop',
                                           name='Nightstop'): [1],
                        thread_struct.User(href='https://www.pprune.org/members/265368-andrewgr2',
                                           name='Andrewgr2'): [
                            2],
                        thread_struct.User(href='https://www.pprune.org/members/485736-lake1952',
                                           name='Lake1952'): [3],
                    }
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad.html'],
                    {
                        thread_struct.User(href='https://www.pprune.org/members/506827-shared-reality',
                                           name='shared reality'): [19],
                        thread_struct.User(href='https://www.pprune.org/members/507292-dogtailred2',
                                           name='DogTailRed2'): [17],
                        thread_struct.User(href='https://www.pprune.org/members/4330-mightygem',
                                           name='MightyGem'): [
                            16],
                        thread_struct.User(href='https://www.pprune.org/members/333150-krismiler',
                                           name='krismiler'): [
                            15],
                        thread_struct.User(href='https://www.pprune.org/members/526350-mobov98423',
                                           name='mobov98423'): [14,
                                                                18],
                        thread_struct.User(href='https://www.pprune.org/members/7156-acms',
                                           name='ACMS'): [13],
                        thread_struct.User(href='https://www.pprune.org/members/70434-skysod',
                                           name='skysod'): [12],
                        thread_struct.User(href='https://www.pprune.org/members/291583-tu-114',
                                           name='Tu.114'): [11],
                        thread_struct.User(href='https://www.pprune.org/members/13045-compressor-stall',
                                           name='compressor stall'): [10],
                        thread_struct.User(href='https://www.pprune.org/members/8160-sops',
                                           name='SOPS'): [9],
                        thread_struct.User(href='https://www.pprune.org/members/142217-safelife',
                                           name='safelife'): [8],
                        thread_struct.User(href='https://www.pprune.org/members/476068-rationalfunctions',
                                           name='rationalfunctions'): [7],
                        thread_struct.User(href='https://www.pprune.org/members/234729-ara01jbb',
                                           name='ara01jbb'): [6],
                        thread_struct.User(href='https://www.pprune.org/members/449147-logansi',
                                           name='logansi'): [5],
                        thread_struct.User(href='https://www.pprune.org/members/444692-paxfips',
                                           name='PAXfips'): [4],
                        thread_struct.User(href='https://www.pprune.org/members/347629-xanda_man',
                                           name='xanda_man'): [
                            3],
                        thread_struct.User(href='https://www.pprune.org/members/390429-rixt',
                                           name='rixt'): [1],
                        thread_struct.User(
                            href='https://www.pprune.org/members/6151-wee-weasley-welshman',
                            name='Wee Weasley Welshman'): [2],
                        thread_struct.User(href='https://www.pprune.org/members/125757-janetflight',
                                           name='JanetFlight'): [0],
                    }
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'],
                    {
                        thread_struct.User(href='https://www.pprune.org/members/41169-autobrake3',
                                           name='autobrake3'): [
                            0],
                        thread_struct.User(href='https://www.pprune.org/members/235722-jhpaulo',
                                           name='JHPaulo'): [1],
                        thread_struct.User(href='https://www.pprune.org/members/147051-iaedude',
                                           name='IAEdude'): [2],
                        thread_struct.User(href='https://www.pprune.org/members/366993-olitom',
                                           name='OliTom'): [3],
                        thread_struct.User(href='https://www.pprune.org/members/440074-tupungato',
                                           name='tupungato'): [
                            4],
                        thread_struct.User(href='https://www.pprune.org/members/119704-nolimitholdem',
                                           name='nolimitholdem'): [5],
                        thread_struct.User(href='https://www.pprune.org/members/43791-reverserunlocked',
                                           name='reverserunlocked'): [6],
                        thread_struct.User(href='https://www.pprune.org/members/344780-iron-duck',
                                           name='Iron Duck'): [
                            7,
                            15],
                        thread_struct.User(href='https://www.pprune.org/members/429128-r_p',
                                           name='r_p'): [8],
                        thread_struct.User(href='https://www.pprune.org/members/302188-weatherdude',
                                           name='weatherdude'): [9],
                        thread_struct.User(href='https://www.pprune.org/members/278539-voenos',
                                           name='Voenos'): [10],
                        thread_struct.User(href='https://www.pprune.org/members/112496-22-04',
                                           name='22/04'): [11],
                        thread_struct.User(href='https://www.pprune.org/members/7156-acms',
                                           name='ACMS'): [12],
                        thread_struct.User(href='https://www.pprune.org/members/8095-akerosid',
                                           name='akerosid'): [13],
                        thread_struct.User(href='https://www.pprune.org/members/130903-pug',
                                           name='pug'): [14],
                        thread_struct.User(href='https://www.pprune.org/members/188787-pal90',
                                           name='pal90'): [16],
                        thread_struct.User(href='https://www.pprune.org/members/88277-dixi188',
                                           name='dixi188'): [17],
                        thread_struct.User(href='https://www.pprune.org/members/73670-mmeteesside',
                                           name='mmeteesside'): [18],
                        thread_struct.User(href='https://www.pprune.org/members/333150-krismiler',
                                           name='krismiler'): [
                            19],
                    },
            ),
    ),
    ids=[
        'example_page.html',
        'example_page_four_posts.html',
        '666472-plane-crash-near-ahmedabad.html',
        '666472-plane-crash-near-ahmedabad-2.html',
    ],
)
def test_get_thread_from_html_string_user_post_indexes(html_str, expected):
    result = read_html.get_thread_from_html_string(html_str)
    print()
    assert result is not None
    pprint.pprint(result.user_post_indexes)
    assert result.user_post_indexes == expected


def test_read_posts_from_example_pprune_page():
    file = io.StringIO(example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'])
    post_nodes = read_html.get_post_nodes_from_file(file)
    assert len(post_nodes) == 20


def test_get_post_nodes_from_file():
    file = io.StringIO(example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'])
    post_nodes = read_html.get_post_nodes_from_file(file)
    post_ids = [read_html.html_node_post_id(post) for post in post_nodes]
    assert post_ids == [
        'edit11898940',
        'edit11898942',
        'edit11898944',
        'edit11898952',
        'edit11898953',
        'edit11898954',
        'edit11898955',
        'edit11898956',
        'edit11898958',
        'edit11898962',
        'edit11898963',
        'edit11898965',
        'edit11898970',
        'edit11898971',
        'edit11898974',
        'edit11898976',
        'edit11898979',
        'edit11898980',
        'edit11898982',
        'edit11898984',
    ]


def test_get_post_nodes_from_file():
    file = io.StringIO(example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'])
    post_nodes = read_html.get_post_nodes_from_file(file)
    post_ids = [read_html.html_node_post_number(post) for post in post_nodes]
    assert post_ids == [
        11898940,
        11898942,
        11898944,
        11898952,
        11898953,
        11898954,
        11898955,
        11898956,
        11898958,
        11898962,
        11898963,
        11898965,
        11898970,
        11898971,
        11898974,
        11898976,
        11898979,
        11898980,
        11898982,
        11898984,
    ]


def test_html_node_date():
    file = io.StringIO(example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'])
    post_nodes = read_html.get_post_nodes_from_file(file)
    post_ids = [read_html.html_node_date(post) for post in post_nodes]
    assert post_ids == [
        datetime.datetime(2025, 6, 12, 9, 35),
        datetime.datetime(2025, 6, 12, 9, 36),
        datetime.datetime(2025, 6, 12, 9, 40),
        datetime.datetime(2025, 6, 12, 9, 47),
        datetime.datetime(2025, 6, 12, 9, 48),
        datetime.datetime(2025, 6, 12, 9, 48),
        datetime.datetime(2025, 6, 12, 9, 48),
        datetime.datetime(2025, 6, 12, 9, 49),
        datetime.datetime(2025, 6, 12, 9, 51),
        datetime.datetime(2025, 6, 12, 9, 53),
        datetime.datetime(2025, 6, 12, 9, 53),
        datetime.datetime(2025, 6, 12, 9, 54),
        datetime.datetime(2025, 6, 12, 9, 56),
        datetime.datetime(2025, 6, 12, 9, 57),
        datetime.datetime(2025, 6, 12, 9, 58),
        datetime.datetime(2025, 6, 12, 10, 0),
        datetime.datetime(2025, 6, 12, 10, 1),
        datetime.datetime(2025, 6, 12, 10, 2),
        datetime.datetime(2025, 6, 12, 10, 3),
        datetime.datetime(2025, 6, 12, 10, 3),
    ]


def test_html_node_permalink():
    file = io.StringIO(example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'])
    post_nodes = read_html.get_post_nodes_from_file(file)
    post_ids = [read_html.html_node_permalink(post) for post in post_nodes]
    assert post_ids == [
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898940',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898942',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898944',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898952',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898953',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898954',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898955',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898956',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898958',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898962',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898963',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898965',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898970',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898971',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898974',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898976',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898979',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898980',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898982',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-2.html#post11898984',
    ]


def test_html_node_user():
    file = io.StringIO(example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'])
    post_nodes = read_html.get_post_nodes_from_file(file)
    post_ids = [read_html.html_node_user(post) for post in post_nodes]
    assert post_ids == [
        thread_struct.User(href='https://www.pprune.org/members/41169-autobrake3',
                           name='autobrake3'),
        thread_struct.User(href='https://www.pprune.org/members/235722-jhpaulo', name='JHPaulo'),
        thread_struct.User(href='https://www.pprune.org/members/147051-iaedude', name='IAEdude'),
        thread_struct.User(href='https://www.pprune.org/members/366993-olitom', name='OliTom'),
        thread_struct.User(href='https://www.pprune.org/members/440074-tupungato', name='tupungato'),
        thread_struct.User(href='https://www.pprune.org/members/119704-nolimitholdem',
                           name='nolimitholdem'),
        thread_struct.User(href='https://www.pprune.org/members/43791-reverserunlocked',
                           name='reverserunlocked'),
        thread_struct.User(href='https://www.pprune.org/members/344780-iron-duck', name='Iron Duck'),
        thread_struct.User(href='https://www.pprune.org/members/429128-r_p', name='r_p'),
        thread_struct.User(href='https://www.pprune.org/members/302188-weatherdude',
                           name='weatherdude'),
        thread_struct.User(href='https://www.pprune.org/members/278539-voenos', name='Voenos'),
        thread_struct.User(href='https://www.pprune.org/members/112496-22-04', name='22/04'),
        thread_struct.User(href='https://www.pprune.org/members/7156-acms', name='ACMS'),
        thread_struct.User(href='https://www.pprune.org/members/8095-akerosid', name='akerosid'),
        thread_struct.User(href='https://www.pprune.org/members/130903-pug', name='pug'),
        thread_struct.User(href='https://www.pprune.org/members/344780-iron-duck', name='Iron Duck'),
        thread_struct.User(href='https://www.pprune.org/members/188787-pal90', name='pal90'),
        thread_struct.User(href='https://www.pprune.org/members/88277-dixi188', name='dixi188'),
        thread_struct.User(href='https://www.pprune.org/members/73670-mmeteesside',
                           name='mmeteesside'),
        thread_struct.User(href='https://www.pprune.org/members/333150-krismiler', name='krismiler'),
    ]


# From: https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html
# Content starts with 'Reports on Twitter'
EXAMPLE_PPRINE_PAGE_URL = 'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html'
# https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html
EXAMPLE_PPRUNE_PAGE_THREE_POSTS_URL = 'https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html'


@pytest.mark.parametrize(
    'url, expected',
    (
            (EXAMPLE_PPRINE_PAGE_URL,
             ['https://www.pprune.org/rumours-news/638797-united-b777-engine-failure.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-2.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-3.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-4.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-5.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-6.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-7.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-8.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-9.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-10.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-11.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-12.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-13.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-14.html',
              'https://www.pprune.org/rumours-news/638797-united-b777-engine-failure-15.html',
              ]),
            (EXAMPLE_PPRUNE_PAGE_THREE_POSTS_URL,
             ['https://www.pprune.org/rumours-news/639101-a320-nose-gear-incident.html']),
    )
)
def test_all_page_urls_from_external_url(url, expected):
    html_page = read_html.parse_url_to_beautiful_soup(url)
    result = read_html.all_page_urls_from_page(url, html_page)
    assert result == expected
