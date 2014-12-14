#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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

# Let's reject python >= 3 and use unicode.

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

def validateMathAndEtc(InputString):
    '''Replaces `pi` & `e` by proper numbers.'''

    i = InputString.find("e")

    while (i >= 0) and (i < len(InputString)):
        if not doesItContainFunction(InputString[(i - 5):(i + 6)]): # FIXME e*exp() → ?
            InputString = InputString[:i] + str(math.e) + InputString[(i + 1):] # FIXME 0e1 → 0*e*1

        i = InputString.find("e", (i + 1))

    InputString = InputString.replace("pi", str(math.pi)) # FIXME 0pi1 → 0*pi*1

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
    MathFunctionsStringsList = ("abs", "acos", "acosh", "asin", "asinh", "atan", "atanh",
                                "ceil", "cos", "cosh",
                                "degrees",
                                "erf", "erfc", "exp", "expm1",
                                "gamma",
                                "lgamma", "log", "log1p", "log10",
                                "fabs", "factorial", "floor",
                                "radians",
                                "sin", "sinh", "sqrt",
                                "tan", "tanh", "trunc")

    i = 0
    while (not OutputBoolean) and (i < len(MathFunctionsStringsList)):
        if doesItContainString(InputString, MathFunctionsStringsList[i], MustEndWith):
            OutputBoolean = True
        else:
            i += 1

    return(OutputBoolean)

#===============================================================#"

def calculateArithmetic(InputString):
    '''Calculates input simple arithmetical string expression to output string value.'''

    OperatorsList = ("**", "*", "//", "/", "%", "+", "-", "<<", ">>", "&", "|", "^")

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
    InputString = validateMathAndEtc(InputString)
    InputString = validateParenthesis(InputString)

    while "(" in InputString:
        ClosingIndex = InputString.find(")")
        OpeningIndex = ClosingIndex - InputString[ClosingIndex::-1].find("(")
        TempString = calculateArithmetic(InputString[(OpeningIndex + 1):ClosingIndex])

        if doesItContainFunction(InputString[:OpeningIndex], MustEndWith = True):

            if InputString[(OpeningIndex - 3):OpeningIndex] == "abs":
                TempString = str(abs(float(TempString)))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "acos":
                TempString = str(math.acos(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "acosh":
                TempString = str(math.acosh(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "asin":
                TempString = str(math.asin(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "asinh":
                TempString = str(math.asinh(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "atan":
                TempString = str(math.atan(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "atanh":
                TempString = str(math.atanh(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "ceil":
                TempString = str(math.ceil(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "cos":
                TempString = str(math.cos(float(TempString)))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "cosh":
                TempString = str(math.cosh(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 7):OpeningIndex] == "degrees":
                TempString = str(math.degrees(float(TempString)))
                OpeningIndex -= 7
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "erf":
                TempString = str(math.erf(float(TempString)))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "erfc":
                TempString = str(math.erfc(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "exp":
                TempString = str(math.exp(float(TempString)))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "expm1":
                TempString = str(math.expm1(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "gamma":
                TempString = str(math.gamma(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 6):OpeningIndex] == "lgamma":
                TempString = str(math.lgamma(float(TempString)))
                OpeningIndex -= 6
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "log":
                TempString = str(math.log(float(TempString)))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "log1p":
                TempString = str(math.log1p(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "log10":
                TempString = str(math.log10(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "fabs":
                TempString = str(math.fabs(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 9):OpeningIndex] == "factorial":
                TempString = str(math.factorial(float(TempString)))
                OpeningIndex -= 9
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "floor":
                TempString = str(math.floor(float(TempString)))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 7):OpeningIndex] == "radians":
                TempString = str(math.radians(float(TempString)))
                OpeningIndex -= 7
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "sin":
                TempString = str(math.sin(float(TempString)))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "sinh":
                TempString = str(math.sinh(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "sqrt":
                TempString = str(math.sqrt(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "tan":
                TempString = str(math.tan(float(TempString)))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "tanh":
                TempString = str(math.tanh(float(TempString)))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "trunc":
                TempString = str(math.trunc(float(TempString)))
                OpeningIndex -= 5

        else:
            StartIndex = OpeningIndex

        InputString = InputString.replace(InputString[OpeningIndex:(ClosingIndex + 1)], TempString)

    return(InputString)

#===============================================================#"

if __name__ == '__main__':
    print(calculateIt(raw_input("Please type a string to calculate: ")))
    "1*4+3.3/(3 + .3)*3(sqrt(4))/(sin(0) + 1)3" # TODO
    "10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5" # FIXME ValueError
