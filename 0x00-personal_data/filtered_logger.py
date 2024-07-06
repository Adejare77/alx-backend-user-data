#!/usr/bin/env python3
"""Regex-ing"""

import re


def filter_datum(fields, redaction, message, separator):
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(fr'(?<={field}=)[^;]+', f'{redaction}', message)
    return message
