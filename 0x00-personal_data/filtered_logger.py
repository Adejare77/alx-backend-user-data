#!/usr/bin/env python3
"""Regex-ing"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated

    Args:
        fields (list): a list of strings representing all fields to obfuscate
        redaction (str): a string representing by what the field will
        be obfuscated
        message (str): a string representing the log
        separator (str): a string representing by which character is separating
        all fields in the log line(message)
    """
    for field in fields:
        pattern = rf'(?<={field}=)[^{separator}]+'
        message = re.sub(pattern, redaction, message)
    return message
