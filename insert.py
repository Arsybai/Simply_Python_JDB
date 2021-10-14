from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

datas = {
    "id": 0,
    "username": "Arsybai",
    "password": "Secreet1234"
}

db.insert(
    into="user",
    datas=datas
)

# if u don't see any error thats mean it's work