#!/usr/bin/env python
import pika
import json
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='hello')

body = {"type": "sht31", "deviceId": "66aaq", "payload": {"temp": 30.12, "humi": 67.12}}

channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(body))
print(body)
connection.close()
