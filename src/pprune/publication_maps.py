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

This is a set of maps that determine the layout of the Concorde Re-mix site.
Each key is a word or phrase that can be identified in the text.
Each value in the map is the subject that the text (probably) refers to.

TODO: Make this a list of (function, map) where the function takes a list of words and
applies it to the map. This would make the code more general.
"""

__author__ = 'Paul Ross'
__date__ = '2017-01-01'
__version__ = '0.0.1'
__rights__ = 'Copyright (c) 2017 Paul Ross'

import abc
import typing


class PublicationMap(abc.ABC):
    @abc.abstractmethod
    def get_title(self) -> str:
        """Gets the title to be used in the output index.html"""
        pass

    @abc.abstractmethod
    def get_introduction_in_html(self) -> str:
        """Gets the introduction to be used in the output index.html.
        This can be raw HTML."""
        pass

    @abc.abstractmethod
    def get_lowercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        """Returns a map of {lower_case_word : subject_title, ..}"""
        pass

    @abc.abstractmethod
    def get_uppercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        """Returns a map of {upper_case_word : subject_title, ..}"""
        pass

    @abc.abstractmethod
    def get_phrase_lengths(self) -> typing.List[int]:
        """Returns the phrase lengths supported."""
        pass

    @abc.abstractmethod
    def get_phrases_to_subject_map(self, phrase_length: int) -> typing.Dict[str, str]:
        """Returns a map of {phrase : subject_title, ..}"""
        pass

    @abc.abstractmethod
    def get_specific_posts_to_subject_map(self) -> typing.Dict[int, str]:
        """Returns a map of {permalink : subject_title, ..}"""
        pass

    @abc.abstractmethod
    def get_duplicate_subjects(self, subject: str) -> typing.Set[str]:
        """Given a subject that a post corresponds to then this returns a set
        of subjects the post shall also be included in.
        For example if a post is specifically targeted at "RAT (Deployment)"
        then that post should also be included in "RAT (All)" etc."""
        pass

    def get_all_subject_titles(self) -> typing.Set[str]:
        ret = set()
        ret |= set(self.get_lowercase_word_to_subject_map().values())
        ret |= set(self.get_uppercase_word_to_subject_map().values())
        for phrase_length in self.get_phrase_lengths():
            ret |= set(self.get_phrases_to_subject_map(phrase_length).values())
        ret |= set(self.get_specific_posts_to_subject_map().values())
        # ret |= self.get_duplicate_subjects()
        removed_subjects = self.get_set_of_removed_subjects()
        # # Sanity check.
        # removed_subjects_diff = removed_subjects.difference(ret | self.get_duplicate_subjects())
        # if removed_subjects_diff:
        #     raise ValueError(f'These removed subjects not in all subjects: {removed_subjects_diff}')
        ret -= removed_subjects
        return ret

    @abc.abstractmethod
    def get_significant_posts_permalinks(self) -> typing.Tuple[typing.Tuple[str, int]]:
        """The is the set of permalinks of significant posts that might be gathered
        together in the subject 'Significant Posts'."""
        pass

    @abc.abstractmethod
    def get_set_of_words_required(self) -> typing.Set[str]:
        """This gives the search words that are contained in the maps,
        these should be removed from any common words exclusion."""
        pass

    @abc.abstractmethod
    def get_number_of_top_authors(self) -> int:
        """The number of prolific authors."""
        pass

    @abc.abstractmethod
    def get_upvoted_post_count_limit(self) -> int:
        """The limit of the number of up-voted posts."""
        pass

    @abc.abstractmethod
    def get_upvoted_post_text_limit(self) -> int:
        """The limit of the length of the text to be used with up-voted posts."""
        pass

    @abc.abstractmethod
    def get_minimum_number_username_posts(self) -> int:
        """The minimum number of posts a user has mad to get a page with all their posts."""
        pass

    @abc.abstractmethod
    def get_set_of_removed_subjects(self) -> typing.Set[str]:
        """Returns a set of subjects that are removed, possibly temporarily."""
        pass


class AirIndia171(PublicationMap):
    def get_title(self) -> str:
        return 'AI171 Re-mixed'

    def get_introduction_in_html(self) -> str:
        return """There are these threads on pprune about the accident to
 <a href="https://en.wikipedia.org/wiki/Air_India_Flight_171">Air India Flight 171 [Wikipedia]</a>
 on 12 June 2025:
    <ol>
        <li><a href="https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html">Part One [pprune]</a> (now closed)</li>
        <li><a href="https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html">Part Two [pprune]</a> (now closed)</li>
        <li><a href="https://www.pprune.org/accidents-close-calls/667141-preliminary-air-india-crash-report-published.html">Preliminary Report [pprune]</a> (now closed)</li>
        <li>There is also a thread on the
            <a href="https://www.pprune.org/accidents-close-calls/666714-moderation-air-india-accident-threads.html">moderation of these threads [pprune]</a>
             (this is not included in this analysis)
         </li>
    </ol>
    <p><b>My condolences to all the people affected by this accident, in particular to the friends and families of the victims.</b></p>
    <h2>Useful Links</h2>
    <ol>
        <li><a href="https://aaib.gov.in/What's%20New%20Assets/Preliminary%20Report%20VT-ANB.pdf">The Preliminary Report</a></li>
        <li><a href="https://aaib.gov.in">Air Accident Investigation Board (India)</a></li>
        <li><a href="https://www.dgca.gov.in/digigov-portal/">Directorate General of Civil Aviation (India)</a> (DGCA)</li>
        <li>This accident on the <a href="https://asn.flightsafety.org/asndb/518859">Aviation Safety Network</a></li>
        <li><a href="https://www.gov.uk/government/organisations/air-accidents-investigation-branch">Air Accident Investigation Board (UK)</a></li>
    </ol>
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

    def get_phrases_to_subject_map(self, phrase_length: int) -> typing.Dict[str, str]:
        if phrase_length in self.get_phrase_lengths():
            return self.PHRASES_MAP[phrase_length]
        return {}

    def get_specific_posts_to_subject_map(self) -> typing.Dict[int, str]:
        return self.SPECIFIC_POSTS_MAP

    def get_duplicate_subjects(self, subject: str) -> typing.Set[str]:
        if subject in self.DUPLICATE_SUBJECT_MAP:
            return self.DUPLICATE_SUBJECT_MAP[subject]
        return set()

    def get_significant_posts_permalinks(self) -> typing.Tuple[typing.Tuple[str, int]]:
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
        return {
            '51 Day Issue',
            'Audio Analysis',
            'Biocide',
            'Bird Strike',
            'Engine Over-speed (All)',
            'Engine Shutdown (Over-speed)',
            'Flap Retraction',
            'Flap Setting',
            'Flaps (All)',
            'Flaps vs Gear',
            'Fuel Contamination',
            'Fuel Pump (Engine Driven)',
            'Fuel Pumps',
            'GEnx TCMA Logic',
            'Gear Retraction',
            'Hydraulic Failure (Double)',
            'Hydraulic Failure (Triple)',
            'Hydraulic Pumps',
            'Lift/Drag Ratio',
            'MLG (All)',
            'MLG Tilt',
            'N2 Over-speed',
            'RAT (Alternate Noise Sources)',
            'RAT (Sound)',
            'RAT (Witnesses)',
            'Suicide/Murder',
            'TCMA (Activation)',
            'TCMA (Air-ground Logic)',
            'TCMA (All)',
            'TCMA (Improper Activation)',
            'TCMA (Logic)',
            'TCMA (Shutdown)',
            'Total Energy',
            'VNAV',
            'Water Ingress',
            'Wrong Engine',
        }

    # Map of {lower_case_word : subject_title, ..}
    LC_WORDS_MAP = {
        'mayday': 'MAYDAY',
        'biocide': 'Biocide',
        'tilt': 'MLG Tilt',
        'condolences': 'Condolences',
        'sympathy': 'Condolences',
        'empathy': 'Condolences',
        'spectrogram': 'Audio Analysis',
        'flightradar24': 'FlightRadar24',
        'lavatories': 'Water Ingress',
        'genx': 'GEnx (ALL)',
        'parameters': 'Parameters',
        'generators': 'Generators/Alternators',
        'generator': 'Generators/Alternators',
        'alternators': 'Generators/Alternators',
        'alternator': 'Generators/Alternators',
        'relight': 'Relight',
        'restart': 'Relight',
        '51': '51 Day Issue',
        '51day': '51 Day Issue',
        'detent': 'Fuel Cutoff Switches (detent)',
        'detents': 'Fuel Cutoff Switches (detent)',
        'cutoff': 'Fuel Cutoff Switches',
        'guard': 'Switch Guards',
        'guards': 'Switch Guards',
        'guarded': 'Switch Guards',
        'honeywell': 'Honeywell',
        # Slightly hacky way to capture posts that reference the timeline in the preliminary report.
        # 08:08:42 E1 Fuel Cutoff Switch RUN -> CUTOFF, 180 kts
        # 08:08:43 E2 Fuel Cutoff Switch RUN -> CUTOFF
        '080842': 'Timeline (Preliminary Report)',
        '080843': 'Timeline (Preliminary Report)',
        'cerebellum': 'Action slip',
        'avherald': 'AvHerald',
        'wsj': 'Wall Street Journal',
        'suicide': 'Suicide/Murder',
        'murder': 'Suicide/Murder',
        'jumpseaters': 'Jump Seat',
        'jumpseat': 'Jump Seat',
        'moderators': 'Thread Moderation',
        'moderation': 'Thread Moderation',
        'mods': 'Thread Moderation',
    }
    # This maps capitilised words (stripped of punctuation) to their subject.
    # Any post that has that capitilised word in it is treated as part of that subject.
    CAPS_WORDS_MAP = {
        k: k for k in {
            'AI171', 'ADSB', 'APU', 'BBC', 'CCTV', 'FDR', 'V1', 'V2', 'EAFR',
            'FADEC', 'FAA', 'TOGA', 'VNAV', 'NTSB', 'MEL', 'DFDR', 'FBW', 'HPSOV', 'FCOM', 'FR24', 'CVR', 'EFATO',
            'RIPS', 'TRU', 'ARINC', 'DGCA',
            'ICAO', 'EICAS',
        }
    }
    CAPS_WORDS_MAP_ALL = {
        k: k + ' (All)' for k in [
            'RAT', 'TCMA', 'AAIB', 'MLG',
        ]
    }
    CAPS_WORDS_MAP_EXTRA = {
        'NYT': 'New York Times',
        # NOTE: Punctuation is removed from 'AW&ST' -> 'AWST'.
        # See tests.unit.common.test_thread_struct.test_post_words()
        'AWST': 'Aviation Week & Space Technology',
        'AD': 'Air Worthiness Directives',
        'ADs': 'Air Worthiness Directives',
        'EAFRs': 'EAFR',
        'TRUs': 'TRU',
        'DFDAU': 'Digital Flight Data Acquisition Unit',
        'MAYDAY': "MAYDAY",
        'HPSOV': "High Pressure Shutoff Valve",
        'FR24': "FlightRadar24",
        'LD': 'Lift/Drag Ratio',
        'TLA': 'TLA (Thrust Lever Angle)',
        'RUN': 'RUN/CUTOFF',
        'CUTOFF': 'RUN/CUTOFF',
        'SAIB': 'Special Airworthiness Information Bulletin',
        # NM-18-33 without punctuation.
        'NM1833': 'SAIB NM-18-33',
        'WSJ': 'Wall Street Journal',
        'G650': 'G650 Simulation',
        'FCS': 'Fuel Cutoff Switches',
        'FCO': 'Fuel Cutoff Switches',
    }
    # ('fuel', 'pump') -> "Fuel Pumps"
    # Each part of the key should be lower case unless all caps
    PHRASES_MAP = {
        2: {
            ('engine', 'failure'): 'Engine Failure (All)',

            ('RAT', 'deploy'): 'RAT (Deployment)',
            ('RAT', 'deployed'): 'RAT (Deployment)',
            ('RAT', 'deployment'): 'RAT (Deployment)',
            ('RAT', 'extended'): 'RAT (Deployment)',
            ('RAT', 'electrical'): 'RAT (Electrical)',
            ('RAT', 'seen'): 'RAT (Deployment)',
            ('RAT', 'sound'): 'RAT (Sound)',
            ('deploy', 'RAT'): 'RAT (Deployment)',
            ('deployed', 'RAT'): 'RAT (Deployment)',
            ('deployment', 'RAT'): 'RAT (Deployment)',
            ('evidence', 'RAT'): 'RAT (Deployment)',
            ('failure', 'RAT'): 'RAT (Deployment)',
            ('trigger', 'RAT'): 'RAT (Deployment)',

            ('TCMA', 'activation'): 'TCMA (Activation)',
            ('TCMA', 'airground'): 'TCMA (Air-ground Logic)',
            ('airground', 'logic'): 'TCMA (Air-ground Logic)',
            ('TCMA', 'function'): 'TCMA (Activation)',
            ('TCMA', 'ground'): 'TCMA (Air-ground Logic)',
            ('TCMA', 'logic'): 'TCMA (Logic)',
            ('TCMA', 'package'): 'TCMA (All)',
            ('TCMA', 'shutdown'): 'TCMA (Shutdown)',
            ('improper', 'TCMA'): 'TCMA (Shutdown)',
            ('overspeed', 'protection'): 'TCMA (Shutdown)',

            ('engine', 'shutdown'): 'Engine Shutdown',
            ('engines', 'failed'): 'Engine Shutdown',
            ('engines', 'failed'): 'Engine Shutdown',
            ('engines', 'simultaneously'): 'Dual Engine Failure',
            ('dual', 'rollback'): 'Dual Engine Failure',

            ('wrong', 'engine'): 'Wrong Engine',

            ('fuel', 'contamination'): 'Fuel Contamination',

            ('fuel', 'cutoff'): 'Fuel Cutoff',
            ('fuel', 'cut'): 'Fuel Cutoff',
            ('fuel', 'shut'): 'Fuel Cutoff',
            ('fuel', 'starvation'): 'Fuel Cutoff',

            ('fuel', 'switch'): 'Fuel Cutoff Switches',
            ('fuel', 'switches'): 'Fuel Cutoff Switches',
            ('cutoff', 'switches'): 'Fuel Cutoff Switches',
            ('cutoff', 'switch'): 'Fuel Cutoff Switches',
            ('cut', 'off'): 'Fuel Cutoff Switches',
            ('fuelswitch', 'design'): 'Fuel Cutoff Switches',
            ('fco', 'switches'): 'Fuel Cutoff Switches',

            ('fuel', 'pump'): 'Fuel Pumps',
            ('fuel', 'pumps'): 'Fuel Pumps',
            ('fuel', 'flow'): 'Fuel Pumps',
            ('fuel', 'supply'): 'Fuel Pumps',
            ('boost', 'pumps'): 'Fuel Pumps',
            ('suction', 'feed'): 'Fuel Pumps',

            ('gear', 'doors'): 'Gear Retraction',
            ('gear', 'retraction'): 'Gear Retraction',
            ('gear', 'down'): 'Gear Retraction',
            ('gear', 'selected'): 'Gear Retraction',
            ('landing', 'gear'): 'Gear Retraction',
            ('doors', 'open'): 'Gear Retraction',

            ('gear', 'lever'): 'Gear Lever',

            ('bogie', 'tilting'): 'MLG Tilt',
            ('bogies', 'tilt'): 'MLG Tilt',
            ('gear', 'tilt'): 'MLG Tilt',
            ('tilt', 'position'): 'MLG Tilt',
            ('tipped', 'forward'): 'MLG Tilt',

            ('gear', 'flaps',): 'Flaps vs Gear',

            ('hydraulic', 'failure'): 'Hydraulic Failure (All)',
            ('hydraulic', 'pressure'): 'Hydraulic Pumps',
            ('hydraulic', 'pump'): 'Hydraulic Pumps',
            ('hydraulic', 'pumps'): 'Hydraulic Pumps',
            ('hydraulic', 'power'): 'Hydraulic Pumps',
            ('hydraulic', 'systems'): 'Hydraulic Pumps',

            ('IDGA', 'AAIB'): 'AAIB (India)',
            ('indian', 'AAIB'): 'AAIB (India)',
            ('AAIB', 'india',): 'AAIB (India)',
            ('UK', 'AAIB'): 'AAIB (UK)',

            ('centre', 'tank'): 'Centre Tank',
            ('center', 'tank'): 'Centre Tank',

            ('electrical', 'failure'): 'Electrical Failure',
            ('electrical', 'fault'): 'Electrical Failure',
            ('electrical', 'issue'): 'Electrical Failure',

            ('flap', 'retraction'): 'Flap Retraction',
            ('flap', 'lever'): 'Flap Retraction',
            ('flap', 'retracted'): 'Flap Retraction',
            ('flap', 'setting'): 'Flap Setting',
            ('flap', 'position'): 'Flap Setting',

            ('mayday', 'call'): 'MAYDAY',
            ('radio', 'call'): 'MAYDAY',

            ('takeoff', 'roll'): 'Takeoff Roll',
            ('weight', 'wheels'): 'Weight on Wheels',

            ('bird', 'strike'): 'Bird Strike',
            ('bird', 'strikes'): 'Bird Strike',

            ('flight', 'recorder'): 'DFDR',
            ('flight', 'recorders'): 'DFDR',

            ('maintenance', 'error'): 'Maintenance Error',

            ('thread', 'closed'): 'Thread Closure',

            ('audio', 'analysis'): 'Audio Analysis',
            ('audio', 'samples'): 'Audio Analysis',
            ('audio', 'evidence'): 'Audio Analysis',
            ('doppler', 'shift'): 'Audio Analysis',
            ('doppler', 'effect'): 'Audio Analysis',
            ('frequency', 'plots'): 'Audio Analysis',
            ('acoustic', 'signatures'): 'Audio Analysis',
            ('acoustic', 'signature'): 'Audio Analysis',
            ('spectral', 'comparison'): 'Audio Analysis',

            ('water', 'ingress',): 'Water Ingress',
            ('water', 'leak',): 'Water Ingress',
            ('water', 'leakage',): 'Water Ingress',
            ('water', 'spillages',): 'Water Ingress',
            ('liquid', 'intrusion',): 'Water Ingress',
            ('ee', 'bays',): 'Water Ingress',

            ('preliminary', 'report',): 'Preliminary Report',
            ('prelim', 'report',): 'Preliminary Report',

            ('pilot', 'debrief',): 'Pilot Debrief',

            ('28Vdc', 'busses',): 'Electrical Busses',
            ('28VDC', 'busses',): 'Electrical Busses',
            ('dc', 'busses',): 'Electrical Busses',

            ('total', 'energy',): 'Total Energy',

            ('liftdrag', 'ratio',): 'Lift/Drag Ratio',

            ('richard', 'godfreys',): 'Self Proclaimed Experts',
            ('richard', 'godfrey',): 'Self Proclaimed Experts',
            ('geoffrey', 'thomas',): 'Self Proclaimed Experts',
            ('geoffrey', 'thomass',): 'Self Proclaimed Experts',

            ('memory', 'items',): 'Memory Items',
            ('memory', 'actions',): 'Memory Items',

            ('annex', '13',): 'Annex 13',

            ('simulation', 'scenarios',): 'Simulation Scenarios',

            ('spar', 'valve',): 'Spar Valves',
            ('spar', 'valves',): 'Spar Valves',

            ('startle', 'effect',): 'Startle Effect',

            ('51', 'days',): '51 Day Issue',

            ('action', 'slip',): 'Action slip',

            ('human', 'error',): 'Human Factors',
            ('human', 'factor',): 'Human Factors',
            ('human', 'factors',): 'Human Factors',

            # Note that this assumes 'of' is removed by the common words (in fact it is number 2 :-) ).
            ('timeline', 'events',): 'Timeline (Preliminary Report)',

            ('authority', 'gradient',): 'Authority Gradient',
            ('authority', 'gradients',): 'Authority Gradient',

            ('muscle', 'memory',): 'Muscle Memory',
            ('mental', 'health',): 'Mental Health',

            ('jump', 'seat',): 'Jump Seat',
            ('jump', 'seater',): 'Jump Seat',
            ('jump', 'seating',): 'Jump Seat',
            ('third', 'person',): 'Jump Seat',
            ('third', 'pilot',): 'Jump Seat',
            ('third', 'body',): 'Jump Seat',
            ('third', 'seat',): 'Jump Seat',
        },
        3: {
            ('dual', 'engine', 'failure'): 'Dual Engine Failure',
            ('double', 'engine', 'failure'): 'Dual Engine Failure',
            ('flaps', 'instead', 'gear'): 'Flaps vs Gear',
            ('dual', 'engine', 'shutdown'): 'Dual Engine Failure',
            ('improper', 'TCMA', 'activation'): 'TCMA (Improper Activation)',
            ('TCMA', 'airground', 'logic'): 'TCMA (Air-ground Logic)',
            ('engine', 'N2', 'overspeed'): 'N2 Over-speed',
            ('witnesses', 'RAT', 'hear'): 'RAT (Witnesses)',
            ('triple', 'hydraulic', 'failure'): 'Hydraulic Failure (Triple)',
            ('hydraulic', 'failure', 'double'): 'Hydraulic Failure (Double)',
            ('new', 'york', 'times'): 'New York Times',
            ('235VAC', 'backup', 'bus',): 'Electrical Busses',
            ('lift', 'drag', 'ratio',): 'Lift/Drag Ratio',
            ('take', 'brief', 'pause',): 'Thread Closure',
            ('indian', 'aviation', 'regulator'): 'DGCA',

            ('fuel', 'cutoff', 'switches'): 'Fuel Cutoff Switches',
            ('cut', 'off', 'switches'): 'Fuel Cutoff Switches',
            ('fuel', 'control', 'switches'): 'Fuel Cutoff Switches',
            ('engine', 'cutoff', 'switches'): 'Fuel Cutoff Switches',

            ('cockpit', 'area', 'audio'): 'Cockpit Area Audio',
            ('cockpit', 'area', 'microphone'): 'Cockpit Area Audio',

            ('landing', 'gear', ' lever'): 'Gear Lever',
            ('quick', 'windmill', 'relight'): 'Quick Windmill Relight',
            ('wall', 'street', 'journal'): 'Wall Street Journal',
        },
        4: {
            ('engine', 'driven', 'fuel', 'pump'): 'Fuel Pump (Engine Driven)',
            ('engine', 'driven', 'fuel', 'pumps'): 'Fuel Pump (Engine Driven)',
            ('shutdown', 'engine', 'N2', 'overspeed'): 'Engine Shutdown (Over-speed)',
            ('787genx', 'TCMA', 'airground', 'logic'): 'GEnx TCMA Logic',
            ('definitively', 'witnesses', 'RAT', 'hear'): 'RAT (Witnesses)',
            ('noise', 'listening', 'motorcycle', 'passing'): "RAT (Alternate Noise Sources)",
            ('engine', 'failure', 'detection', 'takes'): 'Engine Failure Detection Time',
            ('fuel', 'cut', 'off', 'switches'): 'Fuel Cutoff Switches',
            ('aviation', 'week', 'space', 'technology'): 'Aviation Week & Space Technology',
            ('indian', 'accident', 'investigation', 'team'): 'AAIB (IDGA)',
            ('indian', 'civil', 'air', 'authority'): 'DGCA',
            ('special', 'airworthiness', 'information', 'bulletin',): 'Special Airworthiness Information Bulletin',
            ('why', 'did', 'he', 'cutoff',): 'Pilot "Why did you cut off"',
            ('why', 'did', 'you', 'cutoff',): 'Pilot "Why did you cut off"',
        },
        5: {
            ('digital', 'flight', 'data', 'acquisition', 'unit',): 'Digital Flight Data Acquisition Unit',
            ('why', 'did', 'you', 'cut', 'off',): 'Pilot "Why did you cut off"',
        }
    }
    # The key is the pprune message permalink where the post is clearly about the subject
    # but the text does not refer to it.
    # This is a map of {permalink : subject, ...}
    SPECIFIC_POSTS_MAP = {
        11899702: 'Thread Moderation',
        11899920: 'Thread Moderation',
        11901310: 'Thread Moderation',
        11902773: 'Thread Moderation',
        11903346: 'Thread Moderation',
        11903792: 'Thread Moderation',
        11904254: 'Thread Moderation',
    }
    # Map of {subject_title : set(subject_title), ..}
    DUPLICATE_SUBJECT_MAP = {
        'RAT (Deployment)': {'RAT (All)', },
        'RAT (Electrical)': {'RAT (All)', },
        'RAT (Sound)': {'RAT (All)', },

        'TCMA (Improper Activation)': {'TCMA (All)', },
        'TCMA (Air-ground Logic)': {'TCMA (All)', },
        'TCMA (Logic)': {'TCMA (All)', },
        'TCMA (Shutdown)': {'TCMA (All)', },
        'GEnx TCMA Logic': {'TCMA (All)', },

        'N2 Over-speed': {'Engine Over-speed (All)', },
        'Engine Shutdown (Over-speed)': {'Engine Over-speed (All)', },

        'Hydraulic Failure (Triple)': {'Hydraulic Failure (All)', },
        'Hydraulic Failure (Double)': {'Hydraulic Failure (All)', },
        'Hydraulic Pumps': {'Hydraulic Failure (All)', },

        'Dual Engine Failure': {'Engine Failure (All)', },
        'Engine Shutdown': {'Engine Failure (All)', },
        'Wrong Engine': {'Engine Failure (All)', },

        'AAIB (IDGA)': {'AAIB (All)', },
        'AAIB (UK)': {'AAIB (All)', },

        'Flap Retraction': {'Flaps (All)', },
        'Flap Setting': {'Flaps (All)', },
        'Flaps vs Gear': {'Flaps (All)', },

        'Fuel Contamination': {'Fuel (All)', },
        'Fuel Pumps': {'Fuel (All)', },
        'Fuel Cutoff': {'Fuel (All)', },
        'Fuel Cutoff Switches': {'Fuel (All)', },

        'Fuel Cutoff Switches (detent)': {'Fuel (All)', 'Fuel Cutoff Switches', },

        'Timeline (Preliminary Report)': {'Preliminary Report', },
        'Quick Windmill Relight': {'Relight', },
    }
    # This the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    SIGNIFICANT_POSTS = (
        ('Summary of Main Theories', 11906480,),
        ('Thread Closure', 11908911,),
        ('Preliminary Report Timeline', 11921202,),
        ('Quick Windmill Relight', 11921747,),
        ('A 787 Pilot Speaks', 11924096,),
        ('tdracer on Air Accident Investigations', 11924194,),
        # https://www.pprune.org/accidents-close-calls/667141-preliminary-air-india-crash-report-published-65.html#post11924281
        ('787 Maintenance and those Fuel Cutoff Switches (15:00 onwards)', 11924281,),
        ('NTSB chair Jennifer Homendy on the Preliminary Report', 11925921,),
        ('The International Federation of Air Line Pilots\' Associations on the Preliminary Report', 11925980,),
    )
