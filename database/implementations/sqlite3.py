from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from decimal import Decimal
from uuid import UUID, uuid4

import pandas as pd
from pandas import Series

from account.account import Account
from database.database import AccountDatabase, ObjectNotFound
import sqlite3


@dataclass
class AccountDatabaseSQLlite3(ABC):
    def __init__(self, connection, *args, **kwargs):
        self.conn = sqlite3.connect(connection, check_same_thread=False)
        cursor = self.conn.cursor()
        print("Database created and Successfully Connected to SQLLite")
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS accounts (
                            id varchar(255) primary key ,
                            currency VARCHAR,
                            balance DECIMAL
                        );
                        """)
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS transfers (
                            transaction_id varchar(255) primary key ,
                            account_from varchar(255)  ,
                            account_to varchar(255)  ,
                            currency VARCHAR,
                            amount DECIMAL
                            date DATETIME
                        );
                        """)
        self.conn.commit()

    def save(self, account: Account) -> None:
        print("I am going to save this:", account)
        return self._save(account=account)

    def close_connection(self):
        self.conn.close()

    def _save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()

        cur = self.conn.cursor()
        ex_str = 'UPDATE accounts SET currency = ?, balance = ? WHERE id = ?'
        values = [account.currency, int(account.balance), str(account.id_)]
        cur.execute(ex_str, values)

        rows_count = cur.rowcount
        self.conn.commit()

        print("ROWS COUNT", rows_count)
        if rows_count == 0:
            cur = self.conn.cursor()
            ex_str = 'INSERT INTO accounts (id, currency, balance) VALUES (?, ?, ?)'
            values = [str(account.id_), account.currency, int(account.balance)]
            cur.execute(ex_str, values)
            self.conn.commit()

    def clear_all(self) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM accounts;")
        self.conn.commit()

    def get_objects(self) -> List[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts;")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return [self.pandas_row_to_account(row) for index, row in df.iterrows()]

    @staticmethod
    def pandas_row_to_account(row: Series) -> Account:
        return Account(
            id_=UUID(row["id"]),
            currency=row["currency"],
            balance=Decimal(int(row["balance"])),
        )

    def get_object(self, id_: UUID) -> Optional[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE id = ?;", (str(id_),))
        print("Trying to find", str(id_))
        data = cur.fetchall()
        if len(data) == 0:
            raise ObjectNotFound("sqllite3: Object not found")
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return self.pandas_row_to_account(row=df.iloc[0])
