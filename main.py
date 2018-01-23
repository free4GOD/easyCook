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

import sys
import re
import classes
import ui
import methods

try:
  import pygtk
  pygtk.require("2.16")
except:
  pass
try:
  import gtk
except:
  print("ERROR: GTK No disponible.")
  sys.exit(1)

builder = gtk.Builder()
builder.add_from_file("easy-cook.glade")
ui = ui.ui()
mtd = methods.methods()

def on_selection_changed(self):
  try:
    row, itr = ui.get_selected_row(builder, builder.get_object("treeview"))
    if itr is None:
      return None
    if not itr:
      return None
    else:
      recipe = mtd.searchRecipe(row.get_value(itr, 0), recipes)
      ui.showRecipe(builder, recipe)
  except:
    pass

def toNewRecipe(self):
  ui.clear_recipe_dialog(self, builder)
  data = ui.newRecipe(self, builder)
  while not data:
    if data is "Cancel":
      break
    data = ui.newRecipe(self, builder)
  if data is "Cancel":
    return None
  if data:
    if mtd.searchRecipe(builder.get_object("entryname").get_text(), recipes):
      ui.showError(builder, "Name already in use")
    recipe = mtd.saveRecipe(self, data)
    recipes.append(recipe)
    ui.refreshRecipes(builder, recipes)

def toAddToMenu(self):
  result, name, daytime = ui.addToMenu(self, builder)
  if result:
    cell_list = mtd.ValuesToList(result)
    ui.checkAddToMenu(builder, cell_list, name, daytime)

def toGenerateShoplist(self):
  list_meals = ui.generateMeals(self, builder)
  shoplist = mtd.classifyIngredients(list_meals, recipes)
  shoplist = mtd.estimateQuantities(shoplist, ingredients)
  filename = ui.showShoplist(builder, shoplist)
  if filename == "print":
    mtd.printBuys(shoplist)
  elif filename:
    mtd.saveBuys(shoplist, filename)

def toModifyRecipe(self):
  row, itr = ui.get_selected_row(builder, builder.get_object("treeview"), True)
  if itr:
    oldrcp = mtd.searchRecipe(row.get_value(itr, 0), recipes)
    ui.clear_recipe_dialog(self, builder)
    data = ui.modifyRecipe(self, builder, oldrcp)
    while not data:
      if data is "Cancel":
        break
      data = ui.newRecipe(self, builder)
    if data is "Cancel":
      return None
    if data:
      recipe = mtd.saveRecipe(self, data)
      mtd.removeRecipe(recipes, oldrcp)
      recipes.append(recipe)
      ui.refreshRecipes(builder, recipes)

def toDelFromMenu(self):
  ui.delFromMenu(builder)

def toAddIng(self):
  ui.addIng(self, builder)

def toDelIng(self):
  ui.delIng(self, builder)

def toAddStp(self):
  ui.addStp(self, builder)

def toDelStp(self):
  ui.delStp(self, builder)

def toConfigureIngredients(self):
  dlging = builder.get_object("dlgListIngredients")
  response = ui.configureIngredients(builder, ingredients, dlging)
  while response != gtk.RESPONSE_OK:
    if response == 43: # AddIngredient
      data = ui.newIngredient(builder)
      if data == "Cancel":
        pass
      elif data:
        if mtd.searchIngredient(builder.get_object("ingentryname").get_text(), ingredients):
          ui.showError(builder, "Name already in use")
        else:
          ingredient = mtd.saveIngredient(self, data)
          ingredients.append(ingredient)
          ui.refreshIngredients(builder, ingredients)
    if response == 44: # EditIngredient
      row, iter = ui.get_selected_row(builder, builder.get_object("treeview7"), True)
      if iter:
        ingredient = mtd.searchIngredient(row.get_value(iter, 0), ingredients)
        data = ui.modifyIngredient(builder, ingredient)
        while not data:
          if data is "Cancel":
            break
          data = ui.newRecipe(self, builder)
        if data is "Cancel":
          pass
        elif data:
          ingredient = mtd.saveIngredient(self, data)
          olding = mtd.searchIngredient(ingredient.name, ingredients)
          mtd.removeIngredient(ingredients, olding)
          mtd.saveIngredient(self, data)
          ingredients.append(ingredient)
          ui.refreshIngredients(builder, ingredients)
    if response == 45: # DelIngredient
      name = ui.delIngredient(builder)
      if name:
        olding = mtd.searchIngredient(name, ingredients)
        rcps = mtd.inRecipe(olding, recipes)
        if rcps:
          text = mtd.listToString(rcps)
          text = text[:-1] #Remove last comma
          ui.showError(builder, "Can't remove " + olding.name + " is in: " + text)
        else:
          mtd.removeIngredient(ingredients, olding)
          ui.refreshIngredients(builder,  ingredients)
    response = ui.configureIngredients(builder, ingredients, dlging)
  dlging.hide()

