import os
import typing

EXAMPLE_PAGES: typing.Dict[str, str] = {}

EXAMPLE_PAGES_DIRECTORY = os.path.join(os.path.dirname(__file__), 'example_pages', )

for filename in os.listdir(EXAMPLE_PAGES_DIRECTORY):
    with open(os.path.join(EXAMPLE_PAGES_DIRECTORY, filename), 'r') as f:
        EXAMPLE_PAGES[filename] = f.read()
