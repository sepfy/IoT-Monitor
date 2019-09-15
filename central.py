from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from model import LevelDBModel, InfluxDBModel
import time, struct


class ScanDelegate(DefaultDelegate):
  def __init__(self, callback):
    DefaultDelegate.__init__(self)
    self.callback = callback

  def handleDiscovery(self, dev, isNewDev, isNewData):
    if isNewDev:
      self.callback(dev)


class Central:

  def __init__(self, devdb, gattdb, scanner_cb):
    self.devdb = devdb
    self.gattdb = gattdb
    self.devs = self.devdb.get_keys()
    self.gatt_keys = self.gattdb.get_keys()
    self.gatts = self.gattdb.getall()
    self.connectionTime = {}
    for dev in self.devs:
      self.connectionTime[dev] = 0


    scanner_delegate = ScanDelegate(scanner_cb)
    listener_delegate = ScanDelegate(self.listener_callback)

    self.scanner = Scanner().withDelegate(scanner_delegate)
    self.listener = Scanner().withDelegate(listener_delegate)


  # Initialize database
  iotdb = InfluxDBModel("iot")

  # Initialize bluepy
  conn = Peripheral()
  
  do_listen = True

  def listener_callback(self, dev):
    if dev.addr in self.devs:
      try:
        if time.time() - self.connectionTime[dev.addr] < 60:
          return
      except:
        pass
      self.listener.do_process = False

  def read(self, addr):
    if addr in self.devs:
      try:

        if self.connectionTime[addr] is None:
          self.connectionTime[addr] = 0  

        if time.time() - self.connectionTime[addr] < 60:
          return 
        self.connectionTime[addr] = time.time()
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
        print(series)
        self.iotdb.insert(self.gatts[index]["devid"], {"deviceId": addr}, series)
        self.conn.disconnect()

      except Exception as e:
        pass
        #print(e)


  def listen(self):
    self.scanner.do_process = False
    self.do_listen = True
    # wait for scanner is stopped
    time.sleep(0.5)
    while self.do_listen is True:
      try:
        self.listener.do_process = True
        devices = self.listener.scan(60)
        for device in devices:
          self.read(device.addr)
      except:
        pass
    

  def scan(self):

    self.do_listen = False
    self.listener.do_process = False
    self.scanner.do_process = True
    # wait for listener is stopped
    time.sleep(1.0)
    self.scanner.scan(60)

if __name__ == "__main__":
  central = Central()
  central.listen()
