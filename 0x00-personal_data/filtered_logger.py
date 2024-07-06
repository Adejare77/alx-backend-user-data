#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(fr'(?<={field}=)[^{separator}]+',
                         f'{redaction}', message)
    return message
