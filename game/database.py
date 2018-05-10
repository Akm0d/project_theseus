#!/usr/bin/env python3
import logging
from logging.handlers import RotatingFileHandler
from os import path
from sqlite3 import Connection
from typing import List
try:
    from game.constants import TIME_GIVEN
except ModuleNotFoundError:
    from constants import TIME_GIVEN

log = logging.getLogger(__name__)


class Row(dict):
    """
    An object representing a single row from the database
    """
    code = None
    color = None
    id = None
    lasers = None
    name = None
    time = None
    success = None

    def __init__(self, key: int = None, name=None, lasers: bin = None, code: hex = None, color: str = None,
                 time: int = None, success: bool = None):
        dict.__init__(self)
        self["name"] = name
        self["lasers"] = lasers
        self["code"] = code
        self["color"] = color
        self["time"] = time
        self["success"] = success
        # Add dict values to namespace
        self.__dict__.update(self)

    def __str__(self):
        return "{id}, {name}, {lasers}, {code}, {color}, {time}, {success}".format(
            id=self.id, name=self.name, lasers=bin(self.lasers),
            code=hex(int("0x" + str(self.code), 16)), color=self.color, time=self.time, success=bool(self.success)
        )


class Database(Connection):
    FILE = path.dirname(__file__) + "/scores.db"

    def __init__(self):
        # if does not exist, format / create tables
        Connection.__init__(self, self.FILE)
        self.cur = self.cursor()

        # The TIME is the number on the clock when the game ended in success or failure
        self._execute(
            """
            CREATE TABLE IF NOT EXISTS DATA (
                 ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                 NAME VARCHAR,
                 LASERS INT NOT NULL,
                 CODE INT NOT NULL,
                 COLOR VARCHAR NOT NULL,
                 TIME INT NOT NULL,
                 SUCCESS BOOL NOT NULL
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
            "\n".join(str(x) for x in self.get_rows(success=True)),
            len(self.get_rows(success=False))
        )

    def _execute(self, *args, **kwargs):
        log.debug("SQLITE:{}".format(" ".join([str(x) for x in args])))
        return self.cur.execute(*args, **kwargs)

    def add_row(self, item: Row):
        """
        Append a row to the database
        :param item: a Row object
        """
        # Brief Error checking for columns that cannot be null
        if item.time is None:
            item.time = TIME_GIVEN
        if item.success is None:
            item.success = False

        self._execute("INSERT INTO DATA (NAME, LASERS, CODE, COLOR, TIME, SUCCESS) VALUES (?, ?, ?, ?, ?, ?)", (
            item.name, item.lasers, item.code, item.color, item.time, item.success,))
        self.commit()

    @property
    def last(self) -> Row:
        """
        :return: A row object representing the last row in the database
        """
        self._execute("SELECT * FROM DATA WHERE ID = (SELECT max(ID) FROM DATA)")
        return Row(*self.cur.fetchone())

    @last.setter
    def last(self, item: Row):
        """
        # Modify the last row of the database to contain the values that aren't None
        """
        for column, value in item.items():
            if value is not None:
                log.info("Setting last row's {} to '{}'".format(column, value))
                self._execute("UPDATE DATA SET {col} = {q}{val}{q} WHERE ID = (SELECT MAX(ID) FROM DATA)".format(
                    col=column.upper(), val=value, q="'" if isinstance(value, str) else ""
                ))
            self.commit()

    def get_rows(self, lasers: int = None, code: hex = None, color: str = None, name: str = None, time: int = None,
                 success: bool = None) -> List[Row]:
        """
        Select rows based on columns.  If 'None' is given, then all rows will be selected.
        :param lasers: Select rows with this laser configuration
        :param code: Select rows with the same code
        :param color: Select rows with the same color color
        :param name: Select rows with the same name
        :param time: Select rows with a time equal to or less than the given number
        :param success: Select rows with success or failure
        :return: A list of rows
        """
        self._execute("SELECT * FROM DATA")
        result = [Row(*x) for x in self.cur.fetchall()]
        if name is not None:
            result = [x for x in result if x.name == name]
            # result = result where name is equal to value given
        if lasers is not None:
            result = [x for x in result if x.lasers == lasers]
            # result = result where lasers is equal to value given
        if code is not None:
            result = [x for x in result if x.code == code]
            # result = result where code is equal to value given
        if color is not None:
            result = [x for x in result if x.color == color]
            # result = result where color is equal to value given
        if time is not None:
            result = [x for x in result if x.time == time]
            # result = result where time is equal to value given
        if success is not None:
            result = [x for x in result if x.success == success]
            # result = result where success is equal to value given
        return result


if __name__ == "__main__":
    db = Database()

    if not db.get_rows():
        db.add_row(Row(name="ted", lasers=14, code=0x123, color="green", time=9, success=False))
        db.add_row(Row(name="bill", lasers=52, code=0x113, color="red", time=3, success=True))
        db.add_row(Row(name="jane", lasers=31, code=0x1a3, color="green", time=6, success=False))
        db.add_row(Row(name="zach", lasers=33, code=0x1f3, color="green", time=1, success=False))
        db.add_row(Row(name="tyler", lasers=52, code=0x1e3, color="blue", time=10, success=True))
        db.add_row(Row(name="graig", lasers=31, code=0x12a, color="red", time=7, success=False))
        db.add_row(Row(name="chris", lasers=86, code=0xb23, color="green", time=8, success=True))
        db.add_row(Row(name="clayton", lasers=46, code=0x1c3, color="red", time=11, success=True))
        db.add_row(Row(name="broderick", lasers=15, code=0x12d, color="blue", time=9, success=True))

    print("\n".join([str(x) for x in db.get_rows()]))
