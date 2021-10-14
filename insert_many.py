from asu.cdb import SimplyJSONDB

db = SimplyJSONDB(case_sensitive=False, db_name="test")

datas = [
    {
        "id": 1,
        "username": "Chizuru",
        "password": "Secreet"
    },
    {
        "id": 2,
        "username": "Sayu",
        "password": "Secreet"
    },
]

db.insert_many(
    into="user",
    datas=datas
)