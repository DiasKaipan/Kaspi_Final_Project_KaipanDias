from typing import Type
from uuid import uuid4

import pytest

from account.account import Account
from database.database import ObjectNotFound, AccountDatabase
from database.implementations.sqlite3 import AccountDatabaseSQLlite3


class TestAllDatabases:
    def test_all_dbs(self, database_connected: AccountDatabase) -> None:
        database_connected.clear_all()
        account = Account.random()
        account2 = Account.random()
        database_connected.save(account)
        database_connected.save(account2)
        got_account = database_connected.get_object(account.id_)

        assert account == got_account

        with pytest.raises(ObjectNotFound):
            database_connected.get_object(uuid4())

        all_objects = database_connected.get_objects()
        assert len(all_objects) == 2
        for acc in all_objects:
            assert isinstance(acc, Account)

        account.currency = "BTC"
        database_connected.save(account)
        got_account = database_connected.get_object(account.id_)
        assert account == got_account

    def test_connection(self, connection_string_sqlite3: str) -> None:
        database = AccountDatabaseSQLlite3(connection=connection_string_sqlite3)
        database.save(Account.random())
        all_accounts = database.get_objects()
        database.close_connection()
