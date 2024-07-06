#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List
import logging
import os
import mysql


PII_FIELD = ('name', 'email', 'phone', 'ssn', 'password')


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

    def __init__(self, fields: List[str]) -> None:
        # super(Child, self).__init__(self.FORMAT)
        super(RedactingFormatter, self).__init__(self.FORMAT)
        # super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ returns the log message obfuscated """
        # message = super().format(record)  # call Parent class's format Method
        message = super(RedactingFormatter, self).format(record)
        message = filter_datum(self.fields, self.REDACTION, message,
                               self.SEPARATOR)
        return message


def get_logger() -> logging.Logger:
    """ returns logging.Logger object """
    # create a logger instance
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # create a file handler
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELD)
    handler.setFormatter(formatter)

    # set the logger
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user, password=passwd,
                                   host=host, database=db_name)
    return conn


def main():
    """
    main entry point
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
