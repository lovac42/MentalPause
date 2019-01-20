# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/MentalPause 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1

# == User Config =========================================

PARTIAL_CREDIT_DIVISOR = 2 # half credit

# == End Config ==========================================
##########################################################


from aqt import mw
from anki.hooks import wrap
import anki.sched

from anki import version
ANKI21 = version.startswith("2.1.")


def daysLate(sched, card, _old):
    sel=sched.col.conf.get("mentalPause",0)
    if not sel:
        return _old(sched,card)
    if sel==1:
        due=_old(sched,card)//PARTIAL_CREDIT_DIVISOR
        return max(0, int(due))
    return 0


anki.sched.Scheduler._daysLate = wrap(anki.sched.Scheduler._daysLate, daysLate, 'around')
if ANKI21:
    import anki.schedv2
    anki.schedv2.Scheduler._daysLate = wrap(anki.schedv2.Scheduler._daysLate, daysLate, 'around')


##################################################
#
#  GUI stuff, adds preference menu options
#
#################################################
import aqt
import aqt.preferences
from aqt.qt import *


if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


def setupUi(self, Preferences):
    try:
        grid=self.lrnStageGLayout
    except AttributeError:
        self.lrnStage=QtWidgets.QWidget()
        self.tabWidget.addTab(self.lrnStage, "Muffins")
        self.lrnStageGLayout=QtWidgets.QGridLayout()
        self.lrnStageVLayout=QtWidgets.QVBoxLayout(self.lrnStage)
        self.lrnStageVLayout.addLayout(self.lrnStageGLayout)
        spacerItem=QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.lrnStageVLayout.addItem(spacerItem)

    r=self.lrnStageGLayout.rowCount()
    self.mentalPause=QtWidgets.QCheckBox(self.lrnStage)
    self.mentalPause.setText(_('MentalPause: Disable Delay Bonus'))
    self.mentalPause.setTristate(True)
    self.lrnStageGLayout.addWidget(self.mentalPause, r, 0, 1, 3)
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
        txt='MentalPause: Partial Credits'
    else:
        txt='MentalPause: Disable Delay Bonus'
    self.mentalPause.setText(_(txt))


aqt.forms.preferences.Ui_Preferences.setupUi = wrap(aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after")
aqt.preferences.Preferences.__init__ = wrap(aqt.preferences.Preferences.__init__, load, "after")
aqt.preferences.Preferences.accept = wrap(aqt.preferences.Preferences.accept, save, "before")