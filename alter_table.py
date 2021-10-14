from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

db.set_column(
    table_name="user",
    column="id",
    data_type="int",
    default_value=0
)

# if u don't see any error thats mean it's work