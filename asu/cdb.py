import json
import os
from typing import Any

def openDb(dbname):
    with open('./data/{}.json'.format(dbname), 'r') as dbread:
        theDB = json.load(dbread)
    return theDB

def saveDb(datas, dbname):
    with open('./data/{}.json'.format(dbname), 'w') as dbwrite:
        json.dump(datas, dbwrite)

class SimplyJSONDB(object):

    def __init__(self, case_sensitive:bool=False, db_name:str="test") -> None:

        self.case_sensitive = case_sensitive
        self.db_name = db_name

        return None

    def pretyfy(self, data:dict):
        return json.dumps(data, indent=4)

    def create_database(self, database_name:str):
        if os.path.isfile('./data/{}.json'.format(database_name)):
            print("Error : Database with name {} already exsist.".format(database_name))
        else:
            if not os.path.exists('./data'):
                os.makedirs('./data')
            with open('./data/{}.json'.format(database_name), 'w') as dbwrite:
                json.dump({}, dbwrite)
            print("Success create database")

    def show_database(self):
        dbs = []
        for i in os.listdir('./data'):
            dbs.append(i.replace(".json",""))
        return dbs

    def create_table(self, table_name:str, column:list):
        """
        use column like ['username', 'password']
        """
        with open('./data/{}.json'.format(self.db_name), 'r') as dbread:
            theDB = json.load(dbread)
        if table_name in theDB:
            print("Table for {} already exsist.".format(table_name))
        else:
            theDB[table_name] = []
            try:
                theDB["edata"][table_name] = {}
            except:
                theDB["edata"] = {}
                theDB["edata"][table_name] = {}
            for i in column:
                theDB["edata"][table_name][i] = {
                    "default_value": None,
                    "data_type": "str"
                }
            with open('./data/{}.json'.format(self.db_name), 'w') as dbwrite:
                json.dump(theDB, dbwrite)
            print("Success created table.")

    def show_tables(self):
        theDB = openDb(self.db_name)
        del theDB["edata"]
        return theDB.keys()

    def set_column(self, table_name:str, column:str, data_type:str="str", default_value:str=None):
        """
        table_name      : the name of table that you want to set.
        column          : the column in the table that you want to set.
        data_type       : the data type of the column it's like str, bool, int and more.
        default_value   : the default value of the column. (default : null)
        """
        theDB = openDb(self.db_name)
        theDB["edata"][table_name][column]["data_type"] = data_type
        theDB["edata"][table_name][column]["default_value"] = default_value
        saveDb(theDB, self.db_name)
        return "OK"

    def insert(self, into:str, datas:dict):
        """
        Example
        into = "test"
        datas = {
            "id": 0,
            "username":"arsybai",
            "password":"secreet"
        }
        insert(into, datas)

        into    : the table you want to insert
        datas   : the datas for each column
        """
        theDB = openDb(self.db_name)
        keya = theDB["edata"][into].keys()
        ff_ = {}
        for i in keya:
            try:
                ff_[i] = datas[i]
            except:
                ff_[i] = theDB["edata"][into][i]["default_value"]
        theDB[into].append(ff_)
        saveDb(theDB, self.db_name)
        return "Insert {} Success".format(datas)

    def insert_many(self, into:str, datas:list):
        for i in datas:
            self.insert(into, i)
        return "Insert {} Success".format(datas)

    def fetch_all(self, table:str, limit:int):
        theDB = openDb(self.db_name)
        if limit == 0:
            return theDB[table]
        else:
            return theDB[table][:limit]

    def fetch_one(self, table:str):
        theDB = openDb(self.db_name)
        return theDB[table][0]

    def fetch_all_filter(self, table:str, where:str, limit:int=0):
        theDB = openDb(self.db_name)
        theFilter = where.split("=")
        ff_ = []
        for i in theDB[table]:
            if self.case_sensitive == True:
                if i[theFilter[0]] == theFilter[1]:
                    ff_.append(i)
            else:
                if i[theFilter[0]].lower() == theFilter[1].lower():
                    ff_.append(i)
        if limit == 0:
            return ff_
        else:
            return ff_[:limit]

    def fetch_one_filter(self, table:str, where:str):
        the_data = self.fetch_all_filter(table, where, 2)
        return the_data[0]

    def filter_like(self, table:str, where:str, limit:int = 0):
        theDB = openDb(self.db_name)
        theFilter = where.split(" like ")
        ff_ = []
        for i in theDB[table]:
            if self.case_sensitive == True:
                if theFilter[1] in i[theFilter[0]]:
                    ff_.append(i)
            else:
                if theFilter[1].lower() in i[theFilter[0]].lower():
                    ff_.append(i)
        if limit == 0:
            return ff_
        else:
            return ff_[:limit]

    def delete(self, table:str, where:str):
        theDB = openDb(self.db_name)
        datas = self.fetch_all_filter(table, where)
        for i in datas:
            theDB[table].remove(i)
        saveDb(theDB, self.db_name)
        return "{} Row(s) Deleted".format(len(datas))

    def drop_table(self, table:str):
        theDB = openDb(self.db_name)
        del theDB[table]
        del theDB["edata"][table]
        saveDb(theDB, self.db_name)
        return "ok"

    def update(self, table:str, set_:str, where:str):
        theDB = openDb(self.db_name)
        theTable =theDB[table]
        setTo = set_.split("=")
        theFilter = where.split("=")
        for i in theTable:
            if self.case_sensitive == True:
                if i[theFilter[0]] == theFilter[1]:
                    i[setTo[0]] = setTo[1]
            else:
                if i[theFilter[0]].lower() == theFilter[1].lower():
                    i[setTo[0]] = setTo[1]
        saveDb(theDB, self.db_name)
        return "ok"