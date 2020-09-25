#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module for obliterating insert and delete tags from text.
"""

import re


def obliterate_ins_dels(text1: str) -> str:
    pointer = re.compile(r"(<ins.*?>)"
                         r"|(</ins>)"
                         r"|(<del.*?>)"
                         r"|(</del>)", re.S | re.I)

    text2 = pointer.sub("", text1)

    return text2
