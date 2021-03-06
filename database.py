"""
    The database module contains the classes and functions that are required to
    store and query application data from a SQLite database.

    The variables tblProjectSchema and tblWorkflowSchema contain the schema
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
import time

SCHEMA_VERSION = 1

tblMetaSchema = [
        ('key', 'TEXT UNIQUE'),
        ('value', 'TEXT')
        ]
tblMetaCols = [
        'key', 'value' ]
tblProjectSchema = [
        ('pid', 'INTEGER PRIMARY KEY'),
        ('name', 'TEXT UNIQUE'),
        ('title', 'TEXT'),
        ('description', 'TEXT'),
        ('created', 'INTEGER'),
        ('modified', 'INTEGER')
        ]
tblProjectCols = [
        'pid', 'name', 'title', 'description', 'created', 'modified' ]
tblWorkflowSchema = [
        ('wif', 'INTEGER PRIMARY KEY'),
        ('ppid', 'INTEGER'),
        ('pwif', 'INTEGER'),
        ('name', 'TEXT'),
        ('title', 'TEXT'),
        ('description', 'TEXT'),
        ('status', 'TEXT'),
        ('created', 'INTEGER'),
        ('modified', 'INTEGER')
        ]
tblWorfklowCols = [
        'wif', 'ppid', 'pwif', 'name', 'title', 'description', 'status',
        'created', 'modified' ]

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
        tablenames = self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")
        if ('tblMeta',) not in tablenames:
            self.createTable('tblMeta', tblMetaSchema)
            self.insert('tblMeta', {'key': 'schema_version', 'value': SCHEMA_VERSION})
            self.createTable('tblProject', tblProjectSchema)
            self.createTable('tblWorkflow', tblWorkflowSchema)
        else:
            schemaversion = self.cursor.execute(
                    "SELECT 1 FROM tblMeta WHERE key=?", ('schema_version',))
            schemaversion = schemaversion.fetchone()[0]
            if schemaversion != SCHEMA_VERSION:
                raise Exception('Trying to open database with old schema!')

    def createTable(self, tablename, schema):
        """
            We define table schemas with a list that contains two member tuples
            for column tablename. See the declarations at the beginning of this file.

            in: createTable('tblFoo', [('foo', 'INTEGER'), ('bar', 'TEXT')])
            sql: CREATE TABLE tblFoo (foo INTEGER, bar TEXT)
        """
        sql1 = [];
        for col in schema:
            sql1.append(' '.join(col))
        query = 'CREATE TABLE {tblName} ({schema})'.format(
                tblName=tablename, schema=', '.join(sql1))
        self.cursor.execute(query)
        self.connection.commit()

    def insert(self, tablename, data):
        """
            Generic insert method for database tables.

            in: 'tblFoo', {'col1': 'val1', 'col2': 'val2'}
        """
        cols = []
        values = []
        for col, val in data.items():
            cols.append(col)
            values.append(val)
        query = "INSERT INTO {tblName} ({columns}) VALUES ({questionmarks})"
        query = query.format(
                tblName=tablename,
                columns=', '.join(cols),
                questionmarks=', '.join(len(values)*'?'))
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        if tablename in ['tblProject', 'tblWorkflow']:
            return self.cursor.lastrowid

    def getRowCount(self, tablename):
        """
            Get the number of rows in a specific table.
        """
        query = "SELECT Count(*) FROM {}".format(tablename)
        return self.cursor.execute(query).fetchone()[0]

    def getConditionalRowCount(self, tablename, conditions):
        query = "SELECT Count(*) FROM {} WHERE {}"
        condpart = []
        condval = []
        for key, value in conditions.items():
            condpart.append('{}=?'.format(key))
            condval.append(value)
        query = query.format(tablename, ' AND '.join(condpart))
        count = self.cursor.execute(query, tuple(condval))
        count = count.fetchone()[0]
        return count

    def getAllRows(self, tablename, columns):
        """
            Generic select method. Return a list of columns for all records.

            in: 'tblFoo', ['foo', 'bar']
            out: [{'foo': 'fooval1', 'bar': 'barval1'}, {..}]
        """
        query = "SELECT {} FROM {}".format(', '.join(columns), tablename)
        records = self.cursor.execute(query).fetchall()
        out = []
        for rec in records:
            outrec = {}
            for i, col in enumerate(columns):
                outrec[col] = rec[i]
            out.append(outrec)
        return out

    def getConditionalRow(self, tablename, columns, condition):
        """
            Simply said, this is a generalization of
            "SELECT {cols} FROM {tbl} WHERE col=val"
            There can be one or more columns specified and one condition.

            in: getConditionalRow('tblProject', ['name'], {'pid': 1})
            out: {'name': 'foo'}
        """
        query = "SELECT {} FROM {} WHERE {}=?"
        query = query.format(
                ', '.join(columns), tablename, list(condition.keys())[0])
        record = self.cursor.execute(query, (list(condition.values())[0],))
        record = record.fetchone()

        out = {}
        for i, col in enumerate(columns):
            out[col] = record[i]
        return out

    def getConditionalRows(self, tablename, columns, condition):
        """
            Like getConditionalRow, just for multiple rows
        """
        ckeys, cvals, result = [], [], []
        for key, value in condition.items():
            ckeys.append('{}=?'.format(key))
            cvals.append(value)
        ckeys = ' AND '.join(ckeys)
        query = "SELECT {} FROM {} WHERE {}".format(
                    ', '.join(columns), tablename, ckeys)
        records = self.cursor.execute(query, tuple(cvals)).fetchall()
        for record in records:
            recdir = {}
            for i, column in enumerate(columns):
                recdir[column] = record[i]
            result.append(recdir)
        return result

    def updateRow(self, tablename, data, conditions):
        """
            Update a single record in a database table

            Example:
            updateRow('tblProject', {'name': newname}, {'pid': pid})
        """
        query = "UPDATE {tblName} SET {dataQuery} WHERE {whereQuery}"
        newQuery = []
        newValues = []
        for key, value in data.items():
            newQuery.append('{}=?'.format(key))
            newValues.append(value)
        condQuery = []
        condValues = []
        for key, value in conditions.items():
            condQuery.append('{}=?'.format(key))
            condValues.append(value)
        query = query.format(
                tblName = tablename,
                dataQuery = ', '.join(newQuery),
                whereQuery = ' AND '.join(condQuery))
        self.cursor.execute(query, tuple(newValues + condValues))
        if tablename in ['tblProject', 'tblWorkflow']:
            timestamp = int(time.time())
            timequery = "UPDATE {} SET modified=? WHERE {}"
            timequery = timequery.format(tablename, ' AND '.join(condQuery))
            self.cursor.execute(timequery, tuple([timestamp] + condValues))
        self.connection.commit()

    def delete(self, tablename, conditions):
        if len(conditions) == 0:
            print('error: trying to delete row with empty condition')
            return
        query = "DELETE FROM {tablename} WHERE {conditions}"
        condkeys = []
        condvals = []
        for key, value in conditions.items():
            condkeys.append('{}=?'.format(key))
            condvals.append(value)
        query = query.format(tablename=tablename,
                             conditions=' AND '.join(condkeys))
        self.cursor.execute(query, tuple(condvals))
        self.connection.commit()

