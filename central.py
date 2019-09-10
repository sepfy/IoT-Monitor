from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from model import LevelDBModel, InfluxDBModel
import time, struct

iotdb = InfluxDBModel("iot")

devdb = LevelDBModel("devinfo")
gattdb = LevelDBModel("devtype")

# Initialize database
devs = devdb.get_keys()
gatt_keys = gattdb.get_keys()
gatts = gattdb.getall()
# Initialize connection time
connectionTime = {}
for dev in devs:
  connectionTime[dev] = 0


def read(addr):
  if addr in devs:
    try:
      if time.time() - connectionTime[addr] < 60:
        return 

      index = gatt_keys.index(devdb.get_dict(addr)["type"])
      services = gatts[index]["config"]
  
      # Connect to device 
      conn.connect(addr)
      series = {}
      for service in services:

        for charac_cfg in service["characs"]:
          charac = conn.getCharacteristics(uuid=charac_cfg["uuid"])[0]
          data = round(struct.unpack('<f', charac.read())[0], 2)
          series[charac_cfg["desc"]] = data
      connectionTime[addr] = time.time()
      print(series)
      iotdb.insert(gatts[index]["devid"], {"deviceId": addr}, series)
      conn.disconnect()

    except Exception as e:
      print(e)

# Initialize bluepy
scanner = Scanner()
conn = Peripheral()

while True:
  devices = scanner.scan(5)
  for device in devices:
    read(device.addr)
