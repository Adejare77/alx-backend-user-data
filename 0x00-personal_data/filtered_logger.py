#!/usr/bin/env python3
"""Regex-ing"""
from typing import List
import re
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the parent class with the format and
        fields to be redacted"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum.
        values for the fields should be filtered

        Args:
            record (logging.LogRecord): Incoming log record. Created using
            logging.LogRecord(...). Contains message, name etc needed

        Returns:
            str: obfuscated message
        """
        formatted_msg = super().format(record)
        obfuscated_msg = filter_datum(self.fields, self.REDACTION,
                                      formatted_msg, self.SEPARATOR)

        return obfuscated_msg
