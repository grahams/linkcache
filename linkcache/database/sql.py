#!/usr/bin/env python

import db
import time

class LinkSql(db.LinkDb):
    def __init__(self):
        db.LinkDb.__init__(self)
        assert('field_placeholder' in dir(self))

    def create_tables(self):
        q  = r"CREATE TABLE url ("
        q += r"id INTEGER PRIMARY KEY AUTOINCREMENT, "
        q += r"url TEXT NOT NULL, "
        q += r"shorturl TEXT, "
        q += r"user TEXT NOT NULL, "
        q += r"first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
        q += r"title TEXT, "
        q += r"flags INT, "
        q += r"type TEXT, "
        q += r"description TEXT, "
        q += r"channel TEXT DEFAULT '', "
        q += r"private INT DEFAULT 0, "
        q += r"count INT DEFAULT 1, "
        q += r"alive INT DEFAULT 1 "
        q += r" )"
        self.execute(q, [])

    def execute(self, command, args):
        pass

    def query_one(self, command, args):
        pass

    def update(self, id, field, value):
        args = [value, id]
        query = """UPDATE url SET %s = %s WHERE id = %s""" % (field,
                self.field_placeholder, self.field_placeholder)
        self.execute(query, args)

    def update_shorturl(self, id, shorturl):
        query = """UPDATE url SET shorturl = ? WHERE id = ?"""
        self.execute(query, [shorturl, id])

    def increment_count(self, id):
        query = """UPDATE url SET count = count + 1 WHERE id = %s""" % \
                self.field_placeholder
        self.execute(query, [id])

    def new_entry(self, url, shorturl, user, title, flags=0, type=None,
                  description=None, channel="", private=0):

        args = [url, shorturl, user, title, flags]

        fields = """url, shorturl, user, title, flags"""

        if type is not None:
            fields += ", type"
            args.append(type)

        if description is not None:
            fields += ", description"
            args.append(description)

        if private != 0:
            fields += ", private"
            args.append(private)

        if channel:
            fields += ", channel"
            args.append(channel)

        values = ", ".join([self.field_placeholder] * len(args))
        query = """INSERT INTO url (%s) VALUES(%s)""" % (fields, values)

        self.execute(query, args)

    @staticmethod
    def row_to_result(row):
        return {
            'url' : row[0],
            'user' : row[1],
            'count' : int(row[2]),
            'timestamp' : row[3],
            'title' : row[4],
            'request_timestamp' : row[5],
            'alive' : row[6],
            'flags' :  int(row[7]),
            'private' : row[8],
            'type' : row[9],
            'description' : row[10],
            'shorturl' : row[11],
            'id' : row[12],
        }

    def fetch_by_field(self, field, value, channel=""):
        query  = """SELECT url, user, count, first_seen as 'ts [timestamp]', """
        query += """title, CURRENT_TIMESTAMP as 'ts [timestamp]', alive, """
        query += """flags, private, type, description, shorturl, id """
        query += """FROM url WHERE %s = %s""" % (field, self.field_placeholder)

        args = [value]

        if channel is not None:
            query += " AND channel = %s" % self.field_placeholder
            args.append(channel)

        row = self.query_one(query, args)
        if row:
            return self.row_to_result(row)
        return None

    def close(self):
        pass

    def flush(self):
        pass

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
