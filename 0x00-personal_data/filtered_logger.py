#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(fr'(?<={field}=)[^{separator}]+',
                         f'{redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, *args, **kwargs):
        # super(Child, self).__init__(self.FORMAT)
        super(RedactingFormatter, self).__init__(self.FORMAT)
        # super().__init__(self.FORMAT)
        self.fields = kwargs.get('fields')

    def format(self, record: logging.LogRecord) -> str:
        """ returns the log message obfuscated """
        # message = super(RedactingFormatter, self).format(record)
        message = super().format(record)  # call Parent class's format Method
        message = filter_datum(self.fields, self.REDACTION, message,
                               self.SEPARATOR)
        return message
