# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/MentalPause 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from anki.cards import Card
from aqt import mw
from aqt.qt import *

from .utils import maxFuzzIvlRange


PARTIALLY_CHECKED = 1
CHECKED = 2

_card = None


def getCard():
    card = Card(mw.col)
    card.type = 2
    card.queue = 2
    card.factor = 2000
    card.reps = 5
    card.lapses = 1
    return card


def testDelay(ivl, delayed):
    global _card
    if not _card:
        _card = getCard()
    _card.due = mw.col.sched.today - delayed
    _card.ivl = ivl

    late = mw.col.sched._daysLate(_card)

    state = mw.col.conf.get("mentalPause", 0)
    if state == PARTIALLY_CHECKED:
        fuzz = maxFuzzIvlRange(ivl)
        assert late <= fuzz, 'Addon "MentalPause" self-tests failed, delay exceeds max fuzz.'
    elif state == CHECKED:
        assert late == 0, 'Addon "MentalPause" self-tests failed, delay was not zero.'
    else:
        assert late == delayed, 'Addon "MentalPause" self-tests failed, unexpected delay value.'
    # print("addon MentalPause tested fine.")




def onStartupSelfTest():
    "Runs tests on startup, but limited to current pref options."
    import random
    testDelay(
        random.randint(1,30),
        random.randint(1,100)
    )
    testDelay(
        random.randint(5,90),
        random.randint(50,200)
    )
    _card = None

# from anki.hooks import addHook
# addHook('profileLoaded', onStartupSelfTest)

