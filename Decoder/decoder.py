#!/usr/bin/env python
import pika
import json
from influx import Model

class Decoder:

  def __init__(self):
    self.model = Model()

    self.connection = pika.BlockingConnection(
      pika.ConnectionParameters(host='172.17.0.2'))
    self.channel = self.connection.channel()



  def callback(self, ch, method, properties, body):
    recv = json.loads(str(body, encoding="utf-8"))
    measurement = recv['type']
    tags = recv['deviceId']
    fields = recv['payload']
    print(measurement)
    print(fields)
    print(tags)
    self.model.insert(measurement, {"deviceId": tags}, fields) 


  def start(self, queue):
    self.channel.queue_declare(queue='hello')
    self.channel.basic_consume(
      queue='hello', on_message_callback=self.callback, auto_ack=True)
    self.channel.start_consuming()

if __name__ == "__main__":
  decoder = Decoder()
  decoder.start("hello")
