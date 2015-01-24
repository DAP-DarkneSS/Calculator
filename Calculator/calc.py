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

from val import Validator
from stuff import *
import math


class Calculator(Validator):
    '''A general calculation class.'''

    def calculateArithmetic(self):
        '''Calculates input simple arithmetical string expression to output string value.'''

        def where1NumberStarts(InputString, OperatorIndex):
            '''Returns input string index.'''
            FirstNumberStartsAt = OperatorIndex
            i = OperatorIndex - 1
            while FirstNumberStartsAt == OperatorIndex:
                if i == -1:
                    FirstNumberStartsAt = 0
                elif InputString[i] in OperatorsList:
                    if (i == 0) or (InputString[i-1] in OperatorsList):
                        FirstNumberStartsAt = i
                    else:
                        FirstNumberStartsAt = i + 1
                else:
                    i -= 1
            return(FirstNumberStartsAt)

        def where2NumberEnds(InputString, OperatorIndex, OperatorSymbolsCount):
            '''Returns input string index.'''
            SecondNumberEndsAt = OperatorIndex
            i = OperatorIndex + OperatorSymbolsCount + 1
# +1 to pass unary +/- sign.
            while SecondNumberEndsAt == OperatorIndex:
                if (i == len(InputString)) or (InputString[i] in OperatorsList):
                    SecondNumberEndsAt = i
                else:
                    i += 1
            return(SecondNumberEndsAt)

        while "**" in self.InputString:
            self.validatePlusMinus()
            OperatorSymbolsCount = 2
            OperatorIndex = self.InputString.find("**")
            FirstNumberStartsAt = where1NumberStarts(self.InputString, OperatorIndex)
            SecondNumberEndsAt = where2NumberEnds(self.InputString, OperatorIndex, OperatorSymbolsCount)
            FirstNumber = float(self.InputString[FirstNumberStartsAt:OperatorIndex])
            SecondNumber = float(self.InputString[(OperatorIndex + OperatorSymbolsCount):SecondNumberEndsAt])
            CalculationResult = str(FirstNumber ** SecondNumber)
            self.InputString = self.InputString.replace(self.InputString[FirstNumberStartsAt:SecondNumberEndsAt], CalculationResult)

        while "~" in self.InputString:
            self.validatePlusMinus()
            OperatorSymbolsCount = 1
            OperatorIndex = self.InputString.rfind("~")
# From the end to calculate inversion sequences.
            SecondNumberEndsAt = where2NumberEnds(self.InputString, OperatorIndex, OperatorSymbolsCount)
            SecondNumber = makeIntOrDie(self.InputString[(OperatorIndex + OperatorSymbolsCount):SecondNumberEndsAt])
            CalculationResult = str(~ SecondNumber)
            self.InputString = self.InputString.replace(self.InputString[OperatorIndex:SecondNumberEndsAt], CalculationResult)

        while any(Operator in self.InputString for Operator in ("*", "/", "%")):
            self.validatePlusMinus()
            OperatorsDict = {
                "*": self.InputString.find("*"),
                "/": self.InputString.find("/"),
                "%": self.InputString.find("%")}
            OperatorIndex = max(OperatorsDict.values())
            for i in OperatorsDict.keys():
                if (OperatorsDict[i] == OperatorIndex):
                    Operator = i
            if self.InputString[OperatorIndex + 1] == "/":
                Operator = "//"
                OperatorSymbolsCount = 2
            else:
                OperatorSymbolsCount = 1
            FirstNumberStartsAt = where1NumberStarts(self.InputString, OperatorIndex)
            SecondNumberEndsAt = where2NumberEnds(self.InputString, OperatorIndex, OperatorSymbolsCount)
            FirstNumber = float(self.InputString[FirstNumberStartsAt:OperatorIndex])
            SecondNumber = float(self.InputString[(OperatorIndex + OperatorSymbolsCount):SecondNumberEndsAt])
            if Operator == "*":
                CalculatedNumber = FirstNumber * SecondNumber
            elif Operator == "/":
                CalculatedNumber = FirstNumber / SecondNumber
            elif Operator == "//":
                CalculatedNumber = FirstNumber // SecondNumber
            elif Operator == "%":
                CalculatedNumber = FirstNumber % SecondNumber
            CalculationResult = str(CalculatedNumber)
            self.InputString = self.InputString.replace(self.InputString[FirstNumberStartsAt:SecondNumberEndsAt], CalculationResult)

        while (any(Operator in self.InputString for Operator in ("+", "-"))) and not (isItANumber(self.InputString)):
            self.validatePlusMinus()
            OperatorsDict = {
                "+": (self.InputString[1:].find("+") +1),
                "-": (self.InputString[1:].find("-") +1)}
