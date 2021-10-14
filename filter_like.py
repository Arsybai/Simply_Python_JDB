from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

datas = db.filter_like(table="user", where="username like bai", limit=0)
print(datas)