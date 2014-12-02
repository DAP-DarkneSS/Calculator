#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Let's reject python >= 3 and use unicode.

#===============================================================#"

# A Python2 calculator for EPAM linux cource.
# Copyright (C) 2014 Dmitriy A. Perlow <dap.darkness@gmail.com>

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

#===============================================================#"

global DigitsStringsList
DigitsStringsList = []
for i in xrange(10):
    DigitsStringsList.append(str(i))

#===============================================================#"

def validateDecimalPoint(InputString):
    '''Puts zeros in front of decimal points if required.'''

    if ".." in InputString:
        raise ValueError("Double decimal point.")

    if InputString[0] == ".":
        InputString = "0" + InputString
        i = InputString.find(".", 2)
    else:
        i = InputString.find(".", 1)

    while (i >= 0) and (i < (len(InputString) - 1)):
        if InputString[(i + 1)] not in DigitsStringsList:
            InputString = InputString[:(i + 1)] + "0" + InputString[(i + 1):]

        if InputString[(i - 1)] not in DigitsStringsList:
            InputString = InputString[:i] + "0" + InputString[i:]
            i = InputString.find(".", (i + 2))
        else:
            i = InputString.find(".", (i + 1))

    if InputString[(len(InputString) - 1)] == ".":
        InputString += "0"

    return(InputString)

#===============================================================#"

def validateParenthesis(InputString):
    '''Puts multiplication signs around parenthesis if required.'''
    
    if InputString.count("(") != InputString.count(")"):
        raise ValueError("'(' and ')' counts differ.")

    i = 1
    while i < (len(InputString) - 2):
        if (InputString[(i - 1)] in DigitsStringsList) and (InputString[i] == "("):
            InputString = InputString[:i] + "*" + InputString[i:]
            i += 2
        else:
            i += 1

    i = 2
    while i < (len(InputString) - 1):
        if (InputString[(i + 1)] in DigitsStringsList) and (InputString[i] == ")"):
            InputString = InputString[:(i + 1)] + "*" + InputString[(i + 1):]
            i += 2
        else:
            i += 1

# Hello, the first kludge!
    InputString = "(" + InputString + ")"
    return(InputString)

#===============================================================#"

def validateSigns(InputString):
    '''Cancels multiple signs out or raises ValueError if required.'''

    for i in ("***", "*/", "/*", "///", "+*", "+/", "-*", "-/"):
        if i in InputString:
            raise ValueError("Too many signs. Fix validateSigns() if wrong.")

    while ("++" in InputString) or ("+-" in InputString) or ("-+" in InputString) or ("--" in InputString):
        InputString = InputString.replace("++", "+")
        InputString = InputString.replace("+-", "-")
        InputString = InputString.replace("-+", "-")
        InputString = InputString.replace("--", "+")

    return(InputString)

#===============================================================#"

def calculateIt(InputString):
    '''Calculates input string expression to output string value.'''

    OperatorsList = ("**", "*", "/", "%", "//", "+", "-")

    for j in OperatorsList:
        InputString = validateSigns(InputString)

        if ("*" in InputString) or ("/" in InputString) or ("%" in InputString) or ((InputString.count("+") + InputString.count("-")) > 1) or (InputString.find("+") > 0) or (InputString.find("-") > 0):
            while j in InputString:
                FirstNumberStartsAt = SecondNumberEndsAt = OperatorIndex = InputString.find(j)

                i = OperatorIndex + len(j)
                while SecondNumberEndsAt == OperatorIndex:
                    if (i == len(InputString)) or (InputString[i] in OperatorsList):
                        SecondNumberEndsAt = i
                    else:
                        i += 1

                i = OperatorIndex - 1
                while FirstNumberStartsAt == OperatorIndex:
                    if (i == -1) or (InputString[i] in OperatorsList):
                        FirstNumberStartsAt = i + 1
                    else:
                        i -= 1

                FirstNumber = float(InputString[FirstNumberStartsAt:OperatorIndex])
                SecondNumber = float (InputString[(OperatorIndex + len(j)):SecondNumberEndsAt])
                if j == "**":
                    CalculatedNumber = FirstNumber ** SecondNumber
                elif j == "*":
                    CalculatedNumber = FirstNumber * SecondNumber
                elif j == "/":
                    CalculatedNumber = FirstNumber / SecondNumber
                elif j == "//":
                    CalculatedNumber = FirstNumber // SecondNumber
                elif j == "%":
                    CalculatedNumber = FirstNumber % SecondNumber
                elif j == "+":
                    CalculatedNumber = FirstNumber + SecondNumber
                elif j == "-":
                    CalculatedNumber = FirstNumber - SecondNumber

                InputString = InputString.replace(InputString[FirstNumberStartsAt:SecondNumberEndsAt], str(CalculatedNumber))

    return(InputString)

#===============================================================#"

InputString = raw_input('Please type a string to calculate: ')
InputString = validateDecimalPoint(InputString)
InputString = validateParenthesis(InputString)

#===============================================================#"

while "(" in InputString:
    ClosingIndex = InputString.find(")")
    OpeningIndex = ClosingIndex - InputString[ClosingIndex::-1].find("(")
    InputString = InputString.replace(InputString[OpeningIndex:(ClosingIndex + 1)], calculateIt(InputString[(OpeningIndex + 1):ClosingIndex]))

print(InputString)
