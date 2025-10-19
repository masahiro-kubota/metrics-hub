#!/usr/bin/env python3
import json
import time
import psutil
import paho.mqtt.client as mqtt
import os
from datetime import datetime

# MQTT設定
MQTT_HOST = os.getenv('MQTT_HOST', 'mosquitto')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'hauser')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'hapass')
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'system/memory/usage')
PUBLISH_INTERVAL = int(os.getenv('PUBLISH_INTERVAL', '10'))  # 10秒間隔

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
    else:
        print(f"Failed to connect to MQTT broker, return code {reason_code}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"Disconnected from MQTT broker, return code {reason_code}")

def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Message {mid} published successfully")

def main():
    # MQTTクライアント設定（新しいAPI）
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    
    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_start()
        
        print(f"Starting memory usage publisher to topic: {MQTT_TOPIC}")
        print(f"Publishing interval: {PUBLISH_INTERVAL} seconds")
        
        while True:
            try:
                # メモリ使用量を取得
                memory = psutil.virtual_memory()
                
                # メッセージ作成
                message = {
                    "measurement": "memory",
                    "tags": {
                        "host": "metrics-hub",
                        "type": "virtual"
                    },
                    "fields": {
                        "total": memory.total,
                        "available": memory.available,
                        "used": memory.used,
                        "percent": memory.percent,
                        "free": memory.free,
                        "cached": memory.cached,
                        "buffers": memory.buffers
                    },
                    "timestamp": int(datetime.now().timestamp() * 1000)  # Unix timestamp in milliseconds
                }
                
                # JSON形式でパブリッシュ
                payload = json.dumps(message)
                result = client.publish(MQTT_TOPIC, payload, qos=1)
                
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                    print(f"Published memory usage: {memory.percent:.2f}% ({memory.used / (1024**3):.2f}GB used)")
                else:
                    print(f"Failed to publish message, error code: {result.rc}")
                
                time.sleep(PUBLISH_INTERVAL)
                
            except Exception as e:
                print(f"Error getting memory usage: {e}")
                time.sleep(5)
                
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
