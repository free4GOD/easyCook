#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Easy-Cook: The week menu planner.
# Copyright (C) 2019  free4fun (Mauricio Sosa Giri) <free4fun@riseup.net>


#This file is part of Easy-Cook.

#Easy-Cook is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#Easy-Cook is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
from pymongo import MongoClient

class Ingredient:

    def __init__(self, data):
        self.name = data['name']
        self.picture = data['picture']
        self.type = data['type']
        self.price = data['price']
        self.catgory = data['category']
        self.equivalents = data['equivalents']

    def setName(self, value):
        self.name = value

    def setPicture(self, value):
        self.picture = value

    def setType(self, value):
        self.type = value

    def setPrice(self, value):
        self.price = value

    def setCategory(self, value):
        self.category = value

    def setEquivalents(self, value):
        self.equivalents = value

    def getName(self):
        return self.name

    def getPicture(self):
        return self.picture

    def getType(self):
        return self.name

    def getPrice(self):
        return self.price

    def getCategory(self):
        return self.category

    def getEquivalents(self):
        return self.equivalents
