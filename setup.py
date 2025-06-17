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
import os
import sysconfig

from setuptools import setup, find_packages

COPYRIGHT = '2017-2025, Paul Ross'


# with open('README.rst') as readme_file:
#     readme = readme_file.read()
#
# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

install_requirements = [
    'beautifulsoup4',
    'colorama',
    'lxml',
    'psutil',
    'requests',
]

setup_requirements = [
    'setuptools>=18.0',
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='pprune-thread',
    version='0.1.0rc0',
    description="Analysis of pprune threads.",
    long_description="Analysis of pprune threads.",
    author="Paul Ross",
    author_email='apaulross@gmail.com',
    url='https://github.com/paulross/pprune-threads',
    packages=find_packages('src'),
    # package_dir={'' : 'src'},
    # package_data={'' : ['TotalDepth/util/plot/formats/*.xml']},
    # data_files=data_files,
    entry_points={
        'console_scripts': {
            'pprune_archive_thread=pprune.common.read_html:main',
        },
    },
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords='pprune',
    # https://pypi.org/project/trove-classifiers/
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
    test_suite='tests',
    setup_requires=setup_requirements,
    install_requires=install_requirements,
    tests_require=test_requirements,
    # cmdclass = {'build_ext': build_ext},
    # ext_modules=ext_modules
)
