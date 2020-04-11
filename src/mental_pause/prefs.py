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

from .lib.com.lovac42.anki.gui import muffins
from .lib.com.lovac42.anki.gui.checkbox import TristateCheckbox


def setupUi(self, Preferences):
    groupbox = muffins.getMuffinsGroupbox(self, "Others")
    grid_layout = groupbox.layout()
    if not grid_layout:
        grid_layout = QGridLayout(groupbox)

    r = grid_layout.rowCount()
    self.mentalPause = TristateCheckbox(groupbox)
    self.mentalPause.setDescriptions({
        Qt.Unchecked:        "Mental Pause: This addon has been disabled",
        Qt.PartiallyChecked: "Mental Pause: Delay bonus is capped at max fuzz range",
        Qt.Checked:          "Mental Pause: Delay bonus has been eliminated",
    })
    grid_layout.addWidget(self.mentalPause, r, 0, 1, 3)


def load(self, mw):
    cb=self.mw.col.conf.get("mentalPause", Qt.Unchecked)
    self.form.mentalPause.setCheckState(cb)


def save(self):
    cb=self.form.mentalPause.checkState()
    self.mw.col.conf['mentalPause']=int(cb)


# Wrap Crap #################

aqt.forms.preferences.Ui_Preferences.setupUi = wrap(
    aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after"
)

aqt.preferences.Preferences.__init__ = wrap(
    aqt.preferences.Preferences.__init__, load, "after"
)

aqt.preferences.Preferences.accept = wrap(
    aqt.preferences.Preferences.accept, save, "before"
)
