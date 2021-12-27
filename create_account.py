import sys
from decimal import Decimal
from uuid import uuid4

from account.account import Account
from database.database import AccountDatabase
from database.implementations.sqlite3 import AccountDatabaseSQLlite3
import os

from database.implementations.ram import AccountDatabaseRAM


def create_account(database: AccountDatabaseSQLlite3, currency: str, balance: Decimal) -> None:
    account = Account(
        id_=uuid4(),
        currency=currency,
        balance=balance,
    )
    database.save(account)


if __name__ == "__main__":

    connection_str = "db.sqlite3"
    database = AccountDatabaseSQLlite3(connection=connection_str)
    print("Connected!")

    currency = input("Enter Currency: ")
    balance = Decimal(input("Enter balance: "))
    create_account(database=database, balance=balance, currency=currency)
    sys.exit(0)
