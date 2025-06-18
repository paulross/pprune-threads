import pytest

from pprune.common import read_html


@pytest.mark.parametrize(
    'filename, expected',
    (
            (
                    '423988-concorde-question.html',
                    ('423988', '-concorde-question', None),
            ),
            (
                    '423988-concorde-question-2.html',
                    ('423988', '-concorde-question-', '2'),
            ),
            (
                    '666472-plane-crash-near-ahmedabad.html',
                    ('666472', '-plane-crash-near-ahmedabad', None),
            ),
            (
                    '666472-plane-crash-near-ahmedabad-2.html',
                    ('666472', '-plane-crash-near-ahmedabad-', '2'),
            ),
            (
                    '666472-plane-crash-near-ahmedabad-87.html',
                    ('666472', '-plane-crash-near-ahmedabad-', '87'),
            ),
            (
                    '666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a.html',
                    ('666581', '-air-india-ahmedabad-accident-12th-june-2025-part-2-a', None),
            ),
            (
                    '666581-air-india-ahmedabad-accident-12th-june-2025-part-2-a-20.html',
                    ('666581', '-air-india-ahmedabad-accident-12th-june-2025-part-2-a-', '20'),
            ),
    ),
)
def test_RE_FILENAME(filename, expected):
    m = read_html.RE_FILENAME.match(filename)
    assert m is not None
    assert m.groups() == expected
