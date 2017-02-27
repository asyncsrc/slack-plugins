#!/usr/bin/env python
from __future__ import print_function
from pylibs import slack, saltapi
import re


def get_id_for_alias(alias, minion, sql_server, database):

    sql_statement = "select id from dbo.xyz where Alias = '{}'".format(alias)

    cmd = "sqlcmd -S {} -d {} -W -Q \"{}\"".format(sql_server, database, sql_statement)
    status_code, salt_response = saltapi.execute(minion, "cmd.run", cmd)

    if status_code != 200:
        return True, "SQL query: {} failed against minion: {}.\nResponse: {}".format(cmd, minion, salt_response)

    if "0 rows affected" in salt_response:
        return True, "No matching ID found for specified alias: {}".format(alias)

    alias_guid = re.search(r"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})", salt_response)

    if alias_guid is not None:
        return False, alias_guid.groups(1)[0]
    return True, salt_response


def execute_query(minion, sql_server, database, sql_statement, **kwargs):
    cmd = "sqlcmd -S {} -d {} -W -Q \"{}\"".format(sql_server, database, sql_statement)
    status_code, salt_response = saltapi.execute(minion, "cmd.run", cmd)

    if status_code != 200:
        return True, "SQL query: {} failed against minion: {}.\nResponse: {}".format(cmd, minion, salt_response)

    if 'row_count' in kwargs:
        row_count = re.search(r"((\d+) rows affected)", salt_response)

        if row_count is not None:
            return False, int(row_count.groups(0)[1])
        else:
            return True, salt_response

    return False, salt_response


def export_query_to_csv(minion, sql_server, database, sql_statement, csv_path):

    cmd = "sqlcmd -S {} -d {} -W -Q \"{}\" -s\",\" -W -w 1024 -h 1 -o {}".format(sql_server,
                                                                                 database,
                                                                                 sql_statement,
                                                                                 csv_path)
    status_code, salt_response = saltapi.execute(minion, "cmd.run", cmd)

    if status_code != 200:
        return True, "SQL query: {} failed against minion: {}.\nResponse: {}".format(cmd, minion, salt_response)
