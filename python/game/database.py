#!/usr/bin/env python3
import logging
from logging.handlers import RotatingFileHandler
from sqlite3 import Connection
from typing import List, Tuple

log = logging.getLogger(__name__)
handler = RotatingFileHandler("{}.log".format(__name__), maxBytes=1280000, backupCount=1)
handler.setFormatter(logging.Formatter("[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s"))
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class Database(Connection):
    FILE = "game/scores.db"

    def __init__(self):
        # if does not exist, format / create tables
        super().__init__(self.FILE)
        self.cur = self.cursor()
        # TODO? have a single table with a True/False flag for successful attempts
        # TODO The TIME is the number on the clock when the game ended in success or failure
        # TODO KEEP track of the entire game configuration of each attempt
        # TODO have functions to change and get the current configuration

        self.execute(
            """
            CREATE TABLE IF NOT EXISTS SUCCESSES (
                 ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                 NAME VARCHAR NOT NULL,
                 TIME INT NOT NULL
            )
            """
        )
        self.execute(
            """
            CREATE TABLE IF NOT EXISTS FAILURES (
                 COUNT INTEGER PRIMARY KEY AUTOINCREMENT ,
                 DURATION INT NOT NULL
            )
            """
        )
        self.commit()

    def __del__(self):
        log.debug("Closing connection to database")
        self.close()

    def __str__(self):
        return """Solves:\n{}\n\nTotal Failures: {}
        """.format(
            "\n".join(str(x) for x in self.get_scores()),
            len(self.get_attempts())
        )

    def execute(self, *args, **kwargs):
        log.debug("SQLITE:{}".format(" ".join([str(x) for x in args])))
        return self.cur.execute(*args, **kwargs)

    def add_attempt(self, duration: int):
        """
        Only add failed attempts to this table
        :param duration: The duration of the failed attempt
        :return:
        """
        self.execute("INSERT INTO FAILURES (DURATION) VALUES (?)", (duration,))

    def get_attempts(self) -> List[int]:
        """
        :return: A list of all the failed attempt durations
        """
        self.execute(
            "SELECT  * FROM FAILURES"
        )
        return [x[1] for x in self.cur.fetchall()]

    def get_scores(self) -> List[Tuple[str, int]]:
        """
        :return: Scores from the database sorted from fastest to slowest
        """
        self.execute(
            "SELECT  * FROM SUCCESSES"
        )
        return [(x[1], x[2]) for x in sorted(self.cur.fetchall(), key=lambda x: x[1])]

    def add_score(self, name: str, time: int):
        """
        Insert a single record into the success table
        :param name:
        :param time:
        :return:
        """
        log.debug("Name: {}  Time: {}".format(name, time))
        self.execute("INSERT INTO SUCCESSES (NAME,TIME) VALUES (?,?);", (name, time))
        self.commit()
