from psycopg2.extras import DictCursor, NamedTupleCursor
from contextlib import closing
import psycopg2
import typing
from dataclasses import make_dataclass

postgres_data = {"user": "kiryssha", "password": "", "host": "", "dbname": "ruotvet"}


class Database:
    @staticmethod
    def _format_param(param: typing.Any):
        if type(param) == str:
            if param == "true":
                return f"'t'"
            elif param == "false":
                return f"'f'"
            else:
                return f"'{param}'"
        elif type(param) == int:
            return f"{param}"

    def _gen_sql(self, method: str, table: str, params: dict = None, args: tuple = None):
        params = [list(value) for value in params.items()]
        for param in params:
            if type(param[1]) == bool:
                if param[1] == True:
                    param[1] = "true"
                elif param[1] == False:
                    param[1] = "false"
        if method == "insert":
            sql = f"INSERT INTO {table} ("
            for param in params:
                sql += f"{param[0]}"
                if param[1] != params[-1][1]:
                    sql += ", "
            sql += ") VALUES ("
            for param in params:
                sql += self._format_param(param[1])
                if param[1] != params[-1][1]:
                    sql += ", "
            return sql + ") RETURNING *"
        elif method == "select":
            sql = f"SELECT * FROM {table}"
            if params:
                sql += " WHERE ("
                for param in params:
                    sql += f"{param[0]} = {self._format_param(param[1])}"
                    if param[1] != params[-1][1]:
                        sql += "and "
                return sql + ")"
            else:
                return sql
        elif method == "update":
            sql = f"UPDATE {table} SET {args[0]} = {self._format_param(args[1])}"
            if params:
                sql += " WHERE ("
                for param in params:
                    sql += f"{param[0]} = {self._format_param(param[1])}"
                    if param[1] != params[-1][1]:
                        sql += "and "
                sql += ")"
            return sql + " RETURNING *"
        elif method == "delete":
            sql = f"DELETE FROM {table} WHERE ("
            for param in params:
                sql += f"{param[0]} = {self._format_param(param[1])}"
                if param[1] != params[-1][1]:
                    sql += "and "
            return sql + ")"

    def insert(self, table: str, **kwargs: typing.Optional[str or int]) -> typing.List[NamedTupleCursor]:
        """
        :param table: The database table.
        :param kwargs: All args are values, that should be inserted.
        :return: The database row.
        """
        with closing(psycopg2.connect(**postgres_data)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(self._gen_sql("insert", table, kwargs))
                connection.commit()
                return [value for value in cursor]

    def select(self, table: str, **kwargs: typing.Optional[str or int]) -> list:
        """
        :param table: The database table, that already exists.
        :param kwargs: All args is select values.
        :return: The database row.
        """
        with closing(psycopg2.connect(**postgres_data)) as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(self._gen_sql("select", table, kwargs))
                connection.commit()
                values, new_values = [value for value in cursor], []
                for value in values:
                    new_value = {}
                    for sub_value, sub_value_key in zip(value, value.keys()):
                        if sub_value == "t":
                            new_value.update({sub_value_key: True})
                        elif sub_value == "f":
                            new_value.update({sub_value_key: False})
                        else:
                            new_value.update({sub_value_key: sub_value})
                    data_row = make_dataclass("Record", list(value.keys()))
                    new_values.append(data_row(**new_value))
                return new_values

    def update(self, *args, table: str, **kwargs: typing.Optional[str or int]) -> typing.List[NamedTupleCursor]:
        """
        :param table: The database table.
        :param kwargs: The first arg, is the value, that you set in. The second – the select value.
        :return: The database row.
        """
        with closing(psycopg2.connect(**postgres_data)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(self._gen_sql("update", table, kwargs, args=args))
                connection.commit()
                return [value for value in cursor]

    def delete(self, table: str, **kwargs: typing.Optional[str or int]) -> bool:
        """
        :param table: The database table.
        :param kwargs: All args is select values.
        :return: Boolean. True if deleted success.
        """
        with closing(psycopg2.connect(**postgres_data)) as connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(self._gen_sql("delete", table, kwargs))
                connection.commit()
                return True
