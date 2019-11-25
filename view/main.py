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

#!/usr/bin/env python
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

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QKeySequence


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('view/main.ui', self)
        self.buttonsMethods()
        self.show()

    def openWindow(self):
        app = QtWidgets.QApplication(sys.argv)
        window = Ui()
        app.exec_()
        self.buttonsMethods(self)

    def buttonsMethods(self):
        pass
        
    def newIngredient(self):
        print("Creating new ingredient")
