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
from models import ingredient

class Ingredients:
    ingList = []

    def __init__(self):
        for i in self.getData():
            ing = ingredient.Ingredient(i)
            self.ingList.append(ing)

    def get(self):
        return self.ingList

    def getData(self):
        client = MongoClient('mongodb://localhost:27017')
        db = client['easyCook']['ingredient']
        data = db.find()
        return(data)
