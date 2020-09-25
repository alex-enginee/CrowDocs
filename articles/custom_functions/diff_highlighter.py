#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
module for obliterating script tags from text.
"""

import difflib
import re

from django.utils import timezone


def highlight_diff(
        old_text: str,
        new_text: str,
        user_updater="admin",
        date_updated=timezone.now()
) -> str:

    diff_sequence = difflib.SequenceMatcher(None, old_text, new_text)

    tooltip_text = f"updated by {user_updater}, " \
                   f"at {date_updated.strftime(format='%H:%M %d.%m.%Y')}"

    ins_tag = "ins"
    del_tag = "del"
    class_name = "tooltip"

    start_ins = f"<{ins_tag} class='{class_name}' data-title='{tooltip_text}'>"
    end_ins = f"</{ins_tag}>"
    start_del = f"<{del_tag} class='{class_name}' data-title='{tooltip_text}'>"
    end_del = f"</{del_tag}>"

    any_tag = re.compile(r"(<[^<>]*?>)", re.S | re.I)

    def surround(elem):
        if any_tag.match(elem):
            return elem
        elif elem and elem not in " \n\t":
            return f"{start_ins}{elem}{end_ins}"
        else:
            return ""

    output = ""
    for opcode, a0, a1, b0, b1 in diff_sequence.get_opcodes():
        # print(opcode, a0, a1, b0, b1)
        if opcode == 'equal':
            output += old_text[a0:a1]
        # elif opcode == 'delete':
        #     output += old_text[a0:a1]
        elif opcode == 'replace':
            text_list = any_tag.split(new_text[b0:b1])
            mark_text_list = list(map(surround, text_list))
            output += "".join(mark_text_list)
        elif opcode == 'insert':
            text_list = any_tag.split(new_text[b0:b1])
            mark_text_list = list(map(surround, text_list))
            output += "".join(mark_text_list)

    return output
