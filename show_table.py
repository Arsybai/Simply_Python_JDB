from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

tables = db.show_tables()

for i in tables:
    print(i)