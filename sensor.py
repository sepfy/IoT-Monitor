from model import LevelDBModel, InfluxDBModel
import time, struct, json, math
from grove_sht31 import GroveTemperatureHumiditySensorSHT3x
from pir import MotionSensor

class Sensor:

  # Initialize database
  iotdb = InfluxDBModel("iot")
  motion = MotionSensor()

  def __init__(self, devdb, collector_cb):
    self.devdb = devdb
    self.devs = self.devdb.get_keys()
    self.connectionTime = {}
    self.collector_cb = collector_cb
    self.connectionTime = 0
    self.pred_time = 0
    self.survey = -1
  def acquire(self):
    sht31 = GroveTemperatureHumiditySensorSHT3x()
    while True:
      temp, humi = sht31.read()
      e = humi/100.0*6.105*math.exp(17.27*temp/(237.7+temp))
      AT = round(1.07*temp + 0.2*e - 2.7, 2)
      series = {"Temperature": round(temp, 2), "Humidity": round(humi, 2), "AT": AT}
      if time.time() - self.connectionTime > 60:
        #self.iotdb.insert("Thermometer", {"deviceId": "central"}, series)
        self.iotdb.insert("gateway", {}, series)
        self.connectionTime = time.time()

      if self.survey != -1:
        survey_series = series
        survey_series["feel"] = self.survey
        self.iotdb.insert("survey", {}, survey_series)
        self.survey = -1

      #print(series)
      if time.time() - self.pred_time > 1:
          series["pred"] = [{"s": time.time()*1000, "AT": 33}, \
                {"s": time.time()+60*60*4, "AT": 32}, \
                {"s": time.time()+60*60*8, "AT": 35}, \
                {"s": time.time()+60*60*12, "AT": 30}]
          self.pred_time = time.time()
      self.collector_cb(json.dumps(series))

      time.sleep(1)

  def detect(self):
    while True:
      if self.motion.detect() is True:
        print("detect")
        self.iotdb.insert("detect", {}, {"motion": 1})

if __name__ == "__main__":
  gattdb = LevelDBModel("devtype")
  devdb = LevelDBModel("devinfo")
