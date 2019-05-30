import json
import decimal
import time
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime

class DecimalEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, decimal.Decimal):
      if o % 1 > 0:
        return float(o)
      else:
        return int(o)
    return super(DecimalEncoder, self).default(o)

class Model:

  def __init__(self):
    self.dynamodb = boto3.resource('dynamodb', region_name="ap-northeast-1")
    self.table = self.dynamodb.Table('IoTSensor')

  def get(self):
    response = self.table.query(
    KeyConditionExpression=Key('id').eq('r4vwwbav') &\
                           Key("timestamp").gte(1558874942)\
    )
    return response

  def get_last(self):
    response = self.table.query(
    KeyConditionExpression=Key('id').eq('r4vwwbav')
    )
    item = response["Items"][-1]["payload"]
    j = json.dumps(item, indent=4, cls=DecimalEncoder)
    return j

  def get_4hour(self, key):
    cur_ts = int(time.time())
    response = self.table.query(
    KeyConditionExpression=Key('id').eq('r4vwwbav') &\
                           Key("timestamp").gte(cur_ts - 100*60*48)
    )
    items = response["Items"]
    ts = []
    data = []
    j = json.dumps(items, indent=4, cls=DecimalEncoder)
    objs = json.loads(j)

    for item in objs:
        ts.append(datetime.utcfromtimestamp(item["payload"]["timestamp"]).strftime('%H:%M'))
        data.append(item["payload"][key])
    return {"ts": ts, "data": data}

    

if __name__ == "__main__":
  
  model = Model()
  print(model.get_4hour("t"))
  print(model.get_4hour("h"))
  #print(j)
  #response = model.get()
  #items = response["Items"]
  #for item in items:
  #  timestamp = item['payload']['timestamp']
  #  timearray = time.localtime(timestamp)
  #  timestr = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
  #  print(timestr, item['payload']['t'], item['payload']['h'])
