#!/usr/bin/env python3
# ultimateultimateguitar
# Copyright (C) 2024 Salvo "LtWorf" Tomaselli
#
# ultimateultimateguitar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

from setuptools import setup

setup(
    version='0.1',
    name='ultimateultimateguitar',
    description='CLI for ultimateguitar',
    packages=('ultimateultimateguitar',),
    keywords='TODO',
    author="Salvo 'LtWorf' Tomaselli",
    author_email='tiposchi@tiscali.it',
    maintainer="Salvo 'LtWorf' Tomaselli",
    maintainer_email='tiposchi@tiscali.it',
    url='https://codeberg.org/ltworf/ultimateultimateguitar',
    license='AGPL3',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
    ],
    entry_points={
        'console_scripts': [
            'ultimateultimateguitar = ultimateultimateguitar:main',
        ]
    },
    install_requires=[
        'typedload',
        'xtermcolor',
    ]
)
