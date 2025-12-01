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

__author__ = 'Paul Ross'
__date__ = '2017-01-01'
__version__ = '0.0.1'
__rights__ = 'Copyright (c) 2017 Paul Ross'

import abc
import typing


class PublicationMapABC(abc.ABC):

    def __init__(self):
        self._include_posts_with_no_subject = False

    @property
    def include_posts_with_no_subject(self) -> bool:
        """Flag to include pages with posts that have no identifiable subject."""
        return self._include_posts_with_no_subject

    @include_posts_with_no_subject.setter
    def include_posts_with_no_subject(self, value: bool) -> None:
        self._include_posts_with_no_subject = value

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
        """Returns a map of {lower_case_word : subject_title, ...}"""
        pass

    @abc.abstractmethod
    def get_uppercase_word_to_subject_map(self) -> typing.Dict[str, str]:
        """Returns a map of {upper_case_word : subject_title, ...}"""
        pass

    @abc.abstractmethod
    def get_phrase_lengths(self) -> typing.List[int]:
        """Returns the phrase lengths supported."""
        pass

    @abc.abstractmethod
    def get_phrases_to_subject_map(self, phrase_length: int) -> typing.Dict[str, str]:
        """Returns a map of {phrase : subject_title, ...}"""
        pass

    @abc.abstractmethod
    def get_specific_posts_to_subject_map(self) -> typing.Dict[int, str]:
        """Returns a map of {permalink : subject_title, ...}"""
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
    def get_significant_posts_permalinks(self) -> typing.Tuple[typing.Tuple[str, int], ...]:
        """This is the set of permalinks of significant posts that might be gathered
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

    @abc.abstractmethod
    def include_empty_post_dates_in_histogram(self) -> bool:
        """Returns True if we want all dates in the date histogram even if there are no posts."""
        pass
