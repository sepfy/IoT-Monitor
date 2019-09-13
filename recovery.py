from model import LevelDBModel

db = LevelDBModel('account/')
db.put("admin", "123456")

devdb = LevelDBModel("devinfo")
devdb.put_dict("Gateway", {"type": "Thermometer", "location": "Living Room"})
devdb.put_dict("120932ddwa", {"type": "Thermometer", "location":"Outdoor"})


