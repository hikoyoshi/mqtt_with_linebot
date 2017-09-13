import paho.mqtt.client as mqtt
import os,sys
from linebot import LineBotApi
from linebot.models import TextSendMessage

mqtt_broker = 'localhost'
mqtt_port = 1883
keepalive=60

uid = 'your user ID for linebot'
topic = "server_status"

def on_connect(client,data,flags,rc):
    #print "connected with code"+str(rc)
    client.subscribe(topic)

def on_message(client,data,msg):
    #push_message(self, to, messages, timeout=None)
    #Send messages to users, groups, and rooms at any time.
    #line_bot_api.push_message(to, TextSendMessage(text='Hello World!'))
    line_bot_api.push_message(uid,TextSendMessage(text=str(msg.payload)))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker,mqtt_port,keepalive)

client.loop_forever()
