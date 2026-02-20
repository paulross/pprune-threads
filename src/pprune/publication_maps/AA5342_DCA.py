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
        return 'AA5342-Blackhawk Collision at DCA'

    def get_introduction_in_html(self) -> str:
        return """There is this thread on pprune about the mid-air collision between a CRJ700, operating as PSA
Airlines flight 5342, and a Sikorsky UH-60L, operated by the US Army under the callsign PAT25 
approximately 0.5 miles southeast of Ronald Reagan Washington National Airport (DCA) on 29 January 2025:
    <ol>
        <li><a href="https://www.pprune.org/accidents-close-calls/663888-aa5342-down-dca.html">Main Thread [pprune]</a></li>
    </ol>
    <span id="useful_links"></span>
    <h2>Useful Links<a class="headerlink" href="#useful_links" title="Link to this heading">\u00B6</a></h2>
    <ol>
        <li><a href="https://data.ntsb.gov/Docket?ProjectID=199620">NTSB docket [NTSB]</a></li>
        <li><a href="https://data.ntsb.gov/Docket/Document/docBLOB?ID=19088347&FileExtension=pdf&FileName=Report_DCA25MA108_Combined%20Transcript%20-%20FINAL-Rel.pdf">Combined Transcript [NTSB}</a></li>
        <li>This accident on the <a href="https://aviation-safety.net/wikibase/474365">Aviation Safety Network</a></li>
        <li><a href="https://en.wikipedia.org/wiki/2025_Potomac_River_mid-air_collision">2025 Potomac River mid-air collision [Wikipedia]</a></li>
        <li><a href="https://www.ntsb.gov/investigations/Pages/DCA25MA108.aspx">NTSB Jan. 27, 2026 Board Meeting Presentations [NTSB]</a> Includes the findings, probable cause and final recommendations.</li>
        <li><a href="AA_DCA_NTSB_Transcript_2026-01-27_B.html">An <b>unoficial transcript</b> of the NTSB Jan. 27, 2026 Board Meeting Presentations.</a></li>
        <li><a href="https://www.ntsb.gov/investigations/AccidentReports/Reports/AIR2602.pdf">Final Report AIR-26-02 [NTSB] [PDF]</a> dated January 27, 2026</li>
        <li><a href="https://transportation.house.gov/news/email/show.aspx?ID=RFS3V7AWS4PPNV2MA2XZXHULM4">Airspace Location and Enhanced Risk Transparency (ALERT) Act of 2026</a> Press Release with links to the act itself.</li>
    </ol>
    <p><b>My condolences to all the people affected by this accident, in particular to the friends and families of the victims.</b></p>
"""

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
        if subject in self.DUPLICATE_SUBJECT_MAP:
            return self.DUPLICATE_SUBJECT_MAP[subject]
        return set()

    def get_significant_posts_permalinks(self) -> typing.Tuple[typing.Tuple[str, int], ...]:
        return self.SIGNIFICANT_POSTS

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
        'adsbin': 'ADSB In',

        'altimeter': 'Altimeter (All)',
        'radalt': 'Radio Altimeter',

        'accountability': 'Accountability/Liability',
        'liability': 'Accountability/Liability',

        'blackhawk': 'Blackhawk (H-60)',
        'h60': 'Blackhawk (H-60)',
        'uh60': 'Blackhawk (H-60)',

        'controller': 'ATC',

        'faa': 'FAA',
        'faas': 'FAA',

        'antidei': 'DEI',

        'findings': 'Findings',

        'docket': 'NTSB Docket',

        'grief': 'Grief',

        'homendy': 'NTSB Chair Jennifer Homendy',

        'hover': 'Hover',

        'ra': 'TCAS RA',
        'ras': 'TCAS RA',

        'trump': 'President Donald Trump',
        'president': 'President Donald Trump',
        'presidents': 'President Donald Trump',
        'potus': 'President Donald Trump',
        'potuss': 'President Donald Trump',

        'moderation': 'Thread Moderation',
        'moderators': 'Thread Moderation',

        'nvgs': 'Night Vision Goggles (NVG)',

        'normalisation': 'Normalization of Deviance',
        'normalization': 'Normalization of Deviance',

        'separation': 'Separation (ALL)',

        'radar': 'Radar',

        'phraseology': 'Phraseology (ATC)',
        # Catches 'see-and-avoid'
        'seeandavoid': 'See and Avoid',

        'sidestep': 'Circle to Land (Deviate to RWY 33)',
        'doglegging': 'Circle to Land (Deviate to RWY 33)',

    }
    CAPS_WORDS_MAP = {
        k: k for k in {
            'ATC', 'ATCO', 'AA5342', 'ADSB', 'CNN', 'CRJ', 'CVR', 'DCA',
            'DEI', 'FAA', 'HUD', 'IFR', 'ICAO', 'KDCA', 'NBC', 'NTSB', 'NDAA',
            'TCAS', 'PAT23', 'PAT25', 'QNH', 'VFR',
        }
    }
    CAPS_WORDS_MAP_ALL = {
        k: k + ' (All)' for k in [
            'ADSB', 'TCAS',
        ]
    }
    CAPS_WORDS_MAP_EXTRA = {
        '13435': 'Frequency 134.35',
        '1191': 'Frequency 119.1',

        '373': 'Section 373 of the FY26 NDAA',

        'LAHS': 'Land and Hold Short',
        'LAHSO': 'Land and Hold Short',

        'NVG': 'Night Vision Goggles (NVG)',

        'NYT': 'New York Times',

        'SA': 'Situational Awareness',

        '4514': 'Republic Airways Flight 4514 Go-around',
        'RP4514': 'Republic Airways Flight 4514 Go-around',

        'POTUS': 'President Donald Trump',

        'ALERT': 'ALERT Act of 2026',
    }
    # ('fuel', 'pump') -> "Fuel Pumps"
    # Each part of the key should be lowercase unless all caps
    PHRASES_MAP = {
        2: {
            ('pass', 'behind',): 'Pass Behind',
            ('go', 'behind',): 'Pass Behind',

            ('situational', 'awareness'): 'Situational Awareness',

            ('black', 'hawk'): 'Blackhawk (H-60)',

            ('barometric', 'altimeter'): 'Barometric Altimeter',

            ('route', 'altitude'): 'Route Altitude',

            ('hot', 'spots'): 'Hot Spots',

            ('circle', 'land',): 'Circle to Land (Deviate to RWY 33)',
            ('circling', 'approach',): 'Circle to Land (Deviate to RWY 33)',

            ('close', 'call',): 'Close Calls',
            ('close', 'calls',): 'Close Calls',
            ('near', 'miss',): 'Close Calls',
            ('near', 'misses',): 'Close Calls',

            ('route', '4',): 'Route 4',
            ('route', '5',): 'Route 5',
            ('route', '9',): 'Route 9',

            ('ADSB', 'out'): 'ADSB Out',
            ('ADSB', 'Out'): 'ADSB Out',
            ('ADSB', 'in'): 'ADSB In',

            ('TCAS', 'RA'): 'TCAS RA',

            ('PSA', 'procedures'): 'PSA Procedures',

            ('preliminary', 'report'): 'Preliminary Report',

            ('final', 'report'): 'Final Report',

            ('relative', 'bearing'): 'Relative Bearing',

            ('probable', 'cause'): 'Probable Cause',
            ('safety', 'recommendations'): 'Safety Recommendations',

            ('rad', 'alt'): 'Radio Altimeter',

            ('skating', 'team'): 'Skating Team (Victims)',
            ('figure', 'skating'): 'Skating Team (Victims)',
            ('ice', 'dancer'): 'Skating Team (Victims)',

            # NOTE: We don't want 'and' in the text (common words).
            ('see', 'avoid'): 'See and Avoid',

            ('vertical', 'separation'): 'Vertical Separation',
            ('visual', 'separation'): 'Visual Separation',
        },
        3: {
            ('accident', 'waiting', 'happen'): 'Accident Waiting to Happen',
            ('wall', 'street', 'journal'): 'Wall Street Journal',

            ('land', 'hold', 'short',): 'Land and Hold Short',

            ('traffic', 'in', 'sight',): 'Traffic in Sight',

            ('deviate', 'rwy', '33'): 'Circle to Land (Deviate to RWY 33)',

            ('PAT25', 'pass', 'behind'): 'Pass Behind (PAT25)',

            ('helicopter', 'working', 'group'): 'Helicopter Working Group',
        },
        4: {
            ('PAT', '25', 'pass', 'behind'): 'Pass Behind (PAT25)',
        }
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
        'Pass Behind': {'Pass Behind (All)', },
        'Pass Behind (PAT25)': {'Pass Behind (All)', },
    }
    # This the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    SIGNIFICANT_POSTS = (
        ('Airspace Chart, Image and Approach Plate', 11817466,),
        # https://en.wikipedia.org/wiki/Jennifer_Homendy 'Jennifer Homendy'
        ('NTSB Chair Jennifer Homendy on Section 373', 12005067),
        # Resolves to https://www.ntsb.gov/news/Documents/National%20Defense%20Authorization%20Act.pdf
        ('NTSB Letter to Congress (re: Section 373 of the FY26 NDAA)', 12003913,),
    )
