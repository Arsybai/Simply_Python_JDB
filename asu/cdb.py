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

    def fetch_all(self, table:str, limit:int=0):
        theDB = openDb(self.db_name)
        if limit == 0:
            return theDB[table]
        else:
            return theDB[table][:limit]

    def fetch_one(self, table:str):
        theDB = openDb(self.db_name)
        try:
            return theDB[table][0]
        except:
            return None

    def fetch_all_filter(self, table:str, where:str, limit:int=0):
        theDB = openDb(self.db_name)
        key_ = where.split("=")[0]
        val_ = where.split("=")[1]
        if theDB["edata"][table][key_]["data_type"] == "int":
            val_ = int(val_)
        elif theDB["edata"][table][key_]["data_type"] == "bool":
            if val_.lower() == "false":
                val_ = False
            elif val_.lower() == "true":
                val_ = True
        else:
            val_ = val_
        ff_ = []
        for i in theDB[table]:
            if self.case_sensitive == True:
                try:
                    if i[key_].lower() == val_.lower():
                        ff_.append(i)
                except:
                    if i[key_] == val_:
                        ff_.append(i)
            else:
                if i[key_] == val_:
                    ff_.append(i)
        if limit == 0:
            return ff_
        else:
            return ff_[:limit]

    def fetch_one_filter(self, table:str, where:str):
        the_data = self.fetch_all_filter(table, where, 2)
        try:
            return the_data[0]
        except:
            return None

    def filter_like(self, table:str, where:str, limit:int = 0):
        theDB = openDb(self.db_name)
        key_ = where.split("=")[0]
        val_ = where.split("=")[1]
        if theDB["edata"][table][key_]["data_type"] == "int":
            val_ = int(val_)
        elif theDB["edata"][table][key_]["data_type"] == "bool":
            if val_.lower() == "false":
                val_ = False
            elif val_.lower() == "true":
                val_ = True
        else:
            val_ = val_
        ff_ = []
        for i in theDB:
            if self.case_sensitive == True:
                try:
                    if val_.lower() in i[key_].lower():
                        ff_.append(i)
                except:
                    if val_ in i[key_]:
                        ff_.append(i)
            else:
                if val_ in i[key_]:
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
        skey_ = set_.split("=")[0]
        sval_ = set_.split("=")[1]
        gkey_ = where.split("=")[0]
        gval_ = where.split("=")[1]
        if theDB["edata"][table][gkey_]["data_type"] == "bool":
            if gval_.lower() == "true":
                gval_ = True
            elif gval_.lower() == "false":
                gval_ = False
            else:
                return "Boolean must be True or False"
        elif theDB["edata"][table][gkey_]["data_type"] == "int":
            try:
                gval_ = int(gval_)
            except Exception as e:
                raise e
        if theDB["edata"][table][skey_]["data_type"] == "bool":
            if sval_.lower() == "true":
                sval_ = True
            elif sval_.lower() == "false":
                sval_ = False
            else:
                print("Boolean must be True or False")
        elif theDB["edata"][table][skey_]["data_type"] == "int":
            try:
                sval_ = int(sval_)
            except Exception as e:
                raise e
        for i in theDB[table]:
            if self.case_sensitive == False:
                try:
                    if i[gkey_].lower() == gval_.lower():
                        i[skey_] = sval_
                except:
                    if i[gkey_] == gval_:
                        i[skey_] = sval_
            else:
                if i[gkey_] == gval_:
                    i[skey_] = sval_
        saveDb(theDB, self.db_name)
        return "ok"

    def add_column(self, table:str, column_name:str, default_value=None, data_type:str="str"):
        theDB = openDb(self.db_name)
        theDB["edata"][table][column_name] = {"default_value": default_value, "data_type": data_type}
        saveDb(theDB, self.db_name)
        return "ok"

    def printDB(self, pretyfy=False):
        if pretyfy:
            return self.pretyfy(openDb(self.db_name))
        return openDb(self.db_name)
