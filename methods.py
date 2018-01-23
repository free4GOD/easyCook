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

import os;
import classes;
import string;
import zipfile;
import shutil;
import re;
from fractions import Fraction

class methods:
  def __init__(self):
    pass

  def loadRecipes(self):
    global recipe
    files = os.listdir("recipes/")
    recipesList = []
    for i in files:
      archive = open("recipes/"+i, "r")
      data = archive.readlines()
      recipe = classes.Recipe(str(data[0]).strip(),str(data[1]).strip(),eval(data[2]),eval(data[3]),str(data[4]).strip(),eval(data[5]),eval(data[6]))
      recipesList.append(recipe)
    return recipesList

  def loadIngredients(self):
    global ingredient
    files = os.listdir("ingredients/")
    ingredientsList = []
    for i in files:
      archive = open("ingredients/"+i, "r")
      data = archive.readlines()
      ingredient = classes.Ingredient(str(data[0]).strip(),str(data[1]).strip(),str(data[2]).strip(),str(data[3]).strip(),eval(data[4]),eval(data[5]),eval(data[6]))
      ingredientsList.append(ingredient)
    return ingredientsList

  def checkFreeMeal(self, day, meal):
    return False;

  def createRecipe(self, recipes, name):
    instance = recipes.index(name)

  def searchRecipe(self, name, recipes):
    for i in recipes:
      if i.name == name:
        return i
    return None

  def searchIngredient(self, name, ingredients):
    for i in ingredients:
      if i.name == name:
        return i
    return None

  def removeRecipe(self, recipes, recipe):
    name = string.translate(recipe.name, None,'\'"¡!·$%&/()=?¿*^-\áóéúíñÑ´¨çÇ`+"')
    name = string.replace(string.lower(name), ' ', '_')
    filename = "recipes/"+name+".rcp"
    try :
      os.remove(filename)
    except:
      print "ERROR: Can't remove recipe "+ filename +"."
    for i in recipes:
      if i.name == recipe.name:
        recipes.remove(recipe)
    return recipes

  def removeIngredient(self, ingredients, ingredient):
    name = string.translate(ingredient.name, None,'\'"¡!·$%&/()=?¿*^-\áóéúíñÑ´¨çÇ`+"')
    name = string.replace(string.lower(name), ' ', '_')
    filename = "ingredients/"+name+".ing"
    try :
      os.remove(filename)
    except:
      print "ERROR: Can't remove ingredient "+ filename +"."
    for i in ingredients:
      if i.name == ingredient.name:
        ingredients.remove(ingredient)
    return ingredients

  def saveRecipe(self, widget, data):
    filename = string.translate(str(data[0]), None,'\'"¡!·$%&/()=?¿*^-\áóéúíñÑ´¨çÇ`+"')
    filename = string.replace(string.lower(filename), ' ', '_')
    newfile = open("recipes/"+filename+".rcp", 'w')
    newfile.write(data[0]+"\n") # Name
    newfile.write(str(data[1])+"\n") # Category
    newfile.write(str(data[2])+"\n") # Yield
    newfile.write(str(data[3])+"\n") # Tags
    newfile.write(str(data[4])+"\n") # Image
    newfile.write(str(data[5])+"\n") # Ingredients
    newfile.write(str(data[6])+"\n") # Procedure
    newfile.close()
    return classes.Recipe(data[0].strip(),str(data[1]).strip(),data[2],data[3],str(data[4]).strip(),data[5],data[6])

  def saveIngredient(self, widget, data):
    filename = string.translate(str(data[0]), None,'\'"¡!·$%&/()=?¿*^-\áóéúíñÑ´¨çÇ`+"')
    filename = string.replace(string.lower(filename), ' ', '_')
    newfile = open("ingredients/"+filename+".ing", 'w')
    newfile.write(data[0]+"\n") # Name
    newfile.write(str(data[1])+"\n") # Type
    newfile.write(str(data[2])+"\n") # Group
    newfile.write(str(data[3])+"\n") # Measure
    newfile.write(str(data[4])+"\n") # Equivalents
    newfile.write(str(data[5])+"\n") # Packages
    newfile.write(str(data[6])+"\n") # Prices
    newfile.close()
    return classes.Ingredient(str(data[0]).strip(),str(data[1]).strip(),str(data[2]).strip(),str(data[3]).strip(),data[4],data[5],data[6])

  def classifyIngredients(self, list_meals, recipes):
    finalist = []
    shoplist = []
    for meal in list_meals:
      names = self.ValuesToList(meal)
      for name in names:
        recipe = self.searchRecipe(name, recipes)
        if recipe:
          for ingr in recipe.ingredients:
            if shoplist.count(ingr[0]): # Allready exists
              ind = shoplist.index(ingr[0])
              shoplist[ind+1].extend(ingr[1:])
            else: # Must add to list
              shoplist.append(ingr[0])
              shoplist.append(ingr[1:])
    for i in range(int(len(shoplist))):
      if i == 0 or i % 2 == 0:
        tmp = shoplist.pop(0)
        finalist.append([tmp])
      if i == 1 or i % 2 != 0:
        tmp = shoplist.pop(0)
        finalist[int(len(finalist)-1)].extend([tmp])
    return finalist

  def estimateQuantities(self, shoplist, ingredients):
    result = []
    for elem in shoplist:
      ingredient = self.searchIngredient(elem[0], ingredients)
      totalqnt = 0
      quantities = elem[1]
      for each in quantities:
        e = each.partition(' ')
        if e[2] == "Units" or e[2] == "Kilos" or e[2] == "Liters":
          totalqnt = totalqnt + float(Fraction(e[0]))
        elif e[2] == "Grams" or e[2] == "Mililiters":
          totalqnt = totalqnt + float(Fraction(e[0]))/1000.0
        else:
          # Remove when sure all ingredients and measures exists
          equiv = None
          for measure in ingredient.equivalents:
            if measure[0] == e[2]:
              equiv = measure[1]
              totalqnt = totalqnt + float(Fraction(e[0]))*float(equiv)
