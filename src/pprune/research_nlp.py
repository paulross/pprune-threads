import argparse
import collections
import logging
import sys
import time
import typing

import spacy
from pprune.common import log_config
from pprune.common import read_html
from pprune.common import thread_struct

logger = logging.getLogger(__file__)


def print_set_str(the_set: typing.Set[str], width: int):
    """Print a set of strings as a table given a screen width."""
    max_len = max([len(v) + 1 for v in the_set])
    columns = max(1, width // max_len)
    logger.info('Max length of values: %d Columns: %d', max_len, columns)
    for i, value in enumerate(sorted(the_set)):
        if i and i % columns == 0:
            print()
        print(f'{value:{max_len}s} ', end='')
    print()


def process_thread(thread: thread_struct.Thread, collect_nouns: bool, collect_verbs: bool, min_frequency: int):
    logger.info('process_thread(): %s', thread)
    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")
    # {label : value : [post_ordinals, ...], ...}, ...}
    entity_lable_map: typing.Dict[str, typing.Dict[str, typing.List[int]]] = {}
    nouns = collections.Counter()
    verbs = collections.Counter()
    for p, post in enumerate(thread.posts):
        logger.debug('Post %d/%d', p, len(thread))
        doc = nlp(post.text_stripped_without_quoted_message)
        # Analyze syntax
        if collect_nouns:
            # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
            # From: https://spacy.io
            nouns.update([chunk.text for chunk in doc.noun_chunks])
        if collect_verbs:
            verbs.update([token.lemma_ for token in doc if token.pos_ == "VERB"])
        # Find named entities, phrases and concepts
        for entity in doc.ents:
            # print(entity.text, entity.label_)
            if entity.label_ not in entity_lable_map:
                entity_lable_map[entity.label_] = collections.defaultdict(list)
            entity_lable_map[entity.label_][entity.text].append(p)

    if collect_nouns:
        print(f' Nouns '.center(75, '='))
        # pprint.pprint(nouns, width=100)
        # print_set_str(nouns, width=180)
        # print(nouns)
        # for noun in nouns:
        #     if nouns[noun] > min_frequency:
        #         print(f'[{nouns[noun]:8}] {noun}')
        for noun, count in nouns.most_common():
            if count < min_frequency:
                break
            print(f'[{count:8}] {noun}')
        print(f' Nouns DONE '.center(75, '='))
    if collect_verbs:
        print(f' Verbs '.center(75, '='))
        # pprint.pprint(verbs, width=100)
        # print_set_str(verbs, width=180)
        # print(verbs)
        # for verb in verbs:
        #     if verbs[verb] > min_frequency:
        #         print(f'[{verbs[verb]:8}] {verb}')
        for verb, count in verbs.most_common():
            if count < min_frequency:
                break
            print(f'[{count:8}] {verb}')
        print(f' Verbs DONE '.center(75, '='))

    # Prune entity_lable_map
    for entity in entity_lable_map:
        to_del = []
        for key in entity_lable_map[entity]:
            if len(entity_lable_map[entity][key]) < min_frequency:
                to_del.append(key)
        for key in to_del:
            del entity_lable_map[entity][key]

    max_count = 0
    for entity in entity_lable_map:
        for subject in entity_lable_map[entity]:
            max_count = max(max_count, len(entity_lable_map[entity][subject]))

    factor = max([1, max_count // 80])
    logger.info('max_count %d factor %d', max_count, factor)
    print(f' Entity Label Map '.center(75, '='))
    for entity in sorted(entity_lable_map.keys()):
        if len(entity_lable_map[entity].keys()):
            print(f' {entity} '.center(75, '-'))
            print(
                f'    {"Subject":32}'
                f' [{"Posts":6}]:'
                f' {"Histogram"}'
            )
            for subject in sorted(entity_lable_map[entity].keys()):
                print(
                    f'    {subject:32}'
                    f' [{len(entity_lable_map[entity][subject]):6d}]:'
                    f' {"*" * (len(entity_lable_map[entity][subject]) // factor)}'
                )
            print(f' {entity}...DONE '.center(75, '-'))
        else:
            print(f'{entity} Empty ')
    print(f' Entity Label Map DONE '.center(75, '='))


def main() -> int:  # pragma: no cover
    parser = argparse.ArgumentParser(description='Perform research on a pprune thread with NLP.')
    parser.add_argument(
        'archives',
        type=str,
        nargs='+',
        help=(
            'Archive directory of the thread.'
            ' Multiple threads will be added in order.'
        )
    )
    parser.add_argument(
        "--collect-nouns",
        action="store_true",
        help=(
            "Report the nouns in the text (verbose). [default: %(default)s]"
        )
    )
    parser.add_argument(
        "--collect-verbs",
        action="store_true",
        help=(
            "Report the verbs in the text (verbose). [default: %(default)s]"
        )
    )
    parser.add_argument(
        "--min-frequency",
        type=int,
        default=5,
        help="The minimum frequency to report. [default: %(default)d]",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="log_level",
        type=int,
        default=20,
        help="Log level. [default: %(default)d]",
    )
    args, unknown_args = parser.parse_known_args()
    print(f'Args:\n{args}')
    if unknown_args:
        print(f'Unknown args:\n{unknown_args}')
        parser.print_usage()
        return -1
    logging.basicConfig(
        level=args.log_level,
        format=log_config.DEFAULT_OPT_LOG_FORMAT_NO_PROCESS,
        stream=sys.stdout,
    )
    t_start = time.perf_counter()
    thread = thread_struct.Thread()
    for archive in args.archives:
        read_html.update_whole_thread(archive, thread)
    logger.info('Read %d posts in %.3f (s)', len(thread), time.perf_counter() - t_start)

    word_count = 0
    for post in thread.posts:
        word_count += len(post.words)
    logger.info('Number of words: {:d}'.format(word_count))

    process_thread(thread, args.collect_nouns, args.collect_verbs, args.min_frequency)

    t_elapsed = time.perf_counter() - t_start
    logger.info('Processed %d posts in %.3f (s)', len(thread), t_elapsed, )
    print('Bye, bye!')
    return 0


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
