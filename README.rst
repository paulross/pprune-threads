=========================
Remixes of prune threads.
=========================

This describes how to reorganise a pprune thread by subject.

--------------------------------------------
Air India Flight 171 at Ahmedabad 2025-06-12
--------------------------------------------

https://en.wikipedia.org/wiki/Air_India_Flight_171

Original threads:

1. https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html
2. https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html

There is also https://www.pprune.org/accidents-close-calls/666714-moderation-air-india-accident-threads.html

Pulling Down the Thread(s)
--------------------------

.. code-block:: shell

    $ cd threads/AI171-1
    $ curl https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad.html -o "666472-plane-crash-near-ahmedabad.html"
    $ grep 'Last Page' 666472-plane-crash-near-ahmedabad.html

This gives:

.. code-block:: shell

    <li><a id="mb_pagelast" class="button primary hollow" href="https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-87.html?ispreloading=1" title="Last Page - Results 1,721 to 1,729 of 1,729">Last <i class="fas fa-angle-double-right"></i></a></li>

So the last page is ``666472-plane-crash-near-ahmedabad-87.html``

And all the rest:

.. code-block:: shell

    $ time curl https://www.pprune.org/accidents-close-calls/666472-plane-crash-near-ahmedabad-[2-87].html -o "666472-plane-crash-near-ahmedabad-#1.html"
    ...
    real	0m35.544s
    user	0m0.176s
    sys	0m0.356s

Then:

.. code-block:: shell

    $ cd threads/AI171-2
    $ curl https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html -o "666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html"
    $ grep 'Last Page' 666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html

This gives:

