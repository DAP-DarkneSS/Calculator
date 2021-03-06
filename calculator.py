#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# A Python2 calculator for EPAM linux cource.
# Copyright (C) 2014-2015 Dmitriy A. Perlow <dap.darkness@gmail.com>

# This file is part of Calculator.

# Calculator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Calculator.  If not, see
# <http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html>.

# You could contact me with e-mail or jabber dap.darkness@gmail.com

# Let's reject python >= 3 and use unicode.

import argparse
from Calculator.calc import Calculator


if __name__ == '__main__':

    ShellParser = argparse.ArgumentParser()
    ShellParser.add_argument("-f",
                             "--file",
                             default="input.txt",
                             help="input file name.")
    ShellParser.add_argument("-v",
                             "--verbose",
                             default=False,
                             action="store_true",
                             help="print also input string, not result only.")
    ShellArguments = ShellParser.parse_args()

    try:
        with open(ShellArguments.file) as InputFile:
            TempList = InputFile.read().splitlines()
    except:
        TempList = []
        TempList.append(raw_input("Please type a string to calculate (press Enter to calculate buildin tuple): "))
        if TempList[0] == "":
            del(TempList[0])
    if TempList == []:
        TempList = ("1*4+3.3/(3 + .3)*3(sqrt(4))/(sin(0) + 1)3",
                    "10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5")
    for i in TempList:
        try:
            TempObject = Calculator(i)
            TempObject.calculateIt()
            if ShellArguments.verbose:
                TempObject.InputString = TempObject + " = " + TempObject.InputString
            print(TempObject.InputString)
        except Exception as ExceptionMessage:
            print(ExceptionMessage)
