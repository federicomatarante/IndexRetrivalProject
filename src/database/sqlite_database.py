import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection, Cursor
from typing import Optional, List


class Script:
    _queries = []
    _connection: Connection

    def __init__(self, connection: Connection):
        self._connection = connection

    def insertOne(self, table: str, item: dict[str, any]):
        """
        Inserts a record into a table.
        :param table: str. The table's name.
        :param item: dict[str,any]. The items in the record. The key-value is in the format of attributeName-value, for example age-32
        """
        keys_string = ", ".join([key.replace("'", "''") for key in item.keys()])
        values = [value.replace("'", "''") if type(value) == str else value for value in item.values()]
        values_string = ", ".join([f"'{item}'" if type(item) == str else str(item) for item in values])
        query = f'INSERT INTO {table} ({keys_string}) VALUES ({values_string});'
        self._queries.append(query)

    def delete(self, table: str, where: str):
        """
        Deletes records from the table.
        :param table: the table where the records will be deleted.
        :param where: the condition's query.
        """
        query = f"DELETE FROM {table} WHERE {where};"
        self._queries.append(query)

    def commit(self):
        cursor: Cursor = self._connection.cursor()
        scripts: list[str] = []
        for i in range(0, len(self._queries), 25):
            scripts.append('\n'.join(self._queries[i:i + 25]))
        print(scripts)
        try:
            for script in scripts:
                cursor.executescript(script)
            self._connection.commit()
        finally:
            cursor.close()
        self._queries = []


@dataclass
class TableSchema:
    """
    It describes the basic information of a SQL table.
    @:param name: str. The table's name.
    @:param attributes: dict[str,str]. A dict of attributes. The key-value pair contains information in the form of name-description, for example 'firstName-TEXT PRIMARY KEY'
    @:param slope: it's the post-attributes information, such as other constraints, for example 'CONSTRAINT firstName>2'
    """
    name: str
    attributes: dict[str, str] = None
    slope: list[str] = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
        if self.slope is None:
            self.slope = []

    @property
    def creationQuery(self) -> str:
        """
        :return: str. The table's creation query.
        """
        table_details = [name + ' ' + details for name, details in self.attributes.items()]
        table_details.extend(self.slope)
        return f"CREATE TABLE {self.name} ({', '.join(table_details)});"


class SQLiteView:
    _file: str
    _connection: Optional[Connection] = None
    _schemas: list[TableSchema]

    """
    A class that offers an abstract view for a SQLite database with the basic operations and functionalities.
    """

    def __init__(self, file: str, schemas: list[TableSchema]):
        """
        :param file:  the database's path.
        :param schemas: a list of table schemas that the database will contain.
        """
        self._file = file
        self._schemas = schemas

    def isConnected(self) -> bool:
        """
        :return: bool. If the database is connected.
        """
        return self._connection is not None

    def connect(self):
        """
        Connects to the database.
        """
        if self._connection is None:
            self._connection = sqlite3.connect(self._file)

    def disconnect(self):
        """
        Disconnects from the database.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def createTables(self):
        """
        Creates the tables given in the constructor as Table Schemas.
        """
        if self._connection is None:
            self._connectionError()
        cursor: Cursor = self._connection.cursor()
        try:
            for schema in self._schemas:
                cursor.execute(schema.creationQuery)
            self._connection.commit()
        finally:
            cursor.close()

    def doTablesExist(self) -> bool:
        """
        :return: bool. If the tables given in the constructor as Table Schemas exist.
        """
        if self._connection is None:
            self._connectionError()
        cursor: Cursor = self._connection.cursor()
        try:
            for schema in self._schemas:
                cursor.execute(f"SELECT 1 FROM sqlite_master  WHERE type ='table' AND name='{schema.name}'")
                self._connection.commit()
                if cursor.fetchone() is None:
                    return False
            return True
        finally:
            cursor.close()

    def dropTables(self):
        """
        Deletes the tables given in the constructor from the database.
        """
        if self._connection is None:
            self._connectionError()
        cursor: Cursor = self._connection.cursor()
        try:
            table_names = [schema.name for schema in self._schemas]
            for name in table_names:
                cursor.execute(f"DROP TABLE IF EXISTS {name};")
            self._connection.commit()
        finally:
            cursor.close()

    def insertOne(self, table: str, item: dict[str, any]):
        """
        Inserts a record into a table.
        :param table: str. The table's name.
        :param item: dict[str,any]. The items in the record. The key-value is in the format of attributeName-value, for example age-32
        """
        if self._connection is None:
            self._connectionError()
        cursor: Cursor = self._connection.cursor()
        try:
            keys_string = ", ".join([key.replace("'", "''") for key in item.keys()])
            values = [value.replace("'", "''") if type(value) == str else value for value in item.values()]
            values_string = ", ".join([f"'{item}'" if type(item) == str else str(item) for item in values])
            cursor.execute(f'INSERT INTO {table} ({keys_string}) VALUES ({values_string});')
            self._connection.commit()
        finally:
            cursor.close()

    def delete(self, table: str, where: str):
        """
        Deletes records from the table.
        :param table: the table where the records will be deleted.
        :param where: the condition's query.
        """
        if self._connection is None:
            self._connectionError()
        cursor: Cursor = self._connection.cursor()
        try:
            cursor.execute(f"DELETE FROM {table} WHERE {where};")
            self._connection.commit()
        finally:
            cursor.close()

    def select(self, table, attributes: list[str], where: str = None) -> list[dict[str, any]]:
        """
        Selects records from the table.
        :param table: the table where the records will be selected.
        :param attributes: the attributes to be selected.
        :param where: the condition's query.
        :return list[dict[str,any]]. A list of dictionary containing dicitonaries key-value in the format attribute-value.
        """
        if self._connection is None:
            self._connectionError()
        cursor: Cursor = self._connection.cursor()
        try:
            query = f"SELECT {', '.join(attributes)} FROM {table}"
            if where is not None:
                query = query + f" WHERE {where}"
            query = query + ";"
            cursor.execute(query)
            self._connection.commit()
            result_sets = cursor.fetchall()
            return [{attributes[index]: result for index, result in enumerate(result_set)}
                    for result_set in result_sets]
        finally:
            cursor.close()

    def createScript(self) -> Script:
        """
        :return: Script. An object to create complex scripts to be executed in a single commit.
        """
        if self._connection is None:
            self._connectionError()
        return Script(self._connection)

    def _connectionError(self):
        raise ConnectionError("The database is not connected!")
