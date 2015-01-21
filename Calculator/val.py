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

import math
from stuff import *


class Validator(str):
    '''A general input validation class.'''

    def __init__(self, InputString):
        self.InputString = InputString

    def validateSpaces(self):
        '''Just now it simply deletes them.'''

        self.InputString = self.InputString.replace(" ", "")


    def validateDecimalPoint(self):
        '''Puts zeros in front of decimal points if required.'''

        if ".." in self.InputString:
            raise ValueError("Double decimal point.")

        if self.InputString[0] == ".":
            self.InputString = "0" + self.InputString
            i = self.InputString.find(".", 2)
        else:
            i = self.InputString.find(".", 1)

        while (i >= 0) and (i < (len(self.InputString) - 1)):
            if self.InputString[(i + 1)] not in DigitsStringsList:
                self.InputString = self.InputString[:(i + 1)] + "0" + self.InputString[(i + 1):]

            if self.InputString[(i - 1)] not in DigitsStringsList:
                self.InputString = self.InputString[:i] + "0" + self.InputString[i:]
                i = self.InputString.find(".", (i + 2))
            else:
                i = self.InputString.find(".", (i + 1))

        if self.InputString[(len(self.InputString) - 1)] == ".":
            self.InputString += "0"


    def validateMathFunctions(self):
        '''Renames some problematical math functions.'''

        self.InputString = self.InputString.replace("atan2", "atanT")
        self.InputString = self.InputString.replace("ceil", "cxil")
        self.InputString = self.InputString.replace("degrees", "dxgrxxs")
        self.InputString = self.InputString.replace("erf", "xrf")
        self.InputString = self.InputString.replace("erfc", "xrfc")
        self.InputString = self.InputString.replace("exp", "xxp")
        self.InputString = self.InputString.replace("expm1", "xxpmO")
        self.InputString = self.InputString.replace("ldexp", "ldxxp")
        self.InputString = self.InputString.replace("log1p", "logOp")
        self.InputString = self.InputString.replace("log10", "logT")


    def validateMathConstants(self):
        '''Replaces `pi` & `e` by proper numbers.'''

        self.InputString = self.InputString.replace("e", str(math.e))
        self.InputString = self.InputString.replace("pi", str(math.pi))


    def validateMultiplication(self):
        '''Puts multiplication signs around parenthesis and math objects if required.'''

        if self.InputString.count("(") != self.InputString.count(")"):
            raise ValueError("'(' and ')' counts differ.")

        i = 1
        while i < (len(self.InputString) - 2):
            if (self.InputString[(i - 1)] in DigitsStringsList) and (self.InputString[i] == "(") and (not doesItContainFunction(self.InputString[(i + 1):], MustEndWith = True)):
                self.InputString = self.InputString[:i] + "*" + self.InputString[i:]
                i += 2
            else:
                i += 1

        i = 2
        while i < (len(self.InputString) - 1):
            if (self.InputString[(i + 1)] in DigitsStringsList) and (self.InputString[i] == ")"):
                self.InputString = self.InputString[:(i + 1)] + "*" + self.InputString[(i + 1):]
                i += 2
            else:
                i += 1

        for i in (MathFunctionsStringsList + ("e", "pi")):
            j = self.InputString.find(i, 1)
            while (j > 0) and (j < len(self.InputString)):
                if (self.InputString[j - 1] == ")") or (self.InputString[j - 1] in DigitsStringsList):
                    self.InputString = self.InputString[:j] + "*" + self.InputString[j:]
                j = self.InputString.find(i, (j + 1))

# Hello, the first kludge!
        self.InputString = "(" + self.InputString + ")"


    def validatePlusMinus(self):
        '''Cancels multiple signs out if required.'''

        while ("++" in self.InputString) or ("+-" in self.InputString) or ("-+" in self.InputString) or ("--" in self.InputString):
            self.InputString = self.InputString.replace("++", "+")
            self.InputString = self.InputString.replace("+-", "-")
            self.InputString = self.InputString.replace("-+", "-")
            self.InputString = self.InputString.replace("--", "+")