def toConfigureRecipes(self):
  dlgrcp = builder.get_object("dlgListRecipes")
  response = ui.configureRecipes(builder, recipes, dlgrcp)
  while response != gtk.RESPONSE_OK:
    if response == 43: # AddRecipe
      toNewRecipe(self)
      ui.refreshRecipes(builder, recipes)
    if response == 44: # EditRecipe
      row, iter = ui.get_selected_row(builder, builder.get_object("treeview11"), True)
      if iter:
        recipe = mtd.searchRecipe(row.get_value(iter, 0), recipes)
        data = ui.modifyRecipe(recipes, builder, recipe)
        while not data:
          if data is "Cancel":
            break
          data = ui.newRecipe(self, builder)
        if data is "Cancel":
          pass
        elif data:
          recipe = mtd.saveRecipe(self, data)
          oldrcp = mtd.searchRecipe(recipe.name, recipes)
          mtd.removeRecipe(recipes, oldrcp)
          recipes.append(recipe)
          ui.refreshRecipes(builder, recipes)
    if response == 45: # DelRecipe
      name = ui.delRecipe(builder)
      if name:
        oldrcp = mtd.searchRecipe(name, recipes)
        mtd.removeRecipe(recipes, oldrcp)
        ui.refreshRecipes(builder, recipes)
    response = ui.configureRecipes(builder, recipes, dlgrcp)
  dlgrcp.hide()

def toAddMeasure(self):
  ui.addMeasure(builder)

def toDelMeasure(self):
  ui.delMeasure(builder)

def toImportRecipe(self):
  filename = ui.openDlg(builder)
  if filename:
    mtd.importRecipe(filename)
  ingredients = mtd.loadIngredients()
  recipes = mtd.loadRecipes()
  ui.refreshIngredients(builder,  ingredients)
  ui.refreshRecipes(builder,  recipes)

def toExportRecipe(self):
  row, itr = ui.get_selected_row(builder, builder.get_object("treeview"), True)
  if itr:
    recipe = mtd.searchRecipe(row.get_value(itr, 0), recipes)
    includeingr = ui.includeIngredients(builder)
    filename = ui.saveDlg(builder)
    mtd.exportRecipe(recipe, filename, includeingr)
    ui.refreshRecipes(builder,  recipes)

def toSaveMenu(self):
  menu = ui.getMenu(builder)
  mtd.saveMenu(menu)

def toClearMenu(self):
  ui.clearMenu(builder)

def toLoadMenu(self):
  menu = mtd.loadMenu()
  if menu:
    ui.loadMenu(builder, menu)
signals = {
  "on_mainWindow_destroy" : ui.quit,
  "on_newRecipe_clicked" : toNewRecipe,
  "on_addToMenu_clicked": toAddToMenu,
  "on_shopList_clicked" : toGenerateShoplist,
  "on_details_clicked" : toModifyRecipe,
  "on_addIng_clicked" : toAddIng,
  "on_delIng_clicked" : toDelIng,
  "on_addStp_clicked" : toAddStp,
  "on_delStp_clicked" : toDelStp,
  "on_delFromMenu_clicked" : toDelFromMenu,
  "on_Ingredients_activate" : toConfigureIngredients,
  "on_Recipes_activate" : toConfigureRecipes,
  "on_dlgListIngredients_clicked" : toConfigureIngredients,
  "on_btnAddMeassure_clicked" : toAddMeasure,
  "on_btnDelMeassure_clicked" : toDelMeasure,
  "on_importrcp_activate" : toImportRecipe,
  "on_exportrcp_activate" : toExportRecipe,
  "on_savemenu_activate" : toSaveMenu,
  "on_clearmenu_activate" : toClearMenu,
  "on_loadmenu_activate" : toLoadMenu
}

treeview = builder.get_object("treeview")
treeview.get_selection().connect("changed", on_selection_changed)
builder.connect_signals(signals)
liststore = builder.get_object("liststore")
recipes = mtd.loadRecipes()
ingredients = mtd.loadIngredients()
mtd.loadMenu()
ui.refreshRecipes(builder, recipes)
ui.refreshIngredients(builder, ingredients)
for i in range(7):
  builder.get_object("listlunch").append(None)
  builder.get_object("listdinner").append(None)
wnd = builder.get_object("mainWindow")
wnd.maximize()
gtk.main()
