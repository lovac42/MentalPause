# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/MentalPause 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt.qt import *
from anki.hooks import wrap
import anki.sched

from .utils import maxFuzzIvlRange


def daysLate(sched, card, _old):
    sel=sched.col.conf.get("mentalPause", Qt.Unchecked)

    if sel == Qt.Checked:
        return 0 # no bonus

    if sel == Qt.PartiallyChecked:
        late_by = _old(sched, card)
        cap = maxFuzzIvlRange(card.ivl)
        return max(0, min(cap, late_by))

    return _old(sched, card)


anki.sched.Scheduler._daysLate = wrap(anki.sched.Scheduler._daysLate, daysLate, 'around')
try:
    import anki.schedv2
    anki.schedv2.Scheduler._daysLate = wrap(anki.schedv2.Scheduler._daysLate, daysLate, 'around')
except ImportError: pass
