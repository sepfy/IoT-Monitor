from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from model import LevelDBModel, InfluxDBModel
import time, struct

class Central:

  def __init__(self, devdb, gattdb):
    self.devdb = devdb
    self.gattdb = gattdb
    self.devs = self.devdb.get_keys()
    self.gatt_keys = self.gattdb.get_keys()
    self.gatts = self.gattdb.getall()
    self.connectionTime = {}
    for dev in self.devs:
      self.connectionTime[dev] = 0

  # Initialize database
  iotdb = InfluxDBModel("iot")
  # Initialize connection time

  # Initialize bluepy
  scanner = Scanner()
  conn = Peripheral()
  
  do_scan = True

  def read(self, addr):
    if addr in self.devs:
      try:
        if time.time() - self.connectionTime[addr] < 1:
          return 

        index = self.gatt_keys.index(self.devdb.get_dict(addr)["type"])
        services = self.gatts[index]["config"]
  
        # Connect to device 
        self.conn.connect(addr)
        series = {}
        for service in services:

          for charac_cfg in service["characs"]:
            charac = self.conn.getCharacteristics(uuid=charac_cfg["uuid"])[0]
            data = round(struct.unpack('<f', charac.read())[0], 2)
            series[charac_cfg["desc"]] = data
        self.connectionTime[addr] = time.time()
        print(series)
        self.iotdb.insert(self.gatts[index]["devid"], {"deviceId": addr}, series)
        self.conn.disconnect()

      except Exception as e:
        print(e)


  def scan(self):
    while self.do_scan is True:
      try:
        devices = self.scanner.scan(1)
        for device in devices:
          self.read(device.addr)
      except:
       pass

if __name__ == "__main__":
  central = Central()
  central.scan()
