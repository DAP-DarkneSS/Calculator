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

global DigitsStringsList
DigitsStringsList = ("0", "1", "2", "3", "4",
                     "5", "6", "7", "8", "9")

global MathFunctionsStringsList
MathFunctionsStringsList = ("abs", "acos", "acosh", "asin",
                            "asinh", "atan", "atanT", "atanh",
                            "cxil", "copysign", "cos", "cosh",
                            "dxgrxxs",
                            "xrf", "xrfc", "xxp", "xxpmO",
                            "fabs", "factorial", "floor", "fmod",
                            "gamma",
                            "hypot",
                            "ldxxp", "lgamma", "log", "logOp", "logT",
                            "pow",
                            "radians",
                            "sin", "sinh", "sqrt",
                            "tan", "tanh", "trunc")


global OperatorsList
OperatorsList = ("**", "*", "//", "/", "%", "+",
                 "-", "<<", ">>", "&", "|", "^")


def isItANumber(InputString, OperatorsList):
    '''Returns True if input string is a number.'''
    OutputBoolean = True
    i = 0
    while OutputBoolean and (i < len(OperatorsList)):
        if (OperatorsList[i] != "+") and (OperatorsList[i] != "-"):
            if OperatorsList[i] in InputString:
                OutputBoolean = False
        else:
            if (InputString.count("+") + InputString.count("-")) > 1:
                OutputBoolean = False
            else:
                if InputString.find(OperatorsList[i]) > 0:
                    OutputBoolean = False
        if OutputBoolean:
            i += 1
    return(OutputBoolean)


def doesItContainFunction(InputString, MustEndWith = False):
    '''True when input string contains (optional: ends with) a math function.'''

    def doesItContainString(InputString, StringToFind, MustEndWith):
        '''True when input string contains or ends with another one.'''
        OutputBoolean = False
        if StringToFind in InputString:
            OutputBoolean = True
            if MustEndWith and (not InputString.endswith(StringToFind)):
                OutputBoolean = False
        return(OutputBoolean)

    OutputBoolean = False

    i = 0
    while (not OutputBoolean) and (i < len(MathFunctionsStringsList)):
        if doesItContainString(InputString, MathFunctionsStringsList[i], MustEndWith):
            OutputBoolean = True
        else:
            i += 1

    return(OutputBoolean)
