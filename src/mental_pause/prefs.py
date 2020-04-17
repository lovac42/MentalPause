# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/MentalPause 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import random
import aqt
import aqt.preferences
from aqt import mw
from anki.hooks import wrap
from anki.lang import _
from aqt.qt import *
from aqt.utils import tooltip

from .lib.com.lovac42.anki.version import ANKI20
from .lib.com.lovac42.anki.gui import muffins
from .lib.com.lovac42.anki.gui.checkbox import TristateCheckbox

from .self_test import testDelay

if ANKI20:
    range = xrange


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
    self.mentalPause.clicked.connect(lambda:runTest(self))
    grid_layout.addWidget(self.mentalPause, r, 0, 1, 3)


def load(self, mw):
    cb=self.mw.col.conf.get("mentalPause", Qt.Unchecked)
    self.form.mentalPause.setCheckState(cb)


# This is not needed as onClick also saves the state.
# def save(self):
    # _saveState(self.form.mentalPause)


def _saveState(checkbox):
    state = checkbox.checkState()
    mw.col.conf["mentalPause"] = int(state)


def runTest(form):
    _saveState(form.mentalPause)
    for i in range(25):
        testDelay(
            ivl=random.randint(1,30),
            delayed=random.randint(1,60)
        )
        testDelay(
            ivl=random.randint(21,100),
            delayed=random.randint(30,200)
        )
    tooltip("MentalPause, self-test: OK", period=800)



# Wrap Crap #################

aqt.forms.preferences.Ui_Preferences.setupUi = wrap(
    aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after"
)

aqt.preferences.Preferences.__init__ = wrap(
    aqt.preferences.Preferences.__init__, load, "after"
)

# aqt.preferences.Preferences.accept = wrap(
    # aqt.preferences.Preferences.accept, save, "before"
# )
