import sqlite3


class DB:
    conn: sqlite3.Connection | None = None

    @classmethod
    def connect(cls, *args, **kwargs) -> None:
        cls.conn = sqlite3.connect(*args, **kwargs)


class NotConnectedError(Exception):
    """Exception raised when there is no database connection."""

    def __init__(self, message="Database connection is not established"):
        self.message = message
        super().__init__(self.message)


def check_connection(func):
    """Decorator to check if the database connection is established."""

    def wrapper(*args, **kwargs):
        # Assuming the first argument is the instance ('self')
        if DB.conn is None:
            raise NotConnectedError()
        return func(*args, **kwargs)

    return wrapper


@check_connection
def insert_many(table_name: str, data: list[dict]):
    cursor = DB.conn.cursor()

    # Prepare INSERT INTO statement
    placeholders = ", ".join(["?"] * len(data[0]))
    columns = ", ".join(data[0].keys())
    sql = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        """

    # Prepare data tuples
    values_to_insert = [tuple(d.values()) for d in data]

    # Execute INSERT statement
    cursor.executemany(sql, values_to_insert)

    # Commit and close connection
    DB.conn.commit()


@check_connection
def execute_statements(statements):
    """
    Execute a list of SQL statements on the given SQLite database connection.

    :param connection: A sqlite3.Connection object
    :param statements: A statement or list of SQL statements to be executed
    """
    if isinstance(statements, str):
        statements = [statements]

    cursor = DB.conn.cursor()

    for statement in statements:
        try:
            cursor.execute(statement)
        except sqlite3.Error as e:
            print(f"An error occurred while executing the statement: {statement}")
            print(f"Error: {e}")

    DB.conn.commit()
    cursor.close()


@check_connection
def query(query: str, exactly_one: bool = False) -> list:
    """
    Execute a query and return exactly one row.

    :param connection: A sqlite3.Connection object.
    :param query: A SQL query string.
    :return: A single row from the query result.
    :raises ValueError: If the query results in more than one row.
    """
    cursor = DB.conn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()

    if exactly_one and len(rows) != 1:
        raise ValueError(f"Query did not return exactly one row: {rows}")

    return rows
