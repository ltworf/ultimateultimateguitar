#!/usr/bin/env python3
# ultimateultimateguitar

# Copyright (C) 2018 Salvo "LtWorf" Tomaselli
#
# ultimateultimateguitar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>


import argparse
import gzip
import hashlib
import json
import os
from typing import *
from urllib.request import urlopen

import typedload
import xtermcolor


VERSION = '1.1'


class Cache:
    def __init__(self) -> None:
        cachedir = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~') + '/.cache')
        if not os.path.exists(cachedir):
            raise FileNotFoundError('No cache directory present: %s' % cachedir)
        uugcache = cachedir + '/ultimateultimateguitar/'
        if not os.path.exists(uugcache):
            os.mkdir(uugcache)
        self._cachedir = uugcache

    @staticmethod
    def sha(key: str) -> str:
        return hashlib.sha256(key.encode('utf8')).hexdigest()

    def get(self, key: str) -> Optional[bytes]:
        fname = self._cachedir + str(self.sha(VERSION + key))
        if not os.path.exists(fname):
            return None
        with gzip.open(fname, 'rb') as f:
            return f.read()

    def set(self, key: str, content: bytes) -> None:
        fname = self._cachedir + str(self.sha(VERSION + key))
        with gzip.open(fname, 'wb') as f:
            f.write(content)


class Chord(str):
    @property
    def diesis(self) -> bool:
        """
        True if the chord has a ♯
        """
        try:
            return self[1] in {'#', '♯'}
        except IndexError:
            return False

    @property
    def bemolle(self) -> bool:
        """
        True if the chord has a ♭
        """
        try:
            return self[1] in {'b', '♭'}
        except IndexError:
            return False

    @property
    def details(self) -> str:
        """
        Returns whatever is left after the dominant of the chord

        eg: m, 7, and so on.
        """
        start = 1
        if self.diesis or self.bemolle:
            start += 1
        return self[start:]

    @property
    def dominant(self) -> int:
        TABLE = {
            'C': 0,
            'D': 2,
            'E': 4,
            'F': 5,
            'G': 7,
            'A': 9,
            'B': 11,
        }
        value = TABLE[self[0].upper()]
        if self.bemolle:
            value -= 1
        elif self.diesis:
            value += 1
        return value % 12

    def transpose(self, semitones: int) -> 'Chord':
        TABLE = [
            'C',
            'C♯',
            'D',
            'D♯',
            'E',
            'F',
            'F♯',
            'G',
            'G♯',
            'A',
            'B♭',
            'B',
        ]
        dominant = TABLE[(self.dominant + semitones) % 12]
        return Chord(dominant + self.details)


class WikiTab(NamedTuple):
    content: str

    def get_tokens(self, transpose: int = 0) -> Iterator[Union[str, Chord]]:
        for i in self.content.split('[ch]'):
            s = i.split('[/ch]', 1)
            if len(s) > 1:
                sep = ''
                for j in s[0].split('/'):
                    yield sep
                    yield Chord(j).transpose(transpose)
                    sep = '/'
                yield s[1]
            else:
                yield s[0]


    def print(self, transpose: int = 0) -> None:
        content = self.content
        for i in self.get_tokens(transpose):
            if isinstance(i, Chord):
                print(xtermcolor.colorize(i, 0x00FF00), end='')
            else:
                print(i, end='')
        print()


class TabView(NamedTuple):
    wiki_tab: WikiTab
    #TODO recommendations
    #TODO applicature


def get_data(url: str) -> Dict[str, Any]:
    """
    From a url of ultimate-guitar, this function returns
    the actual data, which is stored as json.
    """
    lineheader = b'window.UGAPP.store.page = '
    cache = Cache()

    content = cache.get(url)

    if not content:
        with urlopen(url) as f:
            for i in f:
                i = i.strip()
                if i.startswith(lineheader):
                    content = i[len(lineheader):-1]
                    cache.set(url, content)
                    return json.loads(content)
    else:
        return json.loads(content)
    raise ValueError('Unable to parse song data')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--transpose', '-t', help='Transposes the chords of n semitones',
                        type=int, default=0)

    parser.add_argument("url")
    args = parser.parse_args()

    # Get json data
    data = get_data(args.url)

    # Remove useless crap
    data = data['data']['tab_view']

    a = typedload.load(data, TabView)
    a.wiki_tab.print(args.transpose)


if __name__ == '__main__':
    main()
