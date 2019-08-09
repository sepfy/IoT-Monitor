from influxdb import InfluxDBClient

class Model:
  def __init__(self):
    self.client = InfluxDBClient(host='localhost', port=8086)
    self.client.create_database("iot")
    self.client.switch_database('iot')

  def insert(self, measurement, tags, fields):
    json_body = [{"measurement": "sht31", "tags": tags, "fields": fields}]
    self.client.write_points(json_body)

if __name__ == "__main__":
  model = Model()
  model.insert("sht31", {"deviceId": "6abd"}, {"temp": 31.1, "humi": 65.1})
