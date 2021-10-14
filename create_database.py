from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

db.create_database(database_name="test")