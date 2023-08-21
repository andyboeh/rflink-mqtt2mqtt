#!/usr/bin/env python
# (c) 2021 Andreas Böhler
# License: Apache 2.0

import paho.mqtt.client as mqtt
import json
import yaml
import os
import sys
import time
import socket
import threading
import socketserver
import uuid

if os.path.exists('/config/rflink-mqtt2mqtt.yaml'):
    fp = open('/config/rflink-mqtt2mqtt.yaml', 'r')
    config = yaml.safe_load(fp)
    fp.close()
elif os.path.exists('rflink-mqtt2mqtt.yaml'):
    fp = open('rflink-mqtt2mqtt.yaml', 'r')
    config = yaml.safe_load(fp)
    fp.close()
else:
    print('Configuration file not found, exiting.')
    sys.exit(1)

def parseRfLink(msg, topic, stripid):
    parts = msg.split(';')
    if len(parts) < 4:
        return

    if parts[0] != "20":
        return;

    seq = parts[1]
    proto = parts[2]
    payload = {}
    devid = ""
    for part in parts[3:]:
        if not '=' in part:
            continue
        key, value = part.split('=', 2)
        if key == "ID":
            devid = value
        elif key == "TEMP":
            payload[key] = (int(value, 16) & 0x7fff ) / 10
            if (int(value, 16) & 0x8000) == 0x8000:
                payload[key] = -payload[key]
        else:
            payload[key] = value
    topic = topic + "/" + proto
    if not stripid:
        topic +=  "_" + devid
    for key in payload:
        value = payload[key]
        mqttc.publish(topic + '/' + key, payload=value, retain=False)

# Define MQTT event callbacks
def on_connect(client, userdata, flags, rc):
    connect_statuses = {
        0: "Connected",
        1: "incorrect protocol version",
        2: "invalid client ID",
        3: "server unavailable",
        4: "bad username or password",
        5: "not authorised"
    }
    if rc != 0:
        print("MQTT: " + connect_statuses.get(rc, "Unknown error"))
    else:
        for ii in range(0, len(config['rflink'])):
            mqttc.subscribe(config['rflink'][ii]['topic'] + '/' + config['rflink'][ii]['msg'])

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection")
    else:
        print("Disconnected")

def on_message(client, obj, msg):
    print("Msg: " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    for ii in range(0, len(config['rflink'])):
        if msg.topic == config['rflink'][ii]['topic'] + '/' + config['rflink'][ii]['msg']:
            parseRfLink(msg.payload.decode('ascii'), config['rflink'][ii]['topic'], config['rflink'][ii]['stripid'])

def on_publish(client, obj, mid):
    print("Pub: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

# Setup MQTT connection
mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message

if config['mqtt']['debug']:
    print("Debugging messages enabled")
    mqttc.on_log = on_log    
    mqttc.on_publish = on_publish

if config['mqtt']['username'] and config['mqtt']['password']:
    mqttc.username_pw_set(config['mqtt']['username'], config['mqtt']['password'])
try:
    mqttc.connect(config['mqtt']['host'], config['mqtt']['port'], 60)
except:
    print('Error connecting to MQTT, will now quit.')
    sys.exit(1)
mqttc.loop_start()


    
while True:
    time.sleep(1)
