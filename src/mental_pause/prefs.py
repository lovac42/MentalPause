# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/MentalPause 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import aqt
import aqt.preferences
from aqt import mw
from anki.hooks import wrap
from anki.lang import _
from aqt.qt import *

from .lib.com.lovac42.anki.version import ANKI21
from .lib.com.lovac42.anki.gui import muffins
from .lib.com.lovac42.anki.gui.checkbox import TristateCheckbox

if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


def setupUi(self, Preferences):
    grid_layout = muffins.getMuffinsTab(self)
    r = grid_layout.rowCount()
    self.mentalPause = TristateCheckbox(self.lrnStage)
    self.mentalPause.setDescriptions({
        Qt.Unchecked:        "Mental Pause: This addon has been disabled",
        Qt.PartiallyChecked: "Mental Pause: Delay bonus is capped at max fuzz range",
        Qt.Checked:          "Mental Pause: Delay bonus has been eliminated",
    })
    grid_layout.addWidget(self.mentalPause, r, 0, 1, 3)


def load(self, mw):
    cb=self.mw.col.conf.get("mentalPause", 0)
    self.form.mentalPause.setCheckState(cb)


def save(self):
    cb=self.form.mentalPause.checkState()
    self.mw.col.conf['mentalPause']=cb


aqt.forms.preferences.Ui_Preferences.setupUi = wrap(aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after")
aqt.preferences.Preferences.__init__ = wrap(aqt.preferences.Preferences.__init__, load, "after")
aqt.preferences.Preferences.accept = wrap(aqt.preferences.Preferences.accept, save, "before")