# '1:' & '+1' to pass an unary sign.
            OperatorIndex = max(OperatorsDict.values())
            for i in OperatorsDict.keys():
                if (OperatorsDict[i] == OperatorIndex):
                    Operator = i
            OperatorSymbolsCount = 1
            FirstNumberStartsAt = where1NumberStarts(self.InputString, OperatorIndex)
            SecondNumberEndsAt = where2NumberEnds(self.InputString, OperatorIndex, OperatorSymbolsCount)
            FirstNumber = float(self.InputString[FirstNumberStartsAt:OperatorIndex])
            SecondNumber = float(self.InputString[(OperatorIndex + OperatorSymbolsCount):SecondNumberEndsAt])
            if Operator == "+":
                CalculatedNumber = FirstNumber + SecondNumber
            elif Operator == "-":
                CalculatedNumber = FirstNumber - SecondNumber
            CalculationResult = str(CalculatedNumber)
            self.InputString = self.InputString.replace(self.InputString[FirstNumberStartsAt:SecondNumberEndsAt], CalculationResult)

        while any(Operator in self.InputString for Operator in ("<<", ">>")):
            self.validatePlusMinus()
            OperatorsDict = {
                "<<": self.InputString.find("<<"),
                ">>": self.InputString.find(">>")}
            OperatorIndex = max(OperatorsDict.values())
            for i in OperatorsDict.keys():
                if (OperatorsDict[i] == OperatorIndex):
                    Operator = i
            OperatorSymbolsCount = 2
            FirstNumberStartsAt = where1NumberStarts(self.InputString, OperatorIndex)
            SecondNumberEndsAt = where2NumberEnds(self.InputString, OperatorIndex, OperatorSymbolsCount)
            FirstNumber = makeIntOrDie(self.InputString[FirstNumberStartsAt:OperatorIndex])
            SecondNumber = makeIntOrDie(self.InputString[(OperatorIndex + OperatorSymbolsCount):SecondNumberEndsAt])
            if Operator == "<<":
                CalculatedNumber = FirstNumber << SecondNumber
            elif Operator == ">>":
                CalculatedNumber = FirstNumber >> SecondNumber
            CalculationResult = str(CalculatedNumber)
            self.InputString = self.InputString.replace(self.InputString[FirstNumberStartsAt:SecondNumberEndsAt], CalculationResult)

        while "&" in self.InputString:
            self.validatePlusMinus()
            OperatorSymbolsCount = 1
            OperatorIndex = self.InputString.find("&")
            FirstNumberStartsAt = where1NumberStarts(self.InputString, OperatorIndex)
            SecondNumberEndsAt = where2NumberEnds(self.InputString, OperatorIndex, OperatorSymbolsCount)
            FirstNumber = makeIntOrDie(self.InputString[FirstNumberStartsAt:OperatorIndex])
            SecondNumber = makeIntOrDie(self.InputString[(OperatorIndex + OperatorSymbolsCount):SecondNumberEndsAt])
            CalculationResult = str(FirstNumber & SecondNumber)
            self.InputString = self.InputString.replace(self.InputString[FirstNumberStartsAt:SecondNumberEndsAt], CalculationResult)

        while any(Operator in self.InputString for Operator in ("^", "|")):
            self.validatePlusMinus()
            OperatorsDict = {
                "^": self.InputString.find("^"),
                "|": self.InputString.find("|")}
            OperatorIndex = max(OperatorsDict.values())
            for i in OperatorsDict.keys():
                if (OperatorsDict[i] == OperatorIndex):
                    Operator = i
            OperatorSymbolsCount = 1
            FirstNumberStartsAt = where1NumberStarts(self.InputString, OperatorIndex)
            SecondNumberEndsAt = where2NumberEnds(self.InputString, OperatorIndex, OperatorSymbolsCount)
            FirstNumber = makeIntOrDie(self.InputString[FirstNumberStartsAt:OperatorIndex])
            SecondNumber = makeIntOrDie(self.InputString[(OperatorIndex + OperatorSymbolsCount):SecondNumberEndsAt])
            if Operator == "^":
                CalculatedNumber = FirstNumber ^ SecondNumber
            elif Operator == "|":
                CalculatedNumber = FirstNumber | SecondNumber
            CalculationResult = str(CalculatedNumber)
            self.InputString = self.InputString.replace(self.InputString[FirstNumberStartsAt:SecondNumberEndsAt], CalculationResult)
            
 #===============================================================#

    def calculateIt(self):
        '''Calculates any (the description is a lie) input string expression to output string value.'''

        self.validateSpaces()
        self.validateDecimalPoint()
        self.validateMathFunctions()
        self.validateMultiplication()
        self.validateMathConstants()

        while "(" in self.InputString:
            ClosingIndex = self.InputString.find(")")
            OpeningIndex = ClosingIndex - self.InputString[ClosingIndex::-1].find("(")
            TempList = self.InputString[(OpeningIndex + 1):ClosingIndex].split(",")
            TempListLen = len(TempList)
            for i in xrange(TempListLen):
                TempList[i] = Calculator(TempList[i])
                TempList[i].calculateArithmetic()
                TempList[i] = TempList[i].InputString

            if doesItContainFunction(self.InputString[:OpeningIndex], MustEndWith = True):

                if self.InputString[(OpeningIndex - 3):OpeningIndex] == "abs":
                    TempString = str(abs(float(TempList[0])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "acos":
                    TempString = str(math.acos(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "acosh":
                    TempString = str(math.acosh(float(TempList[0])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "asin":
                    TempString = str(math.asin(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "asinh":
                    TempString = str(math.asinh(float(TempList[0])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "atan":
                    TempString = str(math.atan(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "atanT":
                    TempString = str(math.atan2(float(TempList[0]), float(TempList[1])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "atanh":
                    TempString = str(math.atanh(float(TempList[0])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "cxil":
                    TempString = str(math.ceil(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 8):OpeningIndex] == "copysign":
                    TempString = str(math.copysign(float(TempList[0]), float(TempList[1])))
                    OpeningIndex -= 8
                elif self.InputString[(OpeningIndex - 3):OpeningIndex] == "cos":
                    TempString = str(math.cos(float(TempList[0])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "cosh":
                    TempString = str(math.cosh(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 7):OpeningIndex] == "dxgrxxs":
                    TempString = str(math.degrees(float(TempList[0])))
                    OpeningIndex -= 7
                elif self.InputString[(OpeningIndex - 3):OpeningIndex] == "xrf":
                    TempString = str(math.erf(float(TempList[0])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "xrfc":
                    TempString = str(math.erfc(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 3):OpeningIndex] == "xxp":
                    TempString = str(math.exp(float(TempList[0])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "xxpmO":
                    TempString = str(math.expm1(float(TempList[0])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "fabs":
                    TempString = str(math.fabs(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 9):OpeningIndex] == "factorial":
                    TempString = str(math.factorial(float(TempList[0])))
                    OpeningIndex -= 9
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "floor":
                    TempString = str(math.floor(float(TempList[0])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "fmod":
                    TempString = str(math.fmod(float(TempList[0]), float(TempList[1])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "gamma":
                    TempString = str(math.gamma(float(TempList[0])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "hypot":
                    TempString = str(math.hypot(float(TempList[0]), float(TempList[1])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "ldxxp":
                    TempString = str(math.ldexp(float(TempList[0]), float(TempList[1])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 6):OpeningIndex] == "lgamma":
                    TempString = str(math.lgamma(float(TempList[0])))
                    OpeningIndex -= 6
                elif self.InputString[(OpeningIndex - 3):OpeningIndex] == "log":
                    if TempListLen >= 2:
                        TempString = str(math.log(float(TempList[0]), float(TempList[1])))
                    else:
                        TempString = str(math.log(float(TempList[0])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "logOp":
                    TempString = str(math.log1p(float(TempList[0])))
                    OpeningIndex -= 5
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "logT":
                    TempString = str(math.log10(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 3):OpeningIndex] == "pow":
                    TempString = str(math.pow(float(TempList[0]), float(TempList[1])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 7):OpeningIndex] == "radians":
                    TempString = str(math.radians(float(TempList[0])))
                    OpeningIndex -= 7
                elif self.InputString[(OpeningIndex - 3):OpeningIndex] == "sin":
                    TempString = str(math.sin(float(TempList[0])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "sinh":
                    TempString = str(math.sinh(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "sqrt":
                    TempString = str(math.sqrt(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 3):OpeningIndex] == "tan":
                    TempString = str(math.tan(float(TempList[0])))
                    OpeningIndex -= 3
                elif self.InputString[(OpeningIndex - 4):OpeningIndex] == "tanh":
                    TempString = str(math.tanh(float(TempList[0])))
                    OpeningIndex -= 4
                elif self.InputString[(OpeningIndex - 5):OpeningIndex] == "trunc":
                    TempString = str(math.trunc(float(TempList[0])))
                    OpeningIndex -= 5

            else:
                TempString = TempList[0]

            self.InputString = self.InputString.replace(self.InputString[OpeningIndex:(ClosingIndex + 1)], TempString)
