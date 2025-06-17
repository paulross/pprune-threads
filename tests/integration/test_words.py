import pytest

from pprune.common import words


@pytest.mark.parametrize(
    'limit, expected',
    (
            (0, 333333),
            (100, 100),
    )
)
def test_words_size(limit, expected):
    result = words.read_common_words_file(limit)
    assert len(result) == expected


@pytest.mark.parametrize(
    'index, expected',
    (
            (0, 'the'),
            (1, 'of'),
            (2, 'and'),
    )
)
def test_words_100_content(index, expected):
    result = words.read_common_words_file(limit=100)
    assert result[index] == expected
