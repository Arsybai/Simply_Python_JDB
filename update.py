from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

db.update("user", "biography=Hello There", "username=arsybai")