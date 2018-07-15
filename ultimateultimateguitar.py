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
import json
from typing import *
from urllib.request import urlopen

import typedload
import xtermcolor


VERSION = '1.1'


class Chord(str):
    pass


class WikiTab(NamedTuple):
    content: str

    def get_tokens(self) -> Iterator[Union[str, Chord]]:
        for i in self.content.split('[ch]'):
            s = i.split('[/ch]', 1)
            if len(s) > 1:
                yield Chord(s[0])
                yield s[1]
            else:
                yield s[0]


    def print(self) -> None:
        content = self.content
        for i in self.get_tokens():
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
    with urlopen(url) as f:
        for i in f:
            i = i.strip()
            if i.startswith(lineheader):
                content = i[len(lineheader):-1]
                return json.loads(content)
    raise ValueError('Unable to parse song data')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=VERSION)

    parser.add_argument("url")
    args = parser.parse_args()

    # Get json data
    data = get_data(args.url)

    # Remove useless crap
    data = data['data']['tab_view']

    a = typedload.load(data, TabView)
    a.wiki_tab.print()




if __name__ == '__main__':
    main()
