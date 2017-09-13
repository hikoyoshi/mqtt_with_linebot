簡易主機狀態監測機
----------------

無需架設webhook即可用多台Raspberry pi與DHT11溫溼度來監測各主機狀態與機房溫溼度或自家溫溼度, 監測的狀態會由MQTT將資料傳到broken主機，當監控的伺服器無法連線、溫溼度過高時會透過簡易Line bot推送訊息。

### Broken 主機
```bash
sudo apt-get install mosquitto mosquitto-clients
```

### Requirements (publish and subscribe)

```bash
pip install paho-mqtt 
pip install line-bot-sdk 
```

### Usage
#### subscribe端
``` bash
python ./mqtt_subscribe.py
```

#### publish端 (可以多台)
``` bash
python ./mqtt_publish.py
```

Reference
---------------
* [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
* [Paho-MQTT](https://eclipse.org/paho/clients/python/docs/)
* [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT)
