from asu.cdb import JSQL

db = JSQL(True, "test")

# CREATE A DATABASE
"""
db.create_database("test")
"""

# SHOW THE DATABASE
"""
for i in db.show_database():
    print(i)
"""

# CREATE TABLE
"""
db.create_table('user', ['id', 'username', 'password', 'biography'])
"""

# SHOW TABLES
"""
for i in db.show_tables():
    print(i)
"""

# SET THE COLUMN
"""
db.set_column("user", "biography", "str", "Hello There")
"""

# INSERT DATA
"""
datas = {
    "id" : 0,
    "username": "Arsybai",
    "password": "secreet"
}
db.insert("user", datas)
"""

# INSERT MANY
"""
datas = [
    {
        "id": 1,
        "username": "chizuru",
        "password": "chizuru1234"
    },
    {
        "id": 2,
        "username": "sayu",
        "password": "sayu1234"
    }
]
db.insert_many("user", datas)
"""