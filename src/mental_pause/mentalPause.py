# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/MentalPause 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html



# == User Config =========================================

# Partial credit auto adjusted between 1-10 based on number of lapses.
MIN_CREDIT = 1
MAX_CREDIT = 10

# == End Config ==========================================
##########################################################


from aqt import mw
from anki.hooks import wrap
import anki.sched

from .lib.com.lovac42.anki.version import ANKI21


def daysLate(sched, card, _old):
    sel=sched.col.conf.get("mentalPause",0)

    if not sel:
        return _old(sched,card)

    if sel==1:
        div=min(MAX_CREDIT,max(MIN_CREDIT,card.lapses)) #1-10
        due=_old(sched,card)//div
        return max(0, int(due))

    return 0 #sel==2


anki.sched.Scheduler._daysLate = wrap(anki.sched.Scheduler._daysLate, daysLate, 'around')
if ANKI21:
    import anki.schedv2
    anki.schedv2.Scheduler._daysLate = wrap(anki.schedv2.Scheduler._daysLate, daysLate, 'around')

