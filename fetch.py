from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

# FETCH ALL DATA
datas = db.fetch_all(table="user", limit=0) # Use limit 0 for unlimited fetch
print(datas)


# FETCH THE FIRST ROW
data = db.fetch_one(table="user")
print(data)