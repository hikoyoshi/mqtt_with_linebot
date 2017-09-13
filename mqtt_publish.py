#-*- coding:utf-8 -*-
import paho.mqtt.publish as publish
import sys,os,time,urllib2,subprocess,datetime
import Adafruit_DHT

mqtt_broker = 'localhost'
mqtt_port = 1883
topic = 'server_status'
hostname = 'http://XXXXXXXXXXX'
server_ip = 'Server IP'
PIN = 23
SENSOR = Adafruit_DHT.DHT11
temp_MAX = 28.0
humi_MAX = 70.0
# SENSOR option: Adafruit_DHT.DHT11、Adafruit_DHT.DHT22、Adafruit_DHT.AM2302
# PIN: raspberry pi2 GPIO 23
# default temperature is *C
# convert the temperature to Fahrenheit follow the below
# temperature = temperature * 9/5.0 + 32
def dht11():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    if humidity is not None and temperature is not None:
        temp = '{0:0.1f}'.format(temperature)
        humi = '{0:0.1f}'.format(humidity)
        #print 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity)
    else:
        print 'Failed to get reading. Try again!'
    return temp,humi

def timestamp():
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return t

# host_name: websit url 
# returns the HTTP status code that was sent with the response, or None if the URL is no HTTP URL.

def host_check(host_name):
    try:
        res = urllib2.urlopen(host_name)
        #host_info = "websit status code:{0}.\nServer working".format(res.getcode())
        host_info = "activate"
    except urllib2.URLError as err:
        #host_info = "websit status:{0}.\nServer deactivate".format(err)
        host_info = "deactivate"
    return host_info

# use the "ping" command check server is online or offline. 
# default command : ping -c 2 "ip"

def server_check(ip):
    with open(os.devnull,"wb") as _ping:
        output = subprocess.Popen(['ping','-c','2',str(ip)],stdout=_ping,stderr=_ping).wait()
        if output ==0:
            ipstatus = 'online'
        else:
            ipstatus = 'offline'
        return ipstatus

# publish.single(topic, payload="message", qos=2,, hostname="mqtt_broker",port=1883)
# Other publish.single option can follow the MQTT API

while True:
    pings = server_check(server_ip)
    info = host_check(hostname)
    dht_temp = dht11()
    if pings =="offline":
        ping_msg = "注意!!!伺服主機:"+server_ip+"\nstatus:"+pings+"\nTime:"+str(timestamp())
        publish.single(topic, ping_msg, hostname=mqtt_broker,qos=2)
    time.sleep(1)
    if info == "deactivate":
        host_msg =  "注意!!!網站: "+hostname+"\nstatus:"+info+"\nTime:"+str(timestamp())
        publish.single(topic, ping_msg, hostname=mqtt_broker,qos=2)
    if float(dht_temp[0]) > temp_MAX:
        temp_alert = "注意!!!目前溫度:"+ dht_temp[0]+"\nTime:"+str(timestamp())
        #print temp_alert
        publish.single(topic, temp_alert, hostname=mqtt_broker,qos=2)
    if float(dht_temp[1]) > humi_MAX:
        humi_alert = "注意!!!目前濕度:"+ dht_temp[1]+"\nTime:"+str(timestamp())
        #print humi_alert
        publish.single(topic, humi_alert, hostname=mqtt_broker,qos=2)
    time.sleep(60)