# Uncomment when sure all ingredients and measures exists
#              break
          if not equiv:
            print ingredient.name + " hasn't any equivalence."
      if totalqnt - int(totalqnt) == 0:
        totalqnt = int(totalqnt)
      else:
        totalqnt = str(round(totalqnt,3))
      result.append([ingredient.name, str(totalqnt) + " " + ingredient.measure])
    return result

  def saveBuys(self, shoplist, filename):
    newfile = open(filename+".txt", 'w')
    for elem in shoplist:
      newfile.write(str(elem)+"\n")
    newfile.close()

  def printBuys(self, shoplist):
    pc = os.name
    if pc == 'posix' :
      os.system ('lp -q100 ' + str(shoplist))
    elif pc == 'nt' :
      try :
        import win32api
        win32api.ShellExecute(0, 'print', str(shoplist), None, '.', 0)
      except:
        print "ERROR: win32api no disponible."
    else:
      print "ERROR: No se reconoce el sistema operativo."

  def searchIngredient(self, name, ingredients):
    for i in ingredients:
      if i.name == name:
        return i
    return None

  def exportRecipe(self, recipe, filename, includeIngr):
    archive_list = list()
    if includeIngr:
      for ing in recipe.ingredients:
        ingName = string.translate(str(ing[0]), None,'\'"¡!·$%&/()=?¿*^-\áóéúíñÑ´¨çÇ`+"')
        ingName = string.replace(string.lower(ingName), ' ', '_')
        try:
          shutil.copyfile("ingredients/"+ingName+".ing","data/export/"+ingName+".ing")
          archive_list.append("data/export/"+ingName+".ing")
        except:
          print "ERROR: Can't export recipe. 1"
          return None
    rcpName = string.translate(recipe.name, None,'\'"¡!·$%&/()=?¿*^-\áóéúíñÑ´¨çÇ`+"')
    rcpName = string.replace(string.lower(rcpName), ' ', '_')
    try:
      shutil.copyfile("recipes/"+rcpName+".rcp","data/export/"+rcpName+".rcp")
      archive_list.append("data/export/"+rcpName+".rcp")
    except:
      print "ERROR: Can't export recipe. 2"
      return None
    zfilename = filename + ".zip"
    zout = zipfile.ZipFile(zfilename, "w")
    for fname in archive_list:
      zout.write(fname)
    zout.close()

  def importRecipe(self, path):
    zfile = zipfile.ZipFile(path, "r")
    for info in zfile.infolist():
      fname = info.filename
      data = zfile.read(fname)
      fname = re.split('/', fname)[-1]
      if fname.endswith(".ing"):
        fout = open("ingredients/"+fname, "w")
        fout.write(data)
        fout.close()
      if fname.endswith(".rcp"):
        fout = open("recipes/"+fname, "w")
        fout.write(data)
        fout.close()

  def saveMenu(self, menu):
    try:
      newfile = open("data/menu", 'w')
      newfile.write(str(menu))
      newfile.close()
    except:
      print "ERROR: Can't save menu"

  def loadMenu(self):
    try:
      archive = open("data/menu", "r")
      data = archive.readlines()
      archive.close()
    except:
      print "ERROR: Can't load menu"
      return None
    return data

  def inRecipe(self, ingredient, recipes):
    result = list()
    for rcp in recipes:
      rcps = list()
      for ings in rcp.ingredients:
        if ingredient.name == ings[0]:
          rcps.append(rcp.name)
      if rcps:
        result.append(rcps)
    return result

  def listToString(self, thelist):
    result = ""
    for i in thelist:
      if type(i).__name__=='list':
        result = result + self.listToString(i)
      else:
        result = result + " " + str(i) +","
    return result

  def ValuesToList(self, values):
    array_value = re.split(',', values)
    new_array = []
    for pos in array_value:
      new_array.append(str(pos).strip())
    return new_array
