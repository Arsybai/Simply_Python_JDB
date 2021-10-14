from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

db.create_table(table_name="user", column=["id", "username", "password", "biography"])