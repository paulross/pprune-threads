# MIT License
#
# Copyright (c) 2017 Paul Ross https://github.com/paulross
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""The setup script.
copyright 2017-2025, Paul Ross
"""
import pathlib

from setuptools import setup, find_packages

COPYRIGHT = '2017-2025, Paul Ross'

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (
        (here / 'README.rst').read_text(encoding='utf-8')
        + '\n\n'
        + (here / 'INSTALL.rst').read_text(encoding='utf-8')
        + '\n\n'
        + (here / 'HISTORY.rst').read_text(encoding='utf-8')
)

install_requirements = [
    'beautifulsoup4',
    'coverage',
    'dateparser',
    'lxml',
    'numpy',
    'pytest',
    'pytest-cov',
    'requests',
    'setuptools',
    'urllib3',
    'Sphinx',
]

setup_requirements = [
    'setuptools>=18.0',
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='pprune-threads',
    version='0.1.0rc0',
    description="Analysis of pprune threads.",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author="Paul Ross",
    author_email='apaulross@gmail.com',
    url='https://github.com/paulross/pprune-threads',
    package_dir={'': 'src'},  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=['my_module'],
    #
    packages=find_packages(where='pprune'),  # Required
    entry_points={
        'console_scripts': {
            'archive_thread=pprune.common.read_html:main',
        },
    },
    include_package_data=True,
    license="MIT",
    # copyright=COPYRIGHT,
    zip_safe=False,
    keywords='pprune',
    # https://pypi.org/project/trove-classifiers/
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        # Deprecated, see pyproject.toml
        # 'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    # test_suite='tests',
    setup_requires=setup_requirements,
    install_requires=install_requirements,
    # tests_require=test_requirements,
    # cmdclass = {'build_ext': build_ext},
    # ext_modules=ext_modules
)
