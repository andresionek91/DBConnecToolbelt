#!/usr/bin/env python
# -*- coding: utf-8 -*-

import records
import psycopg2
from time import sleep
from sqlalchemy import create_engine
import pkg_resources
import os
import io
import dbconnectoolbelt.utils as utils


# Toolbelt to connect to postgres databases using different ORMs.
# Set up the following environmental variables before using:
# HOST
# DATABASE
# USER
# PASSWORD

class PostgreSQL:
    """
    Creates connections database.
    """
    def __init__(self):
        """
        takes env vars as parameters for connection to a postgres database
        """
        self.host = os.environ['HOST']
        self.dbname = os.environ['DATABASE']
        self.pwd = os.environ['PASSWORD']
        self.user = os.environ['USER']


    def psycopg2(self):
        """
        Connection object via psycopg2, for executing queries on database
        """
        while True:
            try:
                conn = psycopg2.connect("host={} dbname={} user={} password={} connect_timeout=5 "
                                        "options='-c statement_timeout=3000000'".format(self.host, self.dbname,
                                                                                        self.user, self.pwd))
                break
            except psycopg2.OperationalError:
                sleep(5)

        return conn

    def execute_sql(self, query):
        """
        Executes a sql command using a psycopg2 connection
        :param query: query string
        :return: none
        """
        conn = self.psycopg2()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()

    def records(self):
        """
        Connection object via records, for fetching records from database
        """
        while True:
            try:
                conn = records.Database("postgres://{}:{}@{}:5432/{}".format(self.user, self.pwd,
                                                                             self.host, self.dbname),
                                        connect_args={"options": "-c statement_timeout=3000000"})
                break
            except psycopg2.OperationalError:
                sleep(5)

        return conn

    def get_records_as_dict(self, query):
        """
        Executes a SQL command to fetch records from a database. Returns a list with records as dict.
        :param query: query string
        :return: records fetched as dict
        """
        conn = self.records()
        result = conn.query(query)

        return result.as_dict()

    def sqlalchemy(self):
        """
        Engine object via SQLAlchemy, for fetching records from database with pandas
        """
        return create_engine('postgresql://{}:{}@{}:5432/{}'.format(self.user, self.pwd, self.host, self.dbname))

    def df_to_sql(self, df, schema_name, table_name, if_exists='replace', sep='\t', encoding='utf8'):
        """
        Saves a pandas dataframe to a PostgreSQL table. For moderate/large amounts of data (+1k rows) it's much
        faster than the built-in method in pandas.
        :param df: dataframe to be uploaded
        :param schema_name: schema to upload
        :param table_name: table to upload
        :param if_exists: {‘fail’, ‘replace’, ‘append’}, default ‘replace’
            fail: Raise a ValueError.
            replace: Drop the table before inserting new values.
            append: Insert new values to the existing table.
        :param sep: {‘,‘, ‘;‘, ‘\t‘}, default ‘\t‘
        :param encoding: default ‘utf8‘
        """

        # Create Table
        df[:0].to_sql(table_name, self.sqlalchemy(), schema=schema_name, if_exists=if_exists, index=False)

        # Prepare data
        output = io.StringIO()
        df.to_csv(output, sep=sep, header=False, encoding=encoding, index=False)
        output.seek(0)

        # Insert data
        connection = self.sqlalchemy().raw_connection()
        cursor = connection.cursor()
        cursor.copy_from(output, schema_name + '.' + table_name, sep=sep, null='')
        connection.commit()
        cursor.close()

    def create_index(self, schema_name, table_name, columns):
        """
        Creates standard indexes on columns of PostgreSQL database
        :param schema_name: schema to create index
        :param table_name: table to create index
        :param columns: tuple -> columns to create index
        """

        indexes = '''
                    CREATE INDEX ON {}.{} ({});
                  '''.format(schema_name, table_name, columns)
        self.execute_sql(indexes)

    def insert_dict_record(self, schema, table, record):
        """
        Insert a dict inside a postgres table
        """
        sql_file = pkg_resources.resource_filename('bsatoolbelt', '/sqls/insert.sql')
        record = utils.format_dict_str(record)
        keys = str(tuple(record.keys())).replace("'", "")
        values = str(tuple(record.values()))

        query = open(sql_file, encoding='utf-8').read().format(schema=schema,
                                                               table=table,
                                                               columns=keys,
                                                               values=values)

        self.execute_sql(query)