from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

# FETCH ALL FILTER
datas = db.fetch_all_filter(table="user", where="username=arsybai", limit=1) # Use limit=0 for fetch all
print(db.pretyfy(datas))

# FETCH ONE FILTER
data = db.fetch_one_filter(table="user", where="username=arsybai")
print(db.pretyfy(data))