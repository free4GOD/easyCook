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
import gtk
import re;
import string;

class ui:
  def __init__(self):
    pass

  def quit(self, widget):
    sys.exit(0)

  def addIng(self, widget, builder):
    #TODO check if ingredient is allready added, then add the new quantity to the old one.
    dmes = { 'Cups' : 0, 'Glasses' : 1, 'Grams' : 2, 'Kilos' : 3, 'Liters' : 4 , 'Milliliters' : 5 , 'Pinch' : 6 , 'Spoonfuls' : 7 , 'Teaspoons' : 8, 'Units' : 9 }
    ing =  self.get_active_text(builder.get_object("cboxentrying"))
    qnt = builder.get_object("entryqnt").get_text()
    mes = self.get_active_text(builder.get_object("cboxmeasure"))
    if not ing:
      self.showError(builder, "Name field is empty.")
      return False
    elif not qnt:
      self.showError(builder, "Quantity field is empty.")
      return False
    elif not qnt.isdigit():
      self.showError(builder, "Quantity field must be a number. Example: 13, 20.50, 4/3")
    else:
      builder.get_object("nlistingredients").append([ing, qnt + " " + mes])
      builder.get_object("entryqnt").set_text("")

  def delIng(self, widget, builder):
    row, iter = self.get_selected_row(builder, builder.get_object("treevnring"), True)
    if iter:
      row.remove(iter)

  def addStp(self, widget, builder):
    entry = builder.get_object("entry1").get_text()
    if entry is "":
      self.showError(builder, "Empty field.")
    else:
      builder.get_object("nlistprocedures").append([entry])
      builder.get_object("entry1").clear()
      builder.get_object("entry1").child.set_text("")

  def  delStp(self, widget, builder):
    row, iter = self.get_selected_row(builder, builder.get_object("treevnrproc"), True)
    if iter:
      row.remove(iter)

  def newRecipe(self, widget, builder):
      newrec = builder.get_object("dlgRecipe")
      response = newrec.run()
      newrec.hide()
      if response == gtk.RESPONSE_OK:
        data = self.check_new_recipe(widget, builder)
        if data:
          return data
      elif response == gtk.RESPONSE_CANCEL:
        return "Cancel"
      return False

  def check_new_recipe(self, widget, builder):
    name = builder.get_object("entryname").get_text()
    if not name:
      self.showError(builder, "Name must not be empty.")
      return False
    cat = self.get_active_text(builder.get_object("cboxcategory"))
    yields= [str(builder.get_object("adjustment1").get_value())[0:-2],self.get_active_text(builder.get_object("combobox1"))]
    tags = []
    if builder.get_object("chkfast").get_active():
      tags.append("Fast")
    if builder.get_object("chkappetizer").get_active():
      tags.append("Appetizer")
    if builder.get_object("chklowcalories").get_active():
      tags.append("Low Calories")
    if builder.get_object("chkevents").get_active():
      tags.append("Events")
    if builder.get_object("chkvegetarian").get_active():
      tags.append("Vegetarian")
    if builder.get_object("chkinternational").get_active():
      tags.append("International")
    if builder.get_object("chkbirthday").get_active():
      tags.append("Birthday")
    if builder.get_object("chkfittings").get_active():
      tags.append("Fittings")
    image = builder.get_object("filechooserbutton1").get_filename()
    ingr = self.get_array_data(builder.get_object("nlistingredients"), builder, "treevnring")
    if not ingr:
      self.showError(builder, "Ingredients must not be empty.")
      return False
    proc = self.get_column_data(builder.get_object("nlistprocedures"),0)
    if not proc:
      self.showError(builder, "Procedure must not be empty.")
      return False
    return [name, cat, yields, tags, image, ingr, proc]

  def addToMenu(self, widget, builder):
    dict = {'Monday': 0, 'Tuesday': 1, 'Wednesday' : 2, 'Thursday' : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6}
    row, itr= self.get_selected_row(builder, builder.get_object("treeview"), True)
    if itr:
      name = row.get_value(itr, 0)
      addmenu = builder.get_object("dlgaddToMenu")
      response = addmenu.run()
      addmenu.hide()
      if response == gtk.RESPONSE_OK:
        day = builder.get_object("comboday").get_active_text()
        lunch = builder.get_object("buttonlunch").get_active()
        if lunch:
          listlunch = builder.get_object("listlunch")
          iter = listlunch.get_iter(dict[day])
          occupied = listlunch.get_value(iter, 0)
          if occupied:
            return occupied, name, 'lunch'
          else:
            listlunch.set_value(iter, 0, name)
        else:
          listdinner = builder.get_object("listdinner")
          iter = listdinner.get_iter(dict[day])
          occupied = listdinner.get_value(iter, 0)
          if occupied:
            return occupied, name, 'dinner'
          else:
            listdinner.set_value(iter, 0, name)
    return None, None, None

  def checkAddToMenu(self, builder, cell_list, name, daytime):
    dict = {'Monday': 0, 'Tuesday': 1, 'Wednesday' : 2, 'Thursday' : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6}
    for i in cell_list:
      if i == name:
        self.showError(builder, "Meal allready assigned.")
        return None
    listlunch = builder.get_object("listlunch")
    day = builder.get_object("comboday").get_active_text()
    iter = listlunch.get_iter(dict[day])
    cell_list.append(name)
    cell = self.listToValues(cell_list)
    if daytime == 'lunch':
      listlunch.set_value(iter, 0, cell)
    if daytime == 'dinner':
      listdinner.set_value(iter, 0, cell)

  def delFromMenu(self,  builder):
    dict = {'Monday': 0, 'Tuesday': 1, 'Wednesday' : 2, 'Thursday' : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6}
    addmenu = builder.get_object("dlgaddToMenu")
    response = addmenu.run()
    addmenu.hide()
    if response == gtk.RESPONSE_OK:
      day = builder.get_object("comboday").get_active_text()
      lunch = builder.get_object("buttonlunch").get_active()
      if lunch:
        listlunch = builder.get_object("listlunch")
        iter = listlunch.get_iter(dict[day])
        listlunch.set_value(iter, 0, None)
      else:
        listdinner = builder.get_object("listdinner")
        iter = listdinner.get_iter(dict[day])
        listdinner.set_value(iter, 0, None)

  def generateMeals(self,  widget, builder):
    meals = []
    listlunch = builder.get_object("listlunch")
    listdinner = builder.get_object("listdinner")
    iter_lunch = listlunch.get_iter_root()
    iter_dinner = listdinner.get_iter_root()
    while iter_lunch:
      lunch = listlunch.get_value(iter_lunch, 0)
      if lunch:
        meals.append(lunch)
      iter_lunch = listlunch.iter_next(iter_lunch)
    while iter_dinner:
      dinner = listdinner.get_value(iter_dinner, 0)
      if dinner:
        meals.append(dinner)
      iter_dinner = listdinner.iter_next(iter_dinner)
    return meals

  def showShoplist(self, builder, shoplist):
    lstbuys = builder.get_object("lstorebuys")
    lstbuys.clear()
    for i in shoplist:
      lstbuys.append(i)
    dlg = builder.get_object("dlgbuys")
    response = dlg.run()
    dlg.hide()
    if response == 42: # Save file
      filename = self.saveDlg(builder)
      if filename:
        return filename
    if response == 77: # Print
      return "print"

  def saveDlg(self, builder):
    dlg = gtk.FileChooserDialog("Save file...",None, gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    dlg.set_default_response(gtk.RESPONSE_OK)
    response = dlg.run()
    if response == gtk.RESPONSE_OK:
      filename = dlg.get_filename()
    dlg.destroy()
    if filename:
      return filename

  def openDlg(self, builder):
    dlg = gtk.FileChooserDialog(title="Select a file", parent=None,action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=("OK",True,"Cancel",False))
    response = dlg.run()
    if response:
      fullname = dlg.get_filename()
    dlg.destroy()
    return fullname

  def modifyRecipe(self,  widget, builder, recipe):
      dcat = { 'Seafood' : 0, 'Meals': 1, 'Pastas' : 2, 'Pizzas' : 3, 'Salads' : 4, 'Sauces' : 5, 'Soups' : 6, 'Vegetables' : 7, 'Fishes' : 8, 'Cakes' : 9, 'Desserts' : 10, 'None' : 11 }
      builder.get_object("entryname").set_text(recipe.name)
      builder.get_object("cboxcategory").set_active(dcat[recipe.category])
      builder.get_object("spinbutton1").set_value(float(recipe.yields[0]))
      builder.get_object("combobox1").set_active(1)
      for elem in recipe.tags:
        if elem == "Fast":
          builder.get_object("chkfast").set_active(True)
        if elem == "Appetizer":
          builder.get_object("chkappetizer").set_active(True)
        if elem == "Low Calories":
          builder.get_object("chklowcalories").set_active(True)
        if elem == "Events":
          builder.get_object("chkevents").set_active(True)
        if elem == "Vegetarian":
          builder.get_object("chkvegetarian").set_active(True)
        if elem == "International":
          builder.get_object("chkinternational").set_active(True)
        if elem == "Birthday":
          builder.get_object("chkbirthday").set_active(True)
        if elem == "Fitting":
          builder.get_object("chkfitting").set_active(True)
      if recipe.image != "None":
        try:
          builder.get_object("image5").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(recipe.image))
        except:
          builder.get_object("image5").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("images/default.jpg"))
          print "Error: Image: " + recipe.image + " not found"
      else:
        builder.get_object("image5").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("images/default.jpg"))
      lingr = builder.get_object("nlistingredients")
      lingr.clear()
      for row in recipe.ingredients:
        lingr.append(row)
      lpcdr = builder.get_object("nlistprocedures")
      lpcdr.clear()
      for i in recipe.procedure:
        lpcdr.append([i])
      newrec = builder.get_object("dlgRecipe")
      response = newrec.run()
      newrec.hide()
      if response == gtk.RESPONSE_OK:
        data = self.check_new_recipe(widget, builder)
        if data:
          return data
      elif response == gtk.RESPONSE_CANCEL:
        return "Cancel"
      return False

  def refreshRecipes(self, builder, recipes):
    rlist = builder.get_object("liststore")
    ilist = builder.get_object("liststoreRecipes")
    rlist.clear()
    ilist.clear()
    for rcp in recipes:
      rlist.append([rcp.name, rcp.category])
      ilist.append([rcp.name])
    treemodelsort = gtk.TreeModelSort(ilist)
    treemodelsort.set_sort_column_id(0,gtk.SORT_ASCENDING)
    #There is no combobox of recipes to sort at the moment,  maybe in thu future.
    #combobox = builder.get_object("cboxentryrcp")
    #combobox.get_model().set_sort_column_id(0,gtk.SORT_ASCENDING)
    #combobox.set_model(treemodelsort)

  def showError(self, builder, message):
    error = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,buttons=gtk.BUTTONS_OK, message_format="ERROR\n\n "+message)
    if error.run() == gtk.RESPONSE_OK:
       error.hide()

  def showRecipe(self, builder, recipe):
    builder.get_object("txtname").set_text(recipe.name)
    builder.get_object("txtyields").set_text(str(recipe.yields[0] + " " + recipe.yields[1]))
    tags = ""
    for i in recipe.tags:
      tags = tags + i + " "
    builder.get_object("txttags").set_text(tags)
    if recipe.image != "None":
      try:
        builder.get_object("image1").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(recipe.image))
      except:
        builder.get_object("image1").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("images/default.jpg"))
        print "Error: Image: "+ recipe.image + " not found"
    else:
      builder.get_object("image1").set_from_pixbuf(gtk.gdk.pixbuf_new_from_file("images/default.jpg"))
    lstingredients = builder.get_object("listingredients")
    lstingredients.clear()
    for row in recipe.ingredients:
      lstingredients.append(row)
    lstprocedure = builder.get_object("liststore1")
    lstprocedure.clear()
    for i in recipe.procedure:
      lstprocedure.append([i])

  def get_active_text(self, combobox):
    model = combobox.get_model()
    active = combobox.get_active()
    if active < 0:
      return None
    return model[active][0]

  def get_column_data(self, liststore, col):
    iter = liststore.get_iter_root()
    result = []
    while (iter):
      elem = liststore.get_value(iter, col)
      result.append(elem)
      iter = liststore.iter_next(iter)
    return result

  def get_array_data(self, liststore, builder, treeview):
    iter = liststore.get_iter_root()
    result = list()
    while iter:
      row = []
      for i in range(builder.get_object(treeview).get_model().get_n_columns()):
        row.append(liststore.get_value(iter, i))
      result.append(row)
      iter = liststore.iter_next(iter)
    return result

  def get_selected_row(self, builder, treeview, alert=False):
    row, iter = treeview.get_selection().get_selected()
    if iter is None:
      if alert:
        self.showError(builder, "No row selected.")
        return None, None
    else:
      return row, iter

  def clear_recipe_dialog(self, widget, builder):
    builder.get_object("entryname").set_text("")
    builder.get_object("cboxcategory").set_active(11)
    builder.get_object("spinbutton1").set_value(0.0)
    builder.get_object("combobox1").set_active(0)
    builder.get_object("chkfast").set_active(False)
    builder.get_object("chkappetizer").set_active(False)
    builder.get_object("chklowcalories").set_active(False)
    builder.get_object("chkevents").set_active(False)
    builder.get_object("chkvegetarian").set_active(False)
    builder.get_object("chkinternational").set_active(False)
    builder.get_object("chkbirthday").set_active(False)
    builder.get_object("chkfittings").set_active(False)
    builder.get_object("nlistingredients").clear()
    builder.get_object("nlistprocedures").clear()

  def clear_ingredient_dialog(self, builder):
    builder.get_object("ingentryname").set_text("")
    builder.get_object("comboboxtype").set_active(0)
    builder.get_object("comboboxgroup").set_active(0)
    builder.get_object("combobox3").set_active(0)
    builder.get_object("combobox2").set_active(0)
    builder.get_object("spinbutton2").set_value(0.0)
    builder.get_object("listequivalence").clear()

  def configureIngredients(self,  builder, ingredients, dlging):
    lstings = builder.get_object("liststoreIngredients")
    self.refreshIngredients(builder, ingredients)
    response = dlging.run()
    return response

  def configureRecipes(self,  builder, recipes, dlgrcp):
    lstings = builder.get_object("liststoreIngredients")
    self.refreshRecipes(builder, recipes)
    response = dlgrcp.run()
    return response

  def check_new_ingredient(self, builder):
    name = builder.get_object("ingentryname").get_text()
    if not name:
      self.showError(builder, "Name must not be empty.")
      return False
    type = self.get_active_text(builder.get_object("comboboxtype"))
    if not type:
      self.showError(builder, "Type must not be empty.")
      return False
    group =  self.get_active_text(builder.get_object("comboboxgroup"))
    if not group:
      self.showError(builder, "Group must not be empty.")
      return False
    measure =  self.get_active_text(builder.get_object("combobox3"))
    if not measure:
      self.showError(builder, "Measure must not be empty.")
      return False
    equivalents = self.get_array_data(builder.get_object("listequivalence"), builder, "treeview8")
    return [name,  type,  group,  measure,  list(equivalents),  [],  []]

  def newIngredient(self, builder):
    self.clear_ingredient_dialog(builder)
    dlgIngredient = builder.get_object("dlgIngredient")
    action = dlgIngredient.run()
    dlgIngredient.hide()
    if action == gtk.RESPONSE_OK:
      data = self.check_new_ingredient(builder)
      if data:
        return data
    elif action == gtk.RESPONSE_CANCEL:
      return "Cancel"

  def modifyIngredient(self,  builder,  ingredient):
    dgroup = { 'Bread and Cereals' : 0, 'Drinks': 1, 'Fats and Oils' : 2, 'Fruits and vegetables' : 3, 'Meats and eggs' : 4, 'Milky' : 5, 'Minerals, Nutrients' : 6 }
    dtype = {'Liquid' : 0,  'Solid' : 1 }
    dmeasure = {'Kilos' : 0,  'Liters' : 1,  'Units' : 2 }
    self.clear_ingredient_dialog(builder)
    builder.get_object("ingentryname").set_text(ingredient.name)
    builder.get_object("comboboxgroup").set_active(dgroup[ingredient.group])
    builder.get_object("comboboxtype").set_active(dtype[ingredient.type])
    builder.get_object("comboboxtype").set_active(dmeasure[ingredient.measure])
    lstorequiv =  builder.get_object("listequivalence")
    for eqiv in ingredient.equivalents:
      lstorequiv.append(eqiv)
    dlgIngredient = builder.get_object("dlgIngredient")
    action = dlgIngredient.run()
    dlgIngredient.hide()
    if action == gtk.RESPONSE_OK:
      data = self.check_new_ingredient(builder)
      if data:
       return data
    elif action == gtk.RESPONSE_CANCEL:
      return "Cancel"

  def delIngredient(self, builder):
    row,  iter = self.get_selected_row(builder, builder.get_object("treeview7"), True)
    if iter:
      name = row.get_value(iter, 0)
      row.remove(iter)
      return name
    return None

  def delRecipe(self, builder):
    row,  iter = self.get_selected_row(builder, builder.get_object("treeview11"), True)
    if iter:
      name = row.get_value(iter, 0)
      row.remove(iter)
      return name
    return None

  def addMeasure(self,  builder):
    value = builder.get_object("adjustment2").get_value()
    unit = self.get_active_text(builder.get_object("combobox2"))
    equivalents = builder.get_object("listequivalence")
    equivalents.append([unit,  value])

  def delMeasure(self, builder):
    row,  iter = self.get_selected_row(builder, builder.get_object("treeview8"), True)
    if iter:
      row.remove(iter)

  def refreshIngredients(self, builder, ingredients):
    ilist = builder.get_object("liststoreIngredients")
    ilist.clear()
    for ing in ingredients:
      ilist.append([ing.name])
    treemodelsort = gtk.TreeModelSort(ilist)
    treemodelsort.set_sort_column_id(0,gtk.SORT_ASCENDING)
    combobox = builder.get_object("cboxentrying")
    combobox.get_model().set_sort_column_id(0,gtk.SORT_ASCENDING)

  def clearMenu(self, builder):
    listlunch = builder.get_object("listlunch")
    listlunch.clear()
    listdinner = builder.get_object("listdinner")
    listdinner.clear()
    for i in range(7):
      builder.get_object("listlunch").append(None)
      builder.get_object("listdinner").append(None)

  def getMenu(self, builder):
    menu = list()
    menu.append(self.get_column_data(builder.get_object("listlunch"), 0))
    menu.append(self.get_column_data(builder.get_object("listdinner"), 0))
    return menu

  def loadMenu(self, builder, data):
    menu = eval(data[0])
    lunchs = menu[0]
    dinners = menu[1]
    listlunch = builder.get_object("listlunch")
    listlunch.clear()
    listdinner = builder.get_object("listdinner")
    listdinner.clear()
    for i in range(7):
      listlunch.append([lunchs[i]])
      listdinner.append([dinners[i]])

  def includeIngredients(self,  builder):
    dlg = builder.get_object("dlgYesNo")
    action = dlg.run()
    dlg.hide()
    if action == gtk.RESPONSE_OK:
      return True
    else:
      return False

  def listToValues(self, thelist):
    result = ""
    for i in thelist:
      result = result + ", " + i
    return result[2:]
