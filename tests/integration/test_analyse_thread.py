import pytest
from pprune import analyse_thread
from pprune.common import read_html
from pprune.common import words

import example_data


@pytest.mark.parametrize(
    'html_str, num_common_wrds, freq_ge, expected',
    (
            (
                    example_data.EXAMPLE_PAGES['example_page.html'],
                    1000,
                    4,
                    {'blade': 6, 'engine': 9, 'fan': 5, 'loads': 4, 'seem': 4, 'vibration': 6},
            ),
            (
                    example_data.EXAMPLE_PAGES['example_page_four_posts.html'],
                    1000,
                    2,
                    {'fault': 2},
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad.html'],
                    1000,
                    5,
                    {
                        'Im': 5,
                        'Originally': 8,
                        'cant': 5,
                        'convinced': 5,
                        'crash': 6,
                        'flaps': 12,
                        'gear': 8,
                        'saw': 6,
                    },
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'],
                    1000,
                    5,
                    {'Originally': 6, 'aircraft': 6, 'flaps': 10},
            ),
    ),
    ids=[
        'example_page.html',
        'example_page_four_posts.html',
        '666472-plane-crash-near-ahmedabad.html',
        '666472-plane-crash-near-ahmedabad-2.html',
    ],
)
def test_count_non_cap_words(html_str, num_common_wrds, freq_ge, expected):
    thread = read_html.get_thread_from_html_string(html_str)
    common_words = words.read_common_words_file(limit=num_common_wrds)
    result = analyse_thread.count_non_cap_words(thread, common_words, freq_ge)
    assert result is not None
    assert result == expected


@pytest.mark.parametrize(
    'html_str, num_common_wrds, phrase_length, freq_ge, expected',
    (
            (
                    example_data.EXAMPLE_PAGES['example_page.html'],
                    1000,
                    2,
                    2,
                    {
                        ('777', 'designcert'): 2,
                        ('JAL', 'seem'): 2,
                        ('blade', 'pieces'): 2,
                        ('fan', 'blade'): 4,
                        ('fore', 'mentioned'): 2,
                        ('hydraulic', 'fluid'): 2,
                        ('loads', '777'): 2,
                        ('mentioned', 'JAL'): 2,
                        ('seem', 'loads'): 2,
                        ('vibration', 'levels'): 2,
                    },
            ),
            (
                    example_data.EXAMPLE_PAGES['example_page.html'],
                    1000,
                    3,
                    2,
                    {
                        ('JAL', 'seem', 'loads'): 2,
                        ('fore', 'mentioned', 'JAL'): 2,
                        ('loads', '777', 'designcert'): 2,
                        ('mentioned', 'JAL', 'seem'): 2,
                        ('seem', 'loads', '777'): 2,
                    },
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad.html'],
                    1000,
                    2,
                    4,
                    {
                        ('I', 'cant'): 5,
                        ('I', 'saw'): 5,
                        ('Im', 'convinced'): 5,
                        ('Originally', 'logansi'): 4,
                        ('cant', 'flaps'): 5,
                        ('convinced', 'I'): 5,
                        ('crash', 'Im'): 5,
                        ('logansi', 'I'): 4,
                        ('saw', 'crash'): 5,
                    },
            ),
            (
                    example_data.EXAMPLE_PAGES['666472-plane-crash-near-ahmedabad-2.html'],
                    1000,
                    2,
                    4,
                    {},
            ),
    ),
    ids=[
        'example_page.html-1000-2-2',
        'example_page.html-1000-3-2',
        '666472-plane-crash-near-ahmedabad.html',
        '666472-plane-crash-near-ahmedabad-2.html',
    ],
)
def test_count_phrases(html_str, num_common_wrds, phrase_length, freq_ge, expected):
    thread = read_html.get_thread_from_html_string(html_str)
    common_words = words.read_common_words_file(limit=num_common_wrds)
    result = analyse_thread.count_phrases(thread, common_words, phrase_length, freq_ge)
    assert result is not None
    assert result == expected
@pytest.mark.parametrize(
    'html_str, min_size, freq_ge, expected',
    (
            (
                    example_data.EXAMPLE_PAGES['example_page.html'],
                    2,
                    2,
                    {'777': 5, 'DEN': 2, 'JAL': 3, 'UAL': 2, 'USA': 2},
            ),
    ),
    ids=[
        'example_page.html-2-2',
    ],
)
def test_count_all_caps(html_str, min_size, freq_ge, expected):
    thread = read_html.get_thread_from_html_string(html_str)
    result = analyse_thread.count_all_caps(thread, min_size, freq_ge)
    assert result is not None
    assert result == expected
