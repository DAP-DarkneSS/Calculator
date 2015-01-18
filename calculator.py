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

global MathFunctionsStringsList
MathFunctionsStringsList = ("abs", "acos", "acosh", "asin", "asinh", "atan", "atanT", "atanh",
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

def validateMathFunctions(InputString):
    '''Renames some problematical math functions.'''

    InputString = InputString.replace("atan2", "atanT")
    InputString = InputString.replace("ceil", "cxil")
    InputString = InputString.replace("degrees", "dxgrxxs")
    InputString = InputString.replace("erf", "xrf")
    InputString = InputString.replace("erfc", "xrfc")
    InputString = InputString.replace("exp", "xxp")
    InputString = InputString.replace("expm1", "xxpmO")
    InputString = InputString.replace("ldexp", "ldxxp")
    InputString = InputString.replace("log1p", "logOp")
    InputString = InputString.replace("log10", "logT")

    return(InputString)

#===============================================================#"

def validateMathConstants(InputString):
    '''Replaces `pi` & `e` by proper numbers.'''

    InputString = InputString.replace("e", str(math.e))
    InputString = InputString.replace("pi", str(math.pi))

    return(InputString)

#===============================================================#"

def validateMultiplication(InputString):
    '''Puts multiplication signs around parenthesis and math objects if required.'''

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

    for i in (MathFunctionsStringsList + ("e", "pi")):
        j = InputString.find(i, 1)
        while (j > 0) and (j < len(InputString)):
            if (InputString[j - 1] == ")") or (InputString[j - 1] in DigitsStringsList):
                InputString = InputString[:j] + "*" + InputString[j:]
            j = InputString.find(i, (j + 1))

# Hello, the first kludge!
    InputString = "(" + InputString + ")"
    return(InputString)

#===============================================================#"

def validatePlusMinus(InputString):
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
        InputString = validatePlusMinus(InputString)

        if not isItANumber(InputString, OperatorsList):
            while j in InputString and not ((InputString[0] == j) and (InputString.count(j) == 1)):
                FirstNumberStartsAt = SecondNumberEndsAt = OperatorIndex = (InputString[1:].find(j) + 1)

                i = OperatorIndex + len(j) + 1
# +1 to pass unary +/- sign.
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
                SecondNumber = float(InputString[(OperatorIndex + len(j)):SecondNumberEndsAt])
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
                    CalculatedNumber = int(FirstNumber) << int(SecondNumber)
                elif j == ">>":
                    CalculatedNumber = int(FirstNumber) >> int(SecondNumber)
                elif j == "&":
                    CalculatedNumber = int(FirstNumber) & int(SecondNumber)
                elif j == "|":
                    CalculatedNumber = int(FirstNumber) | int(SecondNumber)
                elif j == "^":
                    CalculatedNumber = int(FirstNumber) ^ int(SecondNumber)

                InputString = InputString.replace(InputString[FirstNumberStartsAt:SecondNumberEndsAt], str(CalculatedNumber))

    return(InputString)

#===============================================================#"

def calculateIt(InputString):
    '''Calculates any (the description is a lie) input string expression to output string value.'''

    InputString = InputString.replace(" ", "")
    InputString = validateDecimalPoint(InputString)
    InputString = validateMathFunctions(InputString)
    InputString = validateMultiplication(InputString)
    InputString = validateMathConstants(InputString)

    while "(" in InputString:
        ClosingIndex = InputString.find(")")
        OpeningIndex = ClosingIndex - InputString[ClosingIndex::-1].find("(")
        TempList = InputString[(OpeningIndex + 1):ClosingIndex].split(",")
        TempListLen = len(TempList)
        for i in xrange(TempListLen):
            TempList[i] = calculateArithmetic(TempList[i])

        if doesItContainFunction(InputString[:OpeningIndex], MustEndWith = True):

            if InputString[(OpeningIndex - 3):OpeningIndex] == "abs":
                TempString = str(abs(float(TempList[0])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "acos":
                TempString = str(math.acos(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "acosh":
                TempString = str(math.acosh(float(TempList[0])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "asin":
                TempString = str(math.asin(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "asinh":
                TempString = str(math.asinh(float(TempList[0])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "atan":
                TempString = str(math.atan(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "atanT":
                TempString = str(math.atan2(float(TempList[0]), float(TempList[1])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "atanh":
                TempString = str(math.atanh(float(TempList[0])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "cxil":
                TempString = str(math.ceil(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 8):OpeningIndex] == "copysign":
                TempString = str(math.copysign(float(TempList[0]), float(TempList[1])))
                OpeningIndex -= 8
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "cos":
                TempString = str(math.cos(float(TempList[0])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "cosh":
                TempString = str(math.cosh(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 7):OpeningIndex] == "dxgrxxs":
                TempString = str(math.degrees(float(TempList[0])))
                OpeningIndex -= 7
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "xrf":
                TempString = str(math.erf(float(TempList[0])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "xrfc":
                TempString = str(math.erfc(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "xxp":
                TempString = str(math.exp(float(TempList[0])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "xxpmO":
                TempString = str(math.expm1(float(TempList[0])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "fabs":
                TempString = str(math.fabs(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 9):OpeningIndex] == "factorial":
                TempString = str(math.factorial(float(TempList[0])))
                OpeningIndex -= 9
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "floor":
                TempString = str(math.floor(float(TempList[0])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "fmod":
                TempString = str(math.fmod(float(TempList[0]), float(TempList[1])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "gamma":
                TempString = str(math.gamma(float(TempList[0])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "hypot":
                TempString = str(math.hypot(float(TempList[0]), float(TempList[1])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "ldxxp":
                TempString = str(math.ldexp(float(TempList[0]), float(TempList[1])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 6):OpeningIndex] == "lgamma":
                TempString = str(math.lgamma(float(TempList[0])))
                OpeningIndex -= 6
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "log":
                if TempListLen >= 2:
                    TempString = str(math.log(float(TempList[0]), float(TempList[1])))
                else:
                    TempString = str(math.log(float(TempList[0])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "logOp":
                TempString = str(math.log1p(float(TempList[0])))
                OpeningIndex -= 5
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "logT":
                TempString = str(math.log10(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "pow":
                TempString = str(math.pow(float(TempList[0]), float(TempList[1])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 7):OpeningIndex] == "radians":
                TempString = str(math.radians(float(TempList[0])))
                OpeningIndex -= 7
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "sin":
                TempString = str(math.sin(float(TempList[0])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "sinh":
                TempString = str(math.sinh(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "sqrt":
                TempString = str(math.sqrt(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 3):OpeningIndex] == "tan":
                TempString = str(math.tan(float(TempList[0])))
                OpeningIndex -= 3
            elif InputString[(OpeningIndex - 4):OpeningIndex] == "tanh":
                TempString = str(math.tanh(float(TempList[0])))
                OpeningIndex -= 4
            elif InputString[(OpeningIndex - 5):OpeningIndex] == "trunc":
                TempString = str(math.trunc(float(TempList[0])))
                OpeningIndex -= 5

        else:
            StartIndex = OpeningIndex

        InputString = InputString.replace(InputString[OpeningIndex:(ClosingIndex + 1)], TempString)

    return(InputString)

#===============================================================#"

if __name__ == '__main__':
    TempString = raw_input("Please type a string to calculate: ")
    if TempString == "":
        print(calculateIt("1*4+3.3/(3 + .3)*3(sqrt(4))/(sin(0) + 1)3"))
        print(calculateIt("10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5"))
    else:
        print(calculateIt(TempString))
