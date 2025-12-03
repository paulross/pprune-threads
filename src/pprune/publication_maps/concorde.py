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
        '747': 'Boeing 747',
        'b747': 'Boeing 747',
        '747s': 'Boeing 747',
        'adcs': 'ADC (Air Data Computer)',
        'aicu': 'AICU (Air Intake Control Computer)',
        'aicus': 'AICU (Air Intake Control Computer)',
        'avionics': 'Avionics',
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
        'bac221': 'BAC221',
        'barbados': 'Barbados',

        'barbara': 'Barbara Harmer',

        'babylon': 'By the Rivers of Babylon',
        'bleed': 'Bleed Air',
        'boom': 'Sonic Boom',
        'booms': 'Sonic Boom',
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

        'checklist': 'Checklists',
        'checklists': 'Checklists',

        'cofg': 'C of G',
        'cog': 'C of G',
        'corrosion': 'Corrosion',
        'crash': 'Air France 4590',
        'dakar': 'Dakar',
        'davies': 'D. P. Davies',
        'depressurisation': 'Depressurisation',
        'depressurization': 'Depressurisation',
        'disaster': 'Air France 4590',
        'elevon': 'Elevons',
        'elevons': 'Elevons',
        'expansion': 'Expansion',
        'fairford': 'Fairford',
        'fatigue': 'Fatigue',
        'filton': 'Filton',
        'flameout': 'Flameout',
        'flameouts': 'Flameout',
        'fl600': 'FL600',
        'galley': 'Galley',
        'galleys': 'Galley',
        'glide': 'Glide',
        'gpus': 'Ground Power Unit',
        'gonesse': 'Air France 4590',
        'haynes': 'Haynes guide to Concorde',
        'heathrow': 'LHR',
        'hooker': 'Sir Stanley Hooker',
        'hp115': 'HP115',
        'hydraulic': 'Hydraulic',
        'hydrazine': 'Hydrazine',
        'ignitor': 'Ignitors',
        'ignitors': 'Ignitors',

        'inlet': 'Intakes',
        'intake': 'Intakes',
        'intakes': 'Intakes',

        'inss': 'INS (Inertial Navigation System)',

        'microprocessor': 'Microprocessor',
        'mmo': 'Mmo',
        'nosewheel': 'Landing Gear',
        'nozzle': 'Nozzles',
        'nozzles': 'Nozzles',
        'parachute': 'Parachute',
        'pressurisation': 'Pressurisation',

        'quiz': 'Quiz',
        'quizes': 'Quiz',

        'reheat': 'Afterburner/Re-heat',
        'reheats': 'Afterburner/Re-heat',
        'relight': 'Relight',

        'roundthebay': 'Round the Bay',

        'rollsroyce': 'Rolls Royce',
        'rudder': 'Rudder',

        'radalt': 'Radio Altimeter',

        'shockwave': 'Shockwave',
        'shockwaves': 'Shockwave',
        'shutdown': 'Engine Shutdown',
        'sideslip': 'Sideslip',
        'sidestick': 'Sidestick',
        'simulator': 'Simulator',
        'simulators': 'Simulator',
        'stagnation': 'Stagnation Point',
        'stewardess': 'Cabin Crew',
        'stewardesses': 'Cabin Crew',
        'landlady': 'Cabin Crew',

        'liftdrag': 'Lift Drag Ratio',

        'supercruise': 'Super-cruise',
        'surge': 'Engine surge',
        'surged': 'Engine surge',
        'surges': 'Engine surge',
        'tailcone': 'Tail Cone',
        'tailwheel': 'Tailwheel',
        'trim': 'Trim',
        'shannon': 'Shannon',
        'toulouse': 'Toulouse',
        'tyres': 'Tyres',
        'tmo': 'TMO (Temprature Max Operating)',

        'tu144': 'Tu-144',
        'concordski': 'Tu-144',
        'russian': 'Tu-144',
        'russians': 'Tu-144',
        'mi6': 'Tu-144',
        'tu144d': 'Tu-144',
        # Missing space in 'Concorde,Tu-144'
        'concordetu144': 'Tu-144',

        'ullage': 'Ullage (Fuel)',

        'undercarridge': 'Landing Gear',
        'visor': 'Visor',
        'vortex': 'Vortex',
        'vorticies': 'Vortex',
        'vmo': 'Vmo',
        'vd': 'Vd',

        'vref': 'Vref',
        'vref5': 'Vref',
        'vref7': 'Vref',
        'vref10': 'Vref',
    }

    # This maps capitilised words (stripped of punctuation) to their subject.
    # Any post that has that capitilised word in it is treated as part of that subject.
    CAPS_WORDS_MAP = {
        k: k for k in {
            'CDG', 'LHR', 'JFK', 'V1', 'V2',
        }
    }
    # This maps capitalised words (stripped of punctuation) to their subject with ' (All)' as a suffix. .
    CAPS_WORDS_MAP_ALL = {}
    # This maps capitalised words (stripped of punctuation) to their subject.
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
        'B747': 'Boeing 747',
        'BA': 'British Airways',
        'BLUE': 'Hydraulic System - BLUE',
        'CG': 'C of G',
        'CC': 'Cabin Crew',
        'FL600': 'FL600',
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
        'HP115': 'HP-115',
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
        'SC1': 'Short SC-1',
        'SR71': 'SR-71',
        'TAS': 'TAS (True Air Speed)',
        'TAT': 'TAT (Total Air Temperature)',
        'TLA': 'TLA (Throttle Lever Angle)',
        'TMO': 'TMO (Temprature Max Operating)',
        'TU144': 'Tu-144',
        'TU144D': 'Tu-144',
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
            ('barber', 'pole'): 'Barber Pole',
            ('boeing', 'SST'): 'Boeing SST',
            ('barbara', 'harmer'): 'Barbara Harmer',
            ('brian', 'calvert'): 'Brian Calvert',
            ('brian', 'wadpole'): 'Brian Walpole',
            ('brian', 'walpole'): 'Brian Walpole',
            ('brize', 'norton'): 'Brize Norton',
            ('bristol', 'siddeley'): 'Bristol Siddeley',
            ('chris', 'norris'): 'Chris Norris',
            ('CLIMB', 'MAX'): 'Climb Performance',
            ('C', 'G'): 'C of G',
            ('concorde', 'simulator'): 'Concorde Simulator',

            ('concorde', 'routing',): 'Concorde Routings',
            ('concorde', 'routings',): 'Concorde Routings',
            ('oceanic', 'routings',): 'Concorde Routings',
            ('crown', 'modification',): 'Crown Modification',
            ('crown', 'modifications',): 'Crown Modification',

            ('cross', 'wind',): 'Cross Wind Limit',

            ('conversion', 'course'): 'Conversion Course',
            ('Chris', 'Norris'): 'Chris Norris',
            ('cabin', 'crew'): 'Cabin Crew',
            ('delta', 'golf'): 'G-BBDG',
            ('engine', 'failure'): 'Engine Failure',

            ('emergency', 'descent'): 'Depressurisation',
            ('window', 'failure'): 'Depressurisation',

            ('female', 'pilots'): 'Female Pilots',
            ('flight', 'envelope'): 'Flight Envelope',

            ('fuel', 'pump'): 'Fuel Pumps',
            ('fuel', 'pumps'): 'Fuel Pumps',
            ('fuel', 'vent'): 'Fuel Vent System',
            ('fuel', 'burn'): 'Fuel Burn',

            # ('fuel', 'incident'): 'Fuel Incident',

            ('green', 'system'): 'GREEN Hydraulic System',
            ('hand', 'flying'): 'Hand Flying',
            ('hydraulic', 'contamination'): 'Hydraulic Failure/Contamination',
            ('hydraulic', 'failures'): 'Hydraulic Failure/Contamination',
            ('HP', 'compressor'): 'HP Compressor',
            ('hp', 'compressor'): 'HP Compressor',
            ('HP', 'turbine'): 'HP Turbine',
            ('hp', 'turbine'): 'HP Turbine',
            ('JFK', 'departures'): 'LHR-JFK Route',
            ('JFK', 'LHR'): 'LHR-JFK Route',
            ('john', 'cook'): 'John Cook',
            ('keith', 'myers'): 'Keith Myers',
            ('landing', 'gear'): 'Landing Gear',

            ('lift', 'drag'): 'Lift Drag Ratio',

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
            ('mike', 'bannister'): 'Mike Bannister',
            ('nose', 'gear'): 'Landing Gear',
            ('nose', 'leg'): 'Landing Gear',
            ('nose', 'wheel'): 'Landing Gear',
            ('nozzle', 'reverser'): 'Thrust Reversers',
            ('Olympus', '593'): 'Olympus 593',
            ('nozzle', 'reverser'): 'Thrust Reversers',
            ('pilot', 'selection'): 'Pilot Selection',
            ('prototype', 'fleet',): 'Prototype Fleet',

            ('radio', 'altimeter',): 'Radio Altimeter',
            ('radar', 'altimeter',): 'Radio Altimeter',

            ('RAE', 'farnborough'): 'RAE Farnborough',
            ('rivers', 'babylon'): 'By the Rivers of Babylon',
            ('rolls', 'royce'): 'Rolls Royce',
            ('rotating', 'stall'): 'Rotating (engine) Stall',

            ('reverse', 'thrust'): 'Reverse Thrust',

            ('stick', 'shaker'): 'Stick Shaker',

            ('stan', 'hookers',): 'Sir Stanley Hooker',

            ('takeoff', 'thrust'): 'Take-off Thrust',
            ('tail', 'skid'): 'Tail Skid',
            ('tyre', 'life'): 'Tyre Life',

            ('trivia', 'questions'): 'Quiz',
            ('stinky', 'questions'): 'Quiz',
            ('concorde', 'quiz'): 'Quiz',
            ('concorde', 'quizes'): 'Quiz',

            ('taxy', 'lights'): 'Landing & Taxy Lights',
            ('temperature', 'shear'): 'Temperature Shear',
            ('temperature', 'shears'): 'Temperature Shear',
            ('transonic', 'acceleration'): 'Transonic Acceleration',
            ('thrust', 'recuperator'): 'Thrust Recuperator',
            ('technical', 'diagrams'): 'Technical Diagrams',
            ('vortex', 'aoa'): 'Vortex AoA',
            # We want to eliminate 'the'
            ('round', 'bay',): 'Round the Bay',
        },
        3: {
            ('c', 'of', 'g',): 'C of G',
            ('head', 'up', 'display',): 'HUD (Head Up Display)',
            ('flight', 'plan', 'segment',): 'Concorde Routings',
            # 'How many wheels on the aircraft'
            ('how', 'many', 'wheels'): 'Quiz',
            ('flight', 'crew', 'positions',): 'Flight Crew Positions',
        },
        4: {
            ('how', 'many', 'wheel', 'brakes'): 'Quiz',
        }
    }
    # The key is the pprune permalink number where the post is clearly about the subject
    # but the text does not refer to it.
    # This is a map of {permalink : subject, ...}
    SPECIFIC_POSTS_MAP = {
        5917048: 'Flight Envelope',  # Post 225 by pprunes counting
        5917084: 'Flight Envelope',
        # https://www.pprune.org/tech-log/423988-concorde-question-108.html#post5918963
        5918963: 'Olympus 593',  # Post 250 by pprunes counting
        # # https://www.pprune.org/tech-log/423988-concorde-question-16.html#post5926053
        # 5926053: 'John Cook',
        # https://www.pprune.org/tech-log/423988-concorde-question-108.html#post5930300
        5930300: 'C of G',  # Post 331 by pprunes counting
        # https://www.pprune.org/tech-log/423988-concorde-question-108.html#post5930647
        5930647: 'C of G',  # Post 333 by pprunes counting
        # # https://www.pprune.org/tech-log/423988-concorde-question-24.html#post5954015
        # 5954015: 'John Cook',  # Post 463
        # https://www.pprune.org/tech-log/423988-concorde-question-30.html#post6012930
        # 6012930: 'John Cook', # Post 600
        # # https://www.pprune.org/tech-log/423988-concorde-question-108.html#post6042205
        # 6042205: 'HUD (Head Up Display)', # Post 664
        # https://www.pprune.org/tech-log/423988-concorde-question-52.html#post6144908
        6144908: 'Relight',  # Post 1023
        # https://www.pprune.org/tech-log/423988-concorde-question-53.html#post6149785
        6149785: 'Captains',  # Post 1049
        # https://www.pprune.org/tech-log/423988-concorde-question-84.html#post7389576
        7389576: 'Tu-144',  # Post 1665
        # https://www.pprune.org/tech-log/423988-concorde-question-108.html#post8937925
        8937925: 'Parachute',  # Post 1860
        # 1937: 'John Cook',
        # https://www.pprune.org/tech-log/423988-concorde-question-108.html#post11681790
        11681790: 'Technical Diagrams',
    }
    # Map of {subject_title : set(subject_title), ..}
    DUPLICATE_SUBJECT_MAP = {}
    # This the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    # Tuple[Tuple[str, permalink], ...]
    SIGNIFICANT_POSTS = tuple()
