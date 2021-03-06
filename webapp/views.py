import json
from uuid import uuid4

from django.http import HttpResponse, HttpRequest
import os

from django.shortcuts import render

from account.account import Account
from database.database import ObjectNotFound
# from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.sqlite3 import AccountDatabaseSQLlite3
from database.implementations.ram import AccountDatabaseRAM

connection_str = "db.sqlite3"
database = AccountDatabaseSQLlite3(connection=connection_str)


def accounts_list(request: HttpRequest) -> HttpResponse:
    pass


def index(request: HttpRequest) -> HttpResponse:
    tmp = database.get_objects()
    return render(request, "index.html", context={"accounts": tmp})


def create_account(request: HttpRequest) -> HttpResponse:
    return render(request, "create_account.html")


def accounts(request: HttpRequest) -> HttpResponse:
    # tmp = database.get_objects()

    # if request.method == "GET":
    #     json_obj = [account.to_json() for account in tmp]
    #     return HttpResponse(content=json.dumps(json_obj))

    try:
        account = Account.from_json_str(request.body.decode("utf8"))
        account.id_ = uuid4()
        try:
            database.get_object(account.id_)
            return HttpResponse(content=f"Error: object already exists, use PUT to update", status=400)
        except ObjectNotFound:
            database.save(account)
            return HttpResponse(content=account.to_json_str(), status=201)
    except Exception as e:
        return HttpResponse(content=f"Error: {e}", status=400)

    # if request.method == "PUT":
    #     try:
    #         account = Account.from_json_str(request.body.decode("utf8"))
    #         database.get_object(account.id_)
    #         database.save(account)
    #         return HttpResponse(content="OK", status=200)
    #     except Exception as e:
    #         return HttpResponse(content=f"Error: {e}", status=400)
