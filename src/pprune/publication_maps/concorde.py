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
import typing

from pprune.publication_maps import publication_map_abc


class Concorde(publication_map_abc.PublicationMapABC):
    def get_title(self) -> str:
        return 'Concorde Re-Mixed'

    def get_introduction_in_html(self) -> str:
        return """<a href="https://www.pprune.org/tech-log/423988-concorde-question.html">This thread</a> on Tech log has 108 pages about Concorde.
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
        return False

    # Map of {lower_case_word : subject_title, ..}
    LC_WORDS_MAP = {
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
    CAPS_WORDS_MAP = {
        k: k for k in {
            'CDG', 'LHR', 'JFK', 'V1', 'V2',
        }
    }
    # This maps capitilised words (stripped of punctuation) to their subject with ' (All)' as a suffix. .
    CAPS_WORDS_MAP_ALL = {}
    # This maps capitilised words (stripped of punctuation) to their subject.
    # Any post that has that capitilised word in it is treated as part of that subject.
    CAPS_WORDS_MAP_EXTRA = {
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
        'JC': 'John Cook',
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
        'YELLOW': 'Hydraulic System - YELLOW',
    }
    # ('fuel', 'pump') -> "Fuel Pumps"
    # Each part of the key should be lower case unless all caps
    PHRASES_MAP = {
        2: {
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
    }
    # The key is the pprune message number where the post is clearly about the subject
    # but the text does not refer to it.
    # The key is the pprune message permalink where the post is clearly about the subject
    # but the text does not refer to it.
    # This is a map of {permalink : subject, ...}
    # TODO: Change to permalinks.
    SPECIFIC_POSTS_MAP = {
        5917048: 'Flight Envelope',  # Post 225 by pprunes counting
        # https://www.pprune.org/tech-log/423988-concorde-question-108.html#post5918963
        5918963: 'Olympus 593',  # Post 250 by pprunes counting
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
    # Map of {subject_title : set(subject_title), ..}
    DUPLICATE_SUBJECT_MAP = {}
    # This the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    # Tuple[Tuple[str, permalink], ...]
    SIGNIFICANT_POSTS = tuple()
