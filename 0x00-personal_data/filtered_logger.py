#!/usr/bin/env python3
""" Filter Logger Module """
import re
import os
from typing import List
import logging
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Obfuscates specified fields in log messages"""
    for field in fields:
        message = re.sub(
            rf"{field}=(.*?){re.escape(separator)}",
            f"{field}={redaction}{separator}",
            message,
        )
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize instances"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Formater"""
        msg = super().format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Createw and configures an instance"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> MySQLConnection:
    """Returns a connection to the database"""
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")
    db_username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")

    return mysql.connector.connect(
        host=db_host, database=db_name, user=db_username, password=db_password
    )


def main() -> None:
    """Main function"""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        field_names = [column[0] for column in cursor.description]

        logger = get_logger()

        for row in cursor:
            str_row = "".join(f"{f}={str(r)}; " for r, f in zip(row, field_names))
            logger.info(str_row.strip())

    db.close()


if __name__ == "__main__":
    main()
