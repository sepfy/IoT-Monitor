from influxdb import InfluxDBClient
import plyvel
import json, time

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

  def get_keys(self):
    keys = []
    for bytes_of_key, bytes_of_value in self.db:
      key = str(bytes_of_key, encoding="utf-8")
      keys.append(key)
    return keys

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

TIME_UNIT = 1000000000

class InfluxDBModel:
  def __init__(self, db):
    self.client = InfluxDBClient(host='localhost', port=8086)
    self.client.create_database(db)
    self.client.switch_database(db)

  def insert(self, measurement, tags, fields):
    json_body = [{"measurement": measurement, "tags": tags, "fields": fields}]
    self.client.write_points(json_body)

  def query(self, measurement, ts, te):
    sql = "SELECT * FROM %s WHERE time >= %d AND time <= %d "\
            %(measurement, ts*TIME_UNIT, te*TIME_UNIT)
    #print(sql)
    rs = self.client.query(sql)
    print(list(rs.get_points(measurement=measurement)))


if __name__ == "__main__":
  model = InfluxDBModel("iot")
  #model.query("Thermometer", (time.time()-3000), time.time())
  

  # Sample
  # Get 24hr ago data

  # 1 Day = 60*60*12
  dayTimeStamp = 60*60*24
  ts = time.time() + 60*60*8 - dayTimeStamp
  te = ts + 4*60*60
  model.query("Thermometer", ts, te)

  #  model.insert("sht31", {"deviceId": "6abd"}, {"temp": 31.1, "humi": 65.1})
