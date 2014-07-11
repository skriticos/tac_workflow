"""
    The database module contains the classes and functions that are required to
    store and query application data from a SQLite database.

    The variables tblProjectSchema and tblWorfklowSchema contain the schema
    definitions for the two tables that we are using to store data.

    db = database.DataBase(
        os.path.join(
            os.path.expanduser('~'), '.local', 'share'. 'tac', 'tac.db')
    db.createTable('tblProject', database.tblProjectSchema)
    ...
"""

import sqlite3
import os
import os.path

tblMetaSchema = [
        ('key', 'TEXT UNIQUE'),
        ('value', 'TEXT')
        ]
tblMetaCols = [
        'key',
        'value'
        ]
tblProjectSchema = [
        ('pid', 'INTEGER PRIMARY KEY'),
        ('name', 'TEXT UNIQUE'),
        ('title', 'TEXT'),
        ('description', 'TEXT'),
        ('created', 'INTEGER'),
        ('modified', 'INTEGER')
        ]
tblProjectCols = [
        'pid',
        'name',
        'title',
        'description',
        'created',
        'modified'
        ]
tblWorkflowSchema = [
        ('wif', 'INTEGER PRIMARY KEY'),
        ('ppid', 'INTEGER'),
        ('pwif', 'INTEGER'),
        ('name', 'TEXT UNIQUE'),
        ('title', 'TEXT'),
        ('description', 'TEXT'),
        ('status', 'TEXT'),
        ('created', 'INTEGER'),
        ('modified', 'INTEGER')
        ]
tblWorfklowCols = [
        'wif',
        'ppid',
        'pwif',
        'name',
        'title',
        'description',
        'status',
        'created',
        'modified'
        ]

class DataBase():

    def __init__(self, path):
        """
            Establish a connection to database file. The path argument is the
            full database path. If the path or database file do not exist, they
            are created. If the database schema is not existent, it will be
            created.

            in: '/foo/bar/baz.db'
        """
        if path != ':memory:':
            dirname = os.path.dirname(path)
            filename = os.path.basename(path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def createTable(self, name, schema):
        """
            We define table schemas with a list that contains two member tuples
            for column name. See the declarations at the beginning of this file.

            in: createTable('tblFoo', [('foo', 'INTEGER'), ('bar', 'TEXT')])
            sql: CREATE TABLE tblFoo (foo INTEGER, bar TEXT)
        """
        sql1 = [];
        for col in schema:
            sql1.append(' '.join(col))
        query = 'CREATE TABLE {tblName} ({schema})'.format(
                tblName=name, schema=', '.join(sql1))
        self.cursor.execute(query)
        self.connection.commit()


