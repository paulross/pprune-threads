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
    def get_specific_posts_to_subject_map(self) -> typing.Dict[str, str]:
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
        return ret

    @abc.abstractmethod
    def get_significant_posts_permalinks(self) -> typing.Set[str]:
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


class ConcordePublicationMap(PublicationMap):
    """Specialisation for the Concorde thread."""

    def get_title(self) -> str:
        return 'Concorde Re-mixed'

    def get_introduction_in_html(self) -> str:
        return """<p>There is a great 
    <a href="http://www.pprune.org/tech-log/423988-concorde-question.html">thread on pprune</a>
    that contains a fascinating discussion from experts about Concorde.
    The thread has nearly 2000 posts and around 100 pages.
    Naturally enough it is ordered in time of each post but since it covers
    so many subjects it is a little hard to follow a particular subject.
</p>"""

    def get_lowercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        return self.WORDS_MAP

    def get_uppercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        return self.CAPS_WORDS

    def get_phrase_lengths(self) -> typing.List[int]:
        return [2, ]

    def get_phrases_to_subject_map(self, phrase_length: int) -> typing.Dict[str, str]:
        if phrase_length == 2:
            return self.PHRASES_2_MAP
        return {}

    def get_specific_posts_to_subject_map(self) -> typing.Dict[str, str]:
        return self.SPECIFIC_POSTS_MAP

    def get_duplicate_subjects(self, subject: str) -> typing.Set[str]:
        return set()

    def get_significant_posts_permalinks(self) -> typing.Set[str]:
        return self.SIGNIFICANT_POSTS

    def get_set_of_words_required(self) -> typing.Set[str]:
        return set()

    def get_number_of_top_authors(self) -> int:
        return 40

    def get_upvoted_post_count_limit(self) -> int:
        return 25

    def get_upvoted_post_text_limit(self) -> int:
        return 256

    # Map of {lower_case_word : subject_title, ..}
    WORDS_MAP = {
        '214': 'G-BOAG',
        '216': 'G-BOAF',
        '593': 'Olympus 593',
        'abatement': 'Noise Abatement',
        'accident': 'Air France 4590',
        'aerospatiale': 'Aerospatiale',
        'afterburner': 'Afterburner/Re-heat',
        'airbus': 'Airbus',
        'antiskid': 'Anti-skid',
        'aoa': 'AoA',
        'apus': 'Auxiliary Power Unit',
        'autoland': 'Auto-land',
        'autopilot': 'Auto-pilot',
        'autostab': 'Auto-stabilisation',
        'autostabs': 'Auto-stabilisation',
        'autothrottle': 'Auto-throttle',
        'autotrim': 'Auto-trim',
        'bleed': 'Bleed Air',
        'boeing': 'Boeing',
        'bourget': 'Le Bourget',
        'brakes': 'Braking',
        'braking': 'Braking',
        'braniff': 'Braniff',
        'brooklands': 'Brooklands',
        'bucket': 'Thrust Reversers',
        'buckets': 'Thrust Reversers',
        'captain': 'Captains',
        'captains': 'Captains',
        'cofg': 'C of G',
        'cog': 'C of G',
        'corrosion': 'Corrosion',
        'crash': 'Air France 4590',
        'dakar': 'Dakar',
        'depressurisation': 'Depressurisation',
        'depressurization': 'Depressurisation',
        'disaster': 'Air France 4590',
        'elevon': 'Elevons',
        'elevons': 'Elevons',
        'fairford': 'Fairford',
        'fatigue': 'Fatigue',
        'filton': 'Filton',
        'flameout': 'Flameout',
        'flameouts': 'Flameout',
        'galley': 'Galley',
        'galleys': 'Galley',
        'glide': 'Glide',
        'gpus': 'Ground Power Unit',
        'gonesse': 'Air France 4590',
        'haynes': 'Haynes guide to Concorde',
        'heathrow': 'LHR',
        'hooker': 'Sir Stanley Hooker',
        'hydraulic': 'Hydraulic',
        'hydrazine': 'Hydrazine',
        'ignitor': 'Ignitors',
        'ignitors': 'Ignitors',
        'inlet': 'Intakes',
        'intakes': 'Intakes',
        'microprocessor': 'Microprocessor',
        'mmo': 'Mmo',
        'nosewheel': 'Landing Gear',
        'nozzle': 'Nozzles',
        'nozzles': 'Nozzles',
        'parachute': 'Parachute',
        'pressurisation': 'Pressurisation',
        'reheat': 'Afterburner/Re-heat',
        'reheats': 'Afterburner/Re-heat',
        'relight': 'Relight',
        'rollsroyce': 'Rolls Royce',
        'rudder': 'Rudder',
        'shockwave': 'Shockwave',
        'shockwaves': 'Shockwave',
        'shutdown': 'Engine Shutdown',
        'sideslip': 'Sideslip',
        'sidestick': 'Sidestick',
        'simulator': 'Simulator',
        'simulators': 'Simulator',
        'stagnation': 'Stagnation Point',
        'stewardess': 'Cabin Crew',
        'supercruise': 'Super-cruise',
        'surge': 'Engine surge',
        'surged': 'Engine surge',
        'surges': 'Engine surge',
        'tailcone': 'Tail Cone',
        'tailwheel': 'Tailwheel',
        'toulouse': 'Toulouse',
        'tyres': 'Tyres',
        'tu144': 'Tu-144',
        'undercarridge': 'Landing Gear',
        'visor': 'Visor',
        'vortex': 'Vortex',
        'vorticies': 'Vortex',
    }

    # This maps capitilised words (stripped of punctuation) to their subject.
    # Any post that has that capitilised word in it is treated as part of that subject.
    CAPS_WORDS = {
        'ADC': 'ADC (Air Data Computer)',
        'AF': 'Air France',
        'AFCS': 'AFCS (Automtic Flight Control System)',
        'AICS': 'AICS (Air Intake Control System)',
        'AICU': 'AICU (Air Intake Control Computer)',
        'APU': 'APU (Auxiliary Power Unit)',
        'AUTOSTAB': 'Auto-stabilisation',
        'AUTOLAND': 'Auto-land',
        'BA': 'British Airways',
        'BLUE': 'Hydraulic System - BLUE',
        'CDG': 'CDG',
        'CG': 'C of G',
        'CC': 'Cabin Crew',
        'FBW': 'FBW (Fly By Wire)',
        'FBTSC': 'F-BTSC',
        'FBTSD': 'F-BTSD',
        'FBVFA': 'F-BVFA',
        'FBVFC': 'F-BVFC',
        'FBVFD': 'F-BVFD',
        'FWTSA': 'F-WTSA',
        'FWTSB': 'F-WTSB',
        'GAXDN': 'G-AXDN',
        'GBBDG': 'G-BBDG',
        'GBFKW': 'G-BFKW',
        'GBOAA': 'G-BOAA',
        'GBOAB': 'G-BOAB',
        'GBOAC': 'G-BOAC',
        'GBOAD': 'G-BOAD',
        'GBOAE': 'G-BOAE',
        'GBOAF': 'G-BOAF',
        'GBOAG': 'G-BOAG',
        'GN81AC': 'G-N81AC',
        'GPU': 'GPU (Ground Power Unit)',
        'GREEN': 'Hydraulic System - GREEN',
        'HUD': 'HUD (Head Up Display)',
        'IAS': 'IAS (Indicated Air Speed)',
        'INS': 'INS (Inertial Navigation System)',
        'ITVV': 'Intelligent Television and Video',
        'JFK': 'JFK',
        'JC': 'John Cook',
        'LHR': 'LHR',
        'LHRBGI': 'LHR-BGI Route',
        'LHRJFK': 'LHR-JFK Route',
        'MEPU': 'MEPU (Monogol Emergency Power Unit)',
        'N1': 'N1 (revolutions)',
        'PFCU': 'PFCU (Powered Flying Control Units)',
        'RAT': 'RAT (Ram Air Turbine)',
        'RR': 'Rolls Royce',
        'SR71': 'SR-71',
        'TAS': 'TAS (True Air Speed)',
        'TAT': 'TAT (Total Air Temperature)',
        'TLA': 'TLA (Throttle Lever Angle)',
        'TMO': 'TMO (Temprature Max Operating)',
        'TU144': 'Tu-144',
        'V1': 'V1',
        'V2': 'V2',
        'YELLOW': 'Hydraulic System - YELLOW',
    }

    # ('fuel', 'pump') -> "Fuel Pumps"
    # Each part of the key should be lower case unless all caps
    PHRASES_2_MAP = {
        ('ALT', 'HOLD'): 'ALT HOLD',
        ('aoa', 'concorde'): 'AoA',
        ('aoa', 'stall'): 'AoA',
        ('aoa', 'vortex'): 'AoA',
        ('aoa', 'vortices'): 'AoA',
        ('auto', 'stabilisation'): 'Auto-stabilisation',
        ('boeing', 'SST'): 'Boeing SST',
        ('barbara', 'harmer'): 'Barbara Harmer',
        ('brian', 'calvert'): 'Brian Calvert',
        ('brian', 'wadpole'): 'Brian Walpole',
        ('brian', 'walpole'): 'Brian Walpole',
        ('CLIMB', 'MAX'): 'Climb Performance',
        ('C', 'G'): 'C of G',  # 'of' is stripped out by common words.
        ('concorde', 'simulator'): 'Concorde Simulator',
        ('Chris', 'Norris'): 'Chris Norris',
        ('cabin', 'crew'): 'Cabin Crew',
        ('delta', 'golf'): 'G-BBDG',
        ('engine', 'failure'): 'Engine Failure',
        ('female', 'pilots'): 'Female Pilots',
        ('flight', 'envelope'): 'Flight Envelope',
        ('fuel', 'pump'): 'Fuel Pumps',
        ('fuel', 'pumps'): 'Fuel Pumps',
        ('fuel', 'vent'): 'Fuel Vent System',
        ('green', 'system'): 'GREEN Hydraulic System',
        ('hand', 'flying'): 'Hand Flying',
        ('hydraulic', 'contamination'): 'Hydraulic Failure/Contamination',
        ('hydraulic', 'failures'): 'Hydraulic Failure/Contamination',
        ('HP', 'compressor'): 'HP Compressor',
        ('HP', 'turbine'): 'HP Turbine',
        ('JFK', 'departures'): 'LHR-JFK Route',
        ('JFK', 'LHR'): 'LHR-JFK Route',
        ('John', 'Cook'): 'John Cook',
        ('landing', 'gear'): 'Landing Gear',
        ('landing', 'lamps'): 'Landing & Taxy Lights',
        ('landing', 'lights'): 'Landing & Taxy Lights',
        ('le', 'bourget'): 'Le Bourget',
        ('LHR', 'JFK'): 'LHR-JFK Route',
        ('LHR', 'runways'): 'LHR Operations',
        ('LP', 'compressor'): 'LP Compressor',
        ('LP', 'turbine'): 'LP Turbine',
        ('main', 'gear'): 'Landing Gear',
        ('mach', 'trim'): 'Mach Trim',
        ('mach', 'trimmer'): 'Mach Trim',
        ('mach', 'trimming'): 'Mach Trim',
        ('nose', 'gear'): 'Landing Gear',
        ('nose', 'leg'): 'Landing Gear',
        ('nose', 'wheel'): 'Landing Gear',
        ('nozzle', 'reverser'): 'Thrust Reversers',
        ('Olympus', '593'): 'Olympus 593',
        ('nozzle', 'reverser'): 'Thrust Reversers',
        ('pilot', 'selection'): 'Pilot Selection',
        ('RAE', 'farnborough'): 'RAE Farnborough',
        ('rivers', 'babylon'): 'By the Rivers of Babylon',
        ('Rolls', 'Royce'): 'Rolls Royce',
        ('rotating', 'stall'): 'Rotating (engine) Stall',
        ('stick', 'shaker'): 'Stick Shaker',
        ('taxy', 'lights'): 'Landing & Taxy Lights',
        ('temperature', 'shear'): 'Temperature Shear',
        ('temperature', 'shears'): 'Temperature Shear',
        ('transonic', 'acceleration'): 'Transonic Acceleration',
        ('thrust', 'recuperator'): 'Thrust Recuperator',
        ('vortex', 'aoa'): 'Vortex AoA',
    }

    # The key is the pprune message number where the post is clearly about the subject
    # but the text does not refer to it.
    # This is a map of {permalink : subject, ...}
    # TODO: Change these to permalinks.
    SPECIFIC_POSTS_MAP = {
        225: 'Flight Envelope',  # Post 225 by pprunes counting
        250: 'Olympus 593',  # Post 250 by pprunes counting
        310: 'John Cook',
        333: 'C of G',  # Post 333 by pprunes counting
        463: 'John Cook',
        600: 'John Cook',
        664: 'HUD (Head Up Display)',
        1023: 'Relight',
        1049: 'Captains',
        1666: 'Tu-144',
        1861: 'Parachute',
        1937: 'John Cook',
    }
    # The is the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    SIGNIFICANT_POSTS = set()


class AirIndia171(PublicationMap):
    def get_title(self) -> str:
        return 'AI171 Re-mixed'

    def get_introduction_in_html(self) -> str:
        return """There are these threads on pprune about the accident to
 <a href="https://en.wikipedia.org/wiki/Air_India_Flight_171">Air India Flight 171 [Wikipedia]</a>
 on 12 June 2025:
    <ol>
        <li><a href="https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html">Part One [pprune]</a> (now closed)</li>
        <li><a href="https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html">Part Two [pprune]</a></li>
        <li>There is also a thread on the
            <a href="https://www.pprune.org/accidents-close-calls/666714-moderation-air-india-accident-threads.html">moderation of these threads [pprune]</a>
             (this is not included in this analysis)
         </li>
    </ol>
    <p><b>My condolences to all the people affected by this accident, in particular to the friends and families of the victims.</b></p>
"""

    def get_lowercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        return self.LC_WORDS_MAP

    def get_uppercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        result = self.CAPS_WORDS_MAP.copy()
        result.update(self.CAPS_WORDS_MAP_ALL)
        result.update(self.CAPS_WORDS_MAP_EXTRA)
        result['MAYDAY'] = "Mayday"
        result['HPSOV'] = "High Pressure Shutoff Valve"
        result['FR24'] = "FlightRadar24"
        return result

    def get_phrase_lengths(self) -> typing.List[int]:
        return sorted(self.PHRASES_MAP.keys())

    def get_phrases_to_subject_map(self, phrase_length: int) -> typing.Dict[str, str]:
        if phrase_length in self.get_phrase_lengths():
            return self.PHRASES_MAP[phrase_length]
        return {}

    def get_specific_posts_to_subject_map(self) -> typing.Dict[str, str]:
        return self.SPECIFIC_POSTS_MAP

    def get_duplicate_subjects(self, subject: str) -> typing.Set[str]:
        if subject in self.DUPLICATE_SUBJECT_MAP:
            return self.DUPLICATE_SUBJECT_MAP[subject]
        return set()

    def get_significant_posts_permalinks(self) -> typing.Set[str]:
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

    # Map of {lower_case_word : subject_title, ..}
    LC_WORDS_MAP = {
        'mayday': 'Mayday',
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
    }
    # This maps capitilised words (stripped of punctuation) to their subject.
    # Any post that has that capitilised word in it is treated as part of that subject.
    CAPS_WORDS_MAP = {
        k: k for k in {
            'AI171', 'ADSB', 'APU', 'BBC', 'CCTV', 'EXDAC', 'FDR', 'V1', 'V2', 'EDML', 'EAFR',
            'FADEC', 'FAA', 'TOGA', 'VNAV', 'NTSB', 'MEL', 'DFDR', 'FBW', 'HPSOV', 'FCOM', 'FR24', 'CVR', 'EFATO',
            'RIPS', 'TRU', 'ARINC',
        }
    }
    CAPS_WORDS_MAP_ALL = {
        k: k + ' (All)' for k in [
            'RAT', 'TCMA', 'AAIB', 'MLG',
        ]
    }
    CAPS_WORDS_MAP_EXTRA = {
        'NYT': 'New York Times',
        'AWST': 'Aviation Week & Space Technology',
        'AD': 'Air Worthiness Directives',
        'ADs': 'Air Worthiness Directives',
        'EAFRs': 'EAFR',
        'TRUs': 'TRU',
        'DFDAU': 'Digital Flight Data Acquisition Unit'
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
            ('fuel', 'switch'): 'Fuel Cutoff',
            ('fuel', 'switches'): 'Fuel Cutoff',
            ('cutoff', 'switches'): 'Fuel Cutoff',
            ('cut', 'off'): 'Fuel Cutoff',

            ('fuel', 'pump'): 'Fuel Pumps',
            ('fuel', 'pumps'): 'Fuel Pumps',
            ('fuel', 'flow'): 'Fuel Pumps',
            ('fuel', 'supply'): 'Fuel Pumps',
            ('boost', 'pumps'): 'Fuel Pumps',
            ('suction', 'feed'): 'Fuel Pumps',

            ('gear', 'doors'): 'Gear Retraction',
            ('gear', 'lever'): 'Gear Retraction',
            ('gear', 'retraction'): 'Gear Retraction',
            ('gear', 'down'): 'Gear Retraction',
            ('gear', 'selected'): 'Gear Retraction',
            ('landing', 'gear'): 'Gear Retraction',
            ('doors', 'open'): 'Gear Retraction',

            ('bogie', 'tilting'): 'MLG Tilt',
            ('bogies', 'tilt'): 'MLG Tilt',
            ('gear', 'tilt'): 'MLG Tilt',
            ('tilt', 'position'): 'MLG Tilt',
            ('tipped', 'forward'): 'MLG Tilt',
            # ('gear', 'tilt') Is found with comon words (200). Maybe need a test?

            ('gear', 'flaps',): 'Flaps vs Gear',

            ('hydraulic', 'failure'): 'Hydraulic Failure (All)',
            ('hydraulic', 'pressure'): 'Hydraulic Pumps',
            ('hydraulic', 'pump'): 'Hydraulic Pumps',
            ('hydraulic', 'pumps'): 'Hydraulic Pumps',
            ('hydraulic', 'power'): 'Hydraulic Pumps',
            ('hydraulic', 'systems'): 'Hydraulic Pumps',

            ('IDGA', 'AAIB'): 'AAIB (IDGA)',
            ('indian', 'AAIB'): 'AAIB (IDGA)',
            ('AAIB', 'india',): 'AAIB (IDGA)',
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

            ('mayday', 'call'): 'Mayday',
            ('radio', 'call'): 'Mayday',

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

            ('pilot', 'debrief',): 'Pilot Debrief',

            ('28Vdc', 'busses',): 'Electrical Busses',
            ('28VDC', 'busses',): 'Electrical Busses',
            ('dc', 'busses',): 'Electrical Busses',
        },
        3: {
            ('dual', 'engine', 'failure'): 'Dual Engine Failure',
            ('double', 'engine', 'failure'): 'Dual Engine Failure',
            ('flaps', 'instead', 'gear'): 'Flaps vs Gear',
            ('dual', 'engine', 'shutdown'): 'Dual Engine Failure',
            ('improper', 'TCMA', 'activation'): 'TCMA (Improper Activation)',
            ('fuel', 'cutoff', 'switches'): 'Fuel Cut Off Switches',
            ('TCMA', 'airground', 'logic'): 'TCMA (Air-ground Logic)',
            ('engine', 'N2', 'overspeed'): 'N2 Over-speed',
            ('witnesses', 'RAT', 'hear'): 'RAT (Witnesses)',
            ('triple', 'hydraulic', 'failure'): 'Hydraulic Failure (Triple)',
            ('hydraulic', 'failure', 'double'): 'Hydraulic Failure (Double)',
            ('new', 'york', 'times'): 'New York Times',
            ('235VAC', 'backup', 'bus',): 'Electrical Busses',
        },
        4: {
            ('engine', 'driven', 'fuel', 'pump'): 'Fuel Pump (Engine Driven)',
            ('engine', 'driven', 'fuel', 'pumps'): 'Fuel Pump (Engine Driven)',
            ('shutdown', 'engine', 'N2', 'overspeed'): 'Engine Shutdown (Over-speed)',
            ('787genx', 'TCMA', 'airground', 'logic'): 'GEnx TCMA Logic',
            ('definitively', 'witnesses', 'RAT', 'hear'): 'RAT (Witnesses)',
            ('noise', 'listening', 'motorcycle', 'passing'): "RAT (Alternate Noise Sources)",
            ('engine', 'failure', 'detection', 'takes'): 'Engine Failure Detection Time',
            ('fuel', 'cut', 'off', 'switches'): 'Fuel Cut Off Switches',
            ('aviation', 'week', 'space', 'technology'): 'Aviation Week & Space Technology',
            ('indian', 'accident', 'investigation', 'team'): 'AAIB (IDGA)',
        },
        5: {
            ('digital', 'flight', 'data', 'acquisition', 'unit',): 'Digital Flight Data Acquisition Unit',
        }
    }
    # The key is the pprune message permalink where the post is clearly about the subject
    # but the text does not refer to it.
    # This is a map of {permalink : subject, ...}
    SPECIFIC_POSTS_MAP = {
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-20.html#post11899702': 'Thread Moderation',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-25.html#post11899920': 'Thread Moderation',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-51.html#post11901310': 'Thread Moderation',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-78.html#post11902773': 'Thread Moderation',
        'https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-87.html#post11903346': 'Thread Moderation',
        'https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-5.html#post11903792': 'Thread Moderation',
        'https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-11.html#post11904254': 'Thread Moderation',
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
    }
    # The is the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    SIGNIFICANT_POSTS = {
        'https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-37.html#post11906480',
        'https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-56.html#post11908911',
    }
