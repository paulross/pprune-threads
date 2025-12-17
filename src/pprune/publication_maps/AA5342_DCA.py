"""MIT License

Copyright (c) 2017-2025 Paul Ross https://github.com/paulross

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
import re
import typing

from pprune.publication_maps import publication_map_abc


class AA5342DCA(publication_map_abc.PublicationMapABC):
    def get_title(self) -> str:
        return 'AA5342 Collision with Military Helicopter at DCA'

    def get_introduction_in_html(self) -> str:
        return """"""

    def get_lowercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        return self.LC_WORDS_MAP

    def get_uppercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        result = self.CAPS_WORDS_MAP.copy()
        result.update(self.CAPS_WORDS_MAP_ALL)
        result.update(self.CAPS_WORDS_MAP_EXTRA)
        return result

    def get_phrase_lengths(self) -> typing.List[int]:
        return sorted(self.PHRASES_MAP.keys())

    def get_phrases_to_subject_map(self, phrase_length: int) -> typing.Dict[typing.Tuple[str, ...], str]:
        if phrase_length in self.get_phrase_lengths():
            return self.PHRASES_MAP[phrase_length]
        return {}

    def get_specific_posts_to_subject_map(self) -> typing.Dict[int, str]:
        return self.SPECIFIC_POSTS_MAP

    def get_duplicate_subjects(self, subject: str) -> typing.Set[str]:
        return set()

    def get_significant_posts_permalinks(self) -> typing.Tuple[typing.Tuple[str, int], ...]:
        # https://en.wikipedia.org/wiki/Jennifer_Homendy 'Jennifer Homendy'
        return (
            ('NTSB Chair Jennifer Homendy on Section 373', 12005067),
        )

    def get_set_of_words_required(self) -> typing.Set[str]:
        result = set(self.LC_WORDS_MAP.keys())
        for phrase_length in self.PHRASES_MAP:
            for key in self.PHRASES_MAP[phrase_length]:
                result |= set(key)
        return result

    def get_number_of_top_authors(self) -> int:
        return 30

    def get_upvoted_post_count_limit(self) -> int:
        return 25

    def get_upvoted_post_text_limit(self) -> int:
        return 150

    def get_minimum_number_username_posts(self) -> int:
        """The minimum number of posts a user has mad to get a page with all their posts."""
        return 5

    def get_set_of_removed_subjects(self) -> typing.Set[str]:
        return set()

    def include_empty_post_dates_in_histogram(self) -> bool:
        """Returns True if we want all dates in the date histogram even if there are no posts."""
        return True

    def histogram_frequency(self) -> publication_map_abc.HistogramFrequency:
        """How frequently the histogram buckets are."""
        return publication_map_abc.HistogramFrequency.MONTHLY

    def external_links_of_interest(self) -> typing.Dict[str, typing.Tuple[re.Pattern, ...]]:
        """Returns a map of {Title : (netloc_re, ...), ...} where netloc_re is a compiled regular expression
        to the netloc part of the <a href=URL>.
        If they match then write these posts to a page with that title.
        """
        return {
            "pprune.org": (
                re.compile(r'.*pprune.org'),
            ),
            "CNN": (
                re.compile(r'.*cnn.com'),
            ),
            "FAA": (
                re.compile(r'.*faa.gov'),
            ),
            "New York Times": (
                re.compile(r'.*nytimes.com'),
            ),
            "NTSB": (
                re.compile(r'.*ntsb.gov'),
            ),
            "YouTube Videos": (
                re.compile(r'.*youtube\.com'),
                re.compile(r'.*youtu\.be'),
            ),
            "Wikipedia": (
                re.compile(r'.*wikipedia.org'),
            ),
            "Washington Post": (
                re.compile(r'.*washingtonpost.com'),
            ),
        }

    # Map of {lower_case_word : subject_title, ..}
    LC_WORDS_MAP = {
        'homendy': 'NTSB Chair Jennifer Homendy',

        'ra': 'TCAS RA',
        'ras': 'TCAS RA',

        'trump': 'President Donald Trump',

        'moderation': 'Thread Moderation',
        'moderators': 'Thread Moderation',

        'nvgs': 'Night Vision Goggles (NVG)',

        'separation': 'Separation (ALL)',
    }
    CAPS_WORDS_MAP = {
        k: k for k in {
            'AA5342', 'ADSB', 'NTSB', 'TCAS', 'PAT25',
        }
    }
    CAPS_WORDS_MAP_ALL = {
        k: k + ' (All)' for k in [
            'ADSB', 'TCAS',
        ]
    }
    CAPS_WORDS_MAP_EXTRA = {
        '373': 'Section 373 of the FY26 NDAA',
        'LAHS': 'Land and Hold Short',
        'LAHSO': 'Land and Hold Short',

        'NVG': 'Night Vision Goggles (NVG)'
    }
    # ('fuel', 'pump') -> "Fuel Pumps"
    # Each part of the key should be lowercase unless all caps
    PHRASES_MAP = {
        2: {
            ('pass', 'behind',): 'Pass Behind',
            ('circle', 'land',): 'Circle to Land (Deviate to RWY 33)',


            ('ADSB', 'out'): 'ADSB Out',
            ('ADSB', 'Out'): 'ADSB Out',
            ('ADSB', 'in'): 'ADSB In',

            ('TCAS', 'RA'): 'TCAS RA',

            ('land', 'hold', 'short',): 'Land and Hold Short',

            ('vertical', 'separation'): 'Vertical Separation',
            ('visual', 'separation'): 'Visual Separation',
        },
        3: {
            ('accident', 'waiting', 'happen'): 'Accident Waiting to Happen',
            ('wall', 'street', 'journal'): 'Wall Street Journal',

            ('traffic', 'in', 'sight',): 'Traffic in Sight',

            ('deviate', 'rwy', '33'): 'Circle to Land (Deviate to RWY 33)',
        },
    }
    # The key is the pprune message permalink where the post is clearly about the subject
    # but the text does not refer to it.
    # This is a map of {permalink : subject, ...}
    SPECIFIC_POSTS_MAP = {
        # 11899702: 'Thread Moderation',
    }
    # Map of {subject_title : set(subject_title), ..}
    DUPLICATE_SUBJECT_MAP = {
        # 'RAT (Deployment)': {'RAT (All)', },
    }
    # This the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    SIGNIFICANT_POSTS = (
        # ('Summary of Main Theories', 11906480,),
    )
