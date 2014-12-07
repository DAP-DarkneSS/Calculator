#!/usr/bin/env python2

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

# -*- coding: utf-8 -*-
# Let's reject python >= 3 and use unicode.

#===============================================================#"

global DigitsStringsList
DigitsStringsList = []
for i in xrange(10):
    DigitsStringsList.append(str(i))
del(i)

import math

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
        if (InputString[(i - 1)] in DigitsStringsList) and (InputString[i] == "(") and (not doesItContainFunction(InputString[(i + 1):], MustEndWith = True)):
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
    '''Cancels multiple signs out if required.'''

    while ("++" in InputString) or ("+-" in InputString) or ("-+" in InputString) or ("--" in InputString):
        InputString = InputString.replace("++", "+")
        InputString = InputString.replace("+-", "-")
        InputString = InputString.replace("-+", "-")
        InputString = InputString.replace("--", "+")

    return(InputString)

#===============================================================#"

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
    MathFunctionsStringsList = dir(math)
    del MathFunctionsStringsList[:4]

    i = 0
    while (not OutputBoolean) and (i < len(OutputBoolean)):
        if doesItContainString(InputString, MathFunctionsStringsList[i], MustEndWith):
            OutputBoolean = True
        else:
            i += 1

    return(OutputBoolean)

#===============================================================#"

def calculateArithmetic(InputString):
    '''Calculates input simple arithmetical string expression to output string value.'''

    OperatorsList = ("**", "*", "/", "%", "//", "+", "-", "<<", ">>", "&", "|", "^")

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

    for j in OperatorsList:
        InputString = validateSigns(InputString)

        if not isItANumber(InputString, OperatorsList):
            while j in InputString and not ((InputString[0] == j) and (InputString.count(j) == 1)):
                FirstNumberStartsAt = SecondNumberEndsAt = OperatorIndex = (InputString[1:].find(j) + 1)

                i = OperatorIndex + len(j)
                while SecondNumberEndsAt == OperatorIndex:
                    if (i == len(InputString)) or (InputString[i] in OperatorsList):
                        SecondNumberEndsAt = i
                    else:
                        i += 1

                i = OperatorIndex - 1
                while FirstNumberStartsAt == OperatorIndex:
                    if i == -1:
                        FirstNumberStartsAt = i + 1
                    elif InputString[i] in OperatorsList:
                        if (i == 0) or (InputString[i-1] in OperatorsList):
                            FirstNumberStartsAt = i
                        else:
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
                elif j == "<<":
                    CalculatedNumber = FirstNumber << SecondNumber
                elif j == ">>":
                    CalculatedNumber = FirstNumber >> SecondNumber
                elif j == "&":
                    CalculatedNumber = FirstNumber & SecondNumber
                elif j == "|":
                    CalculatedNumber = FirstNumber | SecondNumber
                elif j == "^":
                    CalculatedNumber = FirstNumber ^ SecondNumber

                InputString = InputString.replace(InputString[FirstNumberStartsAt:SecondNumberEndsAt], str(CalculatedNumber))

    return(InputString)

#===============================================================#"

def calculateIt(InputString):
    '''Calculates any (the description is a lie) input string expression to output string value.'''

    InputString = InputString.replace(" ", "")
    InputString = validateDecimalPoint(InputString)
    InputString = validateParenthesis(InputString)

    while "(" in InputString:
        ClosingIndex = InputString.find(")")
        OpeningIndex = ClosingIndex - InputString[ClosingIndex::-1].find("(")
        InputString = InputString.replace(InputString[OpeningIndex:(ClosingIndex + 1)], calculateArithmetic(InputString[(OpeningIndex + 1):ClosingIndex]))

    return(InputString)

#===============================================================#"

if __name__ == '__main__':
    print(calculateIt(raw_input("Please type a string to calculate: ")))
