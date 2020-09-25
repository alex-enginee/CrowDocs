#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module for obliterating script tags from text.
"""

import re


def obliterate_scripts(text1: str) -> str:
    pointer = re.compile(r"(<script.*?>.*?<\/script>)"
                         r"|(<script.*?>)"
                         r"|(<iframe.*?>)"
                         r"|(<link.*?>)"
                         r"|(<object.*?>)"
                         r"|(<style.*?>.*?<\/style>)"
                         r"|(<[^><]*?javascript[^><]*?>)"
                         r"|(<[^><]*?expression[^><]*?>)", re.S | re.I)

    text2 = pointer.sub("", text1)

    return text2