.. code-block:: shell

    <li><a id="mb_pagelast" class="button primary hollow" href="https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-56.html?ispreloading=1" title="Last Page - Results 1,061 to 1,074 of 1,074">Last <i class="fas fa-angle-double-right"></i></a></li>```

So the last page is ``https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-56.html``

And all the rest:

.. code-block:: shell

    $ time curl https://www.pprune.org/accidents-close-calls/666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-[2-56].html -o "666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-#1.html"
    ...
    real	0m35.544s
    user	0m0.176s
    sys	0m0.356s

Conducting Research
-------------------

There is a script ``src/pprune/research.py`` that analyses the thread for words and phrases.


Words that are all Capitals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the ``--all-cap-words`` to list words in all capitals.

The first part of the output is ordered most-common first with the word count.
The first part of the output is ordered alphabetically with the word count.

.. code-block:: shell

    $ python src/pprune/research.py --all-cap-words --freq-ge=50 threads/AI171_B/AI171-1 threads/AI171_B/AI171-2
    2025-06-24 11:07:31,753 -             read_html.py#288  - INFO     - Read: 666472-plane-crash-near-ahmedabad.html posts: 20
    ...
    2025-06-24 11:07:48,025 -             read_html.py#290  - INFO     - update_whole_thread(): Read 2832 posts in 6.312 (s)
    Number of posts: 2832
    Number of words: 427262
    Number of common words: 1000
    --------------- print_all_caps(): most_common=100 freq_ge=50 --------------
    [('RAT', 1276),
     ('TCMA', 817),
     ('787', 781),
     ('FADEC', 369),
     ('B787', 220),
     ('ADSB', 170),
     ('EAFR', 170),
     ('APU', 167),
     ('AC', 152),
     ('TO', 143),
     ('FDR', 138),
     ...
     ('767', 50)]
    ------------ print_all_caps(): most_common=100 freq_ge=50 DONE ------------
    ----------- print_all_caps(): most_common=100 freq_ge=50 sorted -----------
    [('10', 121),
     ...
     ('AAIB', 102),
     ('AC', 152),
     ('AD', 51),
     ('ADSB', 170),
     ('AGL', 100),
     ('AI', 135),
     ('AI171', 68),
     ('APU', 167),
     ...
     ('VNAV', 93)]
    --------- print_all_caps(): most_common=100 freq_ge=50 sorted DONE --------

Words that are not all Capitals
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similarly use the ``--non-cap-words`` to list words that are not all capitals.

Phrases
^^^^^^^^^^

Phrases of any length can be extracted.
Here the most common 200 words are eliminated and then three word phrases are extracted.
``--freq_eq=9`` is used to eliminate phrases that occur fewer than 9 times.

.. code-block:: shell

    $ python src/pprune/research.py --most-common=200 --freq-ge=9 --phrases=3 threads/AI171_B/AI171-1 threads/AI171_B/AI171-2
    2025-06-24 11:17:51,103 -             read_html.py#288  - INFO     - Read: 666472-plane-crash-near-ahmedabad.html posts: 20
    2025-06-24 11:17:51,192 -             read_html.py#288  - INFO     - Read: 666472-plane-crash-near-ahmedabad-2.html posts: 20
    2025-06-24 11:17:51,278 -             read_html.py#288  - INFO     - Read: 666472-plane-crash-near-ahmedabad-3.html posts: 20    ...
    ...
    2025-06-24 11:18:07,124 -             read_html.py#290  - INFO     - update_whole_thread(): Read 2832 posts in 6.112 (s)
    Number of posts: 2832
    Number of words: 427262
    Number of common words: 1000
    ------------- print_phrases(): len=3 most_common=200 freq_ge=0 ------------
    ('dual', 'engine', 'failure')                    :  115
    ('double', 'engine', 'failure')                  :   57
    ('engine', 'driven', 'fuel')                     :   33
    ...
    ('assertions', 'contrary', 'seen')               :    9
    ---------- print_phrases(): len=3 most_common=200 freq_ge=0 DONE ----------
    --------- print_phrases(): len=3 most_common=200 freq_ge=0 sorted ---------
    ('1', 'Invalid', 'derate')                       :   11
    ...
    ('Discounting', 'impossible', 'hypotheses')      :   11
    ('Double', 'engine', 'failure')                  :    9
    ('ECL', 'physically', 'impossible')              :    9
    ('FCU', 'Immediate', 'ALT')                      :   13
    ('Flaps', 'instead', 'gear')                     :   10
    ...
    ('Plane', 'crash', 'Ahmedabad')                  :    9
    ('RAT', 'Almost', 'impossible')                  :   10
    ('RAT', 'deploment', 'happily')                  :   10
    ('RAT', 'hear', 'RAT')                           :   10
    ('RAT', 'noise', 'listening')                    :   10
    ...
    ('TCMA', 'TCMA', 'shutdown')                     :   10
    ('TCMA', 'activation', 'logic')                  :   10
    ('TCMA', 'airground', 'logic')                   :   16
    ('TCMA', 'ground', 'unfamiliar')                 :   10
    ('TCMA', 'require', 'failures')                  :   10
    ('TCMA', 'shutdown', 'engine')                   :   11
    ...
    ('driven', 'fuel', 'pump')                       :   20
    ('driven', 'fuel', 'pumps')                      :   21
    ('dual', 'engine', 'failure')                    :  115
    ('dual', 'engine', 'shutdown')                   :   32
    ...
    ('witnesses', 'RAT', 'hear')                     :   10
    ------- print_phrases(): len=3 most_common=200 freq_ge=0 sorted DONE ------
    2025-06-24 11:18:09,446 -              research.py#222  - INFO     - Read 2832 posts in 18.467 (s)

Configuring the Build
--------------------------

In ``src/pprune/publication_maps.py`` create a new concrete class inheriting from the virtual class ``PublicationMap``:

.. code-block:: python

    class AirIndia171(PublicationMap):
        def get_title(self) -> str:
            return 'AI171 Re-mixed'

        def get_introduction_in_html(self) -> str:
            return """There are these threads on pprune about the accident to
    ...
    """

Then create a series of tables (as dictionaries) that map the word/phrase to the chose subject.
For example:

.. code-block:: python

    LC_WORDS_MAP = {
        'mayday': 'Mayday',
        'biocide': 'Biocide',
        # ...
        'tilt': 'MLG Tilt',
    }

And for the phrases:

.. code-block:: python

    PHRASES_MAP = {
        2: {
            ('engine', 'failure'): 'Engine Failure (All)',
            ('RAT', 'deploy'): 'RAT (Deployment)',
            ('RAT', 'deployed'): 'RAT (Deployment)',
            ('RAT', 'deployment'): 'RAT (Deployment)',
            ('RAT', 'extended'): 'RAT (Deployment)',
            # ...
            ('thread', 'closed'): 'Thread Closure',
        },
        3: {
            ('dual', 'engine', 'failure'): 'Dual Engine Failure',
            ('double', 'engine', 'failure'): 'Dual Engine Failure',
            ('flaps', 'instead', 'gear'): 'Flaps vs Gear',
            # ...
            ('hydraulic', 'failure', 'double'): 'Hydraulic Failure (Double)',
        },
        4: {
            ('engine', 'driven', 'fuel', 'pump'): 'Fuel Pump (Engine  Driven)',
            ('engine', 'driven', 'fuel', 'pumps'): 'Fuel Pump (Engine  Driven)',
            # ...
            ('fuel', 'cut', 'off', 'switches'): 'Fuel Cut Off Switches',
        },
    }

Add the ``DUPLICATE_SUBJECT_MAP``.
This means that any post that appears in the subject given by the key also appears in all the
subjects in the value:

.. code-block:: python

    # Map of {subject_title : set(subject_title), ..}
    DUPLICATE_SUBJECT_MAP = {
        'RAT (Deployment)': {'RAT (All)', },
        'RAT (Electrical)': {'RAT (All)', },
        'RAT (Sound)': {'RAT (All)', },
        # ...
        'TCMA (Improper Activation)': {'TCMA (All)', },
        'TCMA (Air-ground Logic)': {'TCMA (All)', },
        'TCMA (Logic)': {'TCMA (All)', },
        'TCMA (Shutdown)': {'TCMA (All)', },
        # ...
    }

Add any specific posts and significant posts, the latter will be drawn to the attention
of the reader as important.

.. code-block:: python

    # The key is the pprune message number where the post is clearly about the subject
    # but the text does not refer to it.
    # This is a map of {permalink : subject, ...}
    SPECIFIC_POSTS_MAP = {}
    # The is the set of permalinks of significant posts that might be gathered
    # together in the subject 'Significant Posts'.
    # This is a map of {permalink : subject, ...}
    SIGNIFICANT_POSTS = {}


In ``src/pprune/publication_maps.py`` implement all the abstract methods.

Running the Build
--------------------------

In ``src/pprune/main.py`` add the reference to the ``AirIndia171`` class:

.. code-block:: python

    if args.thread_name == 'Concorde':
        # ...
    elif args.thread_name == 'AI171':
        pub_map = publication_maps.AirIndia171()
        words_required = pub_map.get_set_of_words_required()
        common_words -= words_required
        logger.info('Common words now length {:d}'.format(len(common_words)))
        write_html.write_whole_thread(thread, common_words, pub_map, args.output)

And run the build:

.. code-block:: shell

    $ python src/pprune/main.py --thread-name=AI171 threads/AI171/AI171-1 threads/AI171/AI171-2 docs/gh-pages/AI171
    2025-06-24 11:50:40,513 -             read_html.py#288  - INFO     - Read: 666472-plane-crash-near-ahmedabad.html posts: 20
    2025-06-24 11:50:40,612 -             read_html.py#288  - INFO     - Read: 666472-plane-crash-near-ahmedabad-2.html posts: 20
    2025-06-24 11:50:40,704 -             read_html.py#288  - INFO     - Read: 666472-plane-crash-near-ahmedabad-3.html posts: 20
    ...
    2025-06-24 11:50:59,295 -             read_html.py#288  - INFO     - Read: 666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-55.html posts: 20
    2025-06-24 11:50:59,373 -             read_html.py#288  - INFO     - Read: 666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-56.html posts: 11
    2025-06-24 11:50:59,373 -             read_html.py#290  - INFO     - update_whole_thread(): Read 2832 posts in 7.476 (s)
    2025-06-24 11:50:59,686 -                  main.py#111  - INFO     - Number of posts: 2832 Number of words: 427262
    2025-06-24 11:50:59,737 -                  main.py#113  - INFO     - Read: 1000 common words from "the" to "entry".
    2025-06-24 11:50:59,737 -                  main.py#129  - INFO     - Common words now length 982
    2025-06-24 11:50:59,738 -            write_html.py#369  - INFO     - Starting write_whole_thread() to tmp/AI171_out_D
    2025-06-24 11:50:59,738 -            write_html.py#91   - INFO     - Starting pass one...
    2025-06-24 11:51:01,833 -            write_html.py#122  - INFO     - Pass one complete in 2.096 (s)
    2025-06-24 11:51:01,833 -            write_html.py#375  - INFO     - Writing: index.html
    2025-06-24 11:51:01,843 -            write_html.py#378  - INFO     - Writing: "AAIB (All)" [69]
    2025-06-24 11:51:01,880 -            write_html.py#378  - INFO     - Writing: "AAIB (IDGA)" [29]
    2025-06-24 11:51:01,897 -            write_html.py#378  - INFO     - Writing: "AAIB (UK)" [11]
    2025-06-24 11:51:01,902 -            write_html.py#378  - INFO     - Writing: "ADSB" [105]
    ...
    2025-06-24 11:51:05,440 -            write_html.py#378  - INFO     - Writing: "Weight on Wheels" [39]
    2025-06-24 11:51:05,464 -            write_html.py#378  - INFO     - Writing: "Wrong Engine" [34]
    2025-06-24 11:51:05,485 -            write_html.py#381  - INFO     - Writing thread done in 5.747 (s)
    2025-06-24 11:51:05,486 -                  main.py#135  - INFO     - Processed 2832 posts in 25.110 (s)
    Bye, bye!
