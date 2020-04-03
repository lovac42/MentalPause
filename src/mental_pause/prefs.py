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

if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


def setupUi(self, Preferences):
    grid_layout = muffins.getMuffinsTab(self)
    r = grid_layout.rowCount()
    self.mentalPause=QtWidgets.QCheckBox(self.lrnStage)
    self.mentalPause.setText(_('MentalPause: Disable Delay Bonus'))
    self.mentalPause.setTristate(True)
    grid_layout.addWidget(self.mentalPause, r, 0, 1, 3)
    self.mentalPause.clicked.connect(lambda:toggle(self))


def load(self, mw):
    qc = self.mw.col.conf
    cb=qc.get("mentalPause", 0)
    self.form.mentalPause.setCheckState(cb)
    toggle(self.form)


def save(self):
    toggle(self.form)
    qc = self.mw.col.conf
    qc['mentalPause']=self.form.mentalPause.checkState()


def toggle(self):
    checked=self.mentalPause.checkState()
    if checked==1:
        txt='MentalPause: Partial Credits (days_late/lapse)'
    else:
        txt='MentalPause: Disable Delay Bonus'
    self.mentalPause.setText(_(txt))


aqt.forms.preferences.Ui_Preferences.setupUi = wrap(aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after")
aqt.preferences.Preferences.__init__ = wrap(aqt.preferences.Preferences.__init__, load, "after")
aqt.preferences.Preferences.accept = wrap(aqt.preferences.Preferences.accept, save, "before")
