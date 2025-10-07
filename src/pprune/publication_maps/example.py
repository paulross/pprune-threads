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
from pprune.publication_maps import publication_map_abc


class Example(publication_map_abc.PublicationMapABC):
    def get_title(self) -> str:
        return ''

    def get_introduction_in_html(self) -> str:
        return """"""

    def get_lowercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        return {}

    def get_uppercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        return {}

    def get_phrase_lengths(self) -> typing.List[int]:
        return []

    def get_phrases_to_subject_map(self, phrase_length: int) -> typing.Dict[str, str]:
        return {}

    def get_specific_posts_to_subject_map(self) -> typing.Dict[int, str]:
        return {}

    def get_duplicate_subjects(self, subject: str) -> typing.Set[str]:
        return set()

    def get_significant_posts_permalinks(self) -> typing.Tuple[typing.Tuple[str, int]]:
        return tuple()

    def get_set_of_words_required(self) -> typing.Set[str]:
        return set()

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
        return {}
