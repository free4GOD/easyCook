#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Easy-Cook: The week menu planner.
# Copyright (C) 2011  barbanegra (Mauricio Sosa Giri) <msosagiri@gmail.com>


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

class Recipe:
  def __init__(self,name,category,yields,tags,image,ingredients,procedure):
    self.name = name
    self.category = category
    self.yields = yields
    self.tags = tags
    self.image = image
    self.ingredients = ingredients
    self.procedure = procedure


class Ingredient:
  def __init__(self,name,thetype,group,measure, equivs,packs,prices):
    self.name = name # The identifier
    self.type = thetype # Binary value: Solid or Liquid
    self.group = group #Only one of this: Milky. Meats and eggs. Fruits and vegetables. Bread and Cereals. Fats and Oils. Minerals, Nutrients. Drinks
    self.measure = measure # Trinary value Liters, Kilos, Units
    self.equivalents = equivs # a list
    self.packages = packs # a list
    self.prices = prices # a list
