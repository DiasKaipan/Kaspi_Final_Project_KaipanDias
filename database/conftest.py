from typing import Type, Any

import pytest

from database.database import AccountDatabase
from database.implementations.sqlite3 import AccountDatabaseSQLlite3


@pytest.fixture()
def connection_string_PGSQL(request: Any) -> str:
    return "dbname=defaultdb port=25060 user=doadmin password=e5Y6G88wWs0EGS5e host=db-postgresql-nyc3-99638-do-user-4060406-0.b.db.ondigitalocean.com"


@pytest.fixture()
def connection_string_sqlite3(request: Any) -> str:
    return "db.sqlite3"


@pytest.fixture(params=[AccountDatabaseSQLlite3])
def database_implementation(request: Any) -> Type[AccountDatabase]:
    implementation = request.param
    return implementation


@pytest.fixture()
def database_connected(
        request: Any,
        database_implementation: Type[AccountDatabase],
        connection_string_sqlite3: str,
) -> AccountDatabaseSQLlite3:

    return AccountDatabaseSQLlite3(connection=connection_string_sqlite3)
