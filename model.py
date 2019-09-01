import plyvel
import json

class LevelDBModel:
  def __init__(self, dbname):
    self.db = plyvel.DB(dbname, create_if_missing=True)

  def put(self, key, value):
    bytes_of_key = bytes(key, encoding="utf-8")
    bytes_of_value = bytes(value, encoding="utf-8")
    self.db.put(bytes_of_key, bytes_of_value)

  def get(self, key):
    bytes_of_key = bytes(key, encoding="utf-8")
    bytes_of_value = self.db.get(bytes_of_key)
    value = str(bytes_of_value, encoding="utf-8")
    return value

  def getall(self):
    devs = []
    for bytes_of_key, bytes_of_value in self.db:
      key = str(bytes_of_key, encoding="utf-8")
      value = str(bytes_of_value, encoding="utf-8")
      devs.append({"devid": key, "config": json.loads(value)})
   
    return devs

  def delete(self, key):
    bytes_of_key = bytes(key, encoding="utf-8")
    self.db.delete(bytes_of_key)

  def modify_dict(self, key, dict_key, value):
    config = self.get_dict(key)
    config[dict_key] = value
    self.put_dict(key, config)

  def put_dict(self, key, value):
    self.put(key, json.dumps(value))

  def get_dict(self, key):
    value = self.get(key)
    return json.loads(value)


