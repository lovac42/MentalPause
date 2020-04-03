# -*- coding: utf-8 -*-
# Copyright: (C) 2019-2020 Lovac42
# Support: https://github.com/lovac42/MentalPause 
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


def maxFuzzIvlRange(ivl):
    if ivl < 2:
        return 1
    elif ivl == 2:
        return 3
    elif ivl < 7:
        fuzz = int(ivl*0.25)
    elif ivl < 30:
        fuzz = max(2, int(ivl*0.15))
    else:
        fuzz = max(4, int(ivl*0.05))
    return max(fuzz, 1)
