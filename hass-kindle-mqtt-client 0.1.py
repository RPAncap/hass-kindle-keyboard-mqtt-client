import json
import time
import struct
import paho.mqtt.client as mqtt
import sys
import threading
import os
import subprocess

# ================== CONFIGURATION ==================
MQTT_BROKER = "192.168.1.1"      # Change to your HA IP 
MQTT_PORT = 1883
MQTT_USER = "AAAA"               # Change to your Mosquitto Broker Login     
MQTT_PASSWORD = "BBBB"        # Change to your Mosquitto Broker Login      

DEVICE_ID = "kindle_keyboard"
DEVICE_NAME = "Kindle 3 keyboard"

# Kindle 3 keymap; what button code corresponds to what key
# If you have kindle 4 you can test yourself and modify this key_map
KEY_MAP = {
    16: "button_Q",
    17: "button_W",
    18: "button_E",
    19: "button_R",
    20: "button_T",
    21: "button_Y",
    22: "button_U",
    23: "button_I",
    24: "button_O",
    25: "button_P",
    30: "button_A",
    31: "button_S",
    32: "button_D",
    33: "button_F",
    34: "button_G",
    35: "button_H",
    36: "button_J",
    37: "button_K",
    38: "button_L",
    44: "button_Z",
    45: "button_X",
    46: "button_C",
    47: "button_V",
    48: "button_B",
    49: "button_N",
    50: "button_M",
    139: "button_menu",
    14: "button_del",
    52: "button_dot",
    126: "button_sym",
    28: "button_enter",
    42: "button_shift",
    57: "button_space",
    190: "button_font",
    102: "button_home",
    158: "button_back",
    193: "button_leftpageturn_left",
    104: "button_leftpageturn_right",
    109: "button_rightpageturn_left",
    191: "button_rightpageturn_right",

    # You can add any text command here
}


# ===================================================

# Path to the main keyboard input device on Kindle 3
INPUT_DEVICE = "/dev/input/event0"
EVENT_FORMAT = 'llHHi'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)


# === CLIENT CREATION ===
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,         
    client_id=f"rp-{DEVICE_ID}"
)



if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("✅ Connected to MQTT broker")
        send_autodiscovery()
    else:
        print(f"❌ Failed to connect: {rc}")

def send_autodiscovery():
    print("📡 Sending device discovery...")

    for trigger_name in KEY_MAP.values():
        config = {
            "automation_type": "trigger",
            "type": "button_short_press",
            "subtype": trigger_name,
            "topic": f"{DEVICE_ID}/events",
            "payload": trigger_name,
            "platform": "mqtt",
            "device": {
                "identifiers": [DEVICE_ID],
                "name": DEVICE_NAME,
                "model": "Kindle 3 MQTT Keyboard Trigger",
                "manufacturer": "RP"
            }
        }

        discovery_topic = f"homeassistant/device_automation/{DEVICE_ID}_{trigger_name}/config"

        client.publish(discovery_topic, json.dumps(config), qos=1, retain=True)
        print(f"   → Registered: {trigger_name}")

def publish_trigger(command):
    client.publish(f"{DEVICE_ID}/events", command, qos=0, retain=False)
    print(f"🔘 Sent trigger: {command}")

# ====================== START ======================
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)

threading.Thread(target=client.loop_forever, daemon=True).start()

time.sleep(1.5)

print("Kindle 3 MQTT Keyboard Trigger by RP")
print(f"Listening on {INPUT_DEVICE}")
print("Press keys on the physical keyboard...")
print("Press Ctrl+C to stop (if running in foreground)\n")


def main():
    try:
        with open(INPUT_DEVICE, "rb") as f:
            while True:
                event = f.read(EVENT_SIZE)
                if len(event) == EVENT_SIZE:
                    tv_sec, tv_usec, etype, code, value = struct.unpack(EVENT_FORMAT, event)
                    
                    # Only process key events (type 1 = EV_KEY)
                    if etype == 1 and value == 1:   # value=1 means key pressed (not released)
                        try:
                            if code in KEY_MAP:
                                trigger = KEY_MAP[code]
                                publish_trigger(trigger)
                                text1 = f"[{time.strftime('%H:%M:%S')}] Key : {KEY_MAP[code]}"
                            else:
                                text1 = f"[{time.strftime('%H:%M:%S')}] Key not in Keymap. code: {code}"
                            
                            print(text1)
                            subprocess.run(["eips", "1", "38", "                                               "])
                            subprocess.run(["eips", "1", "38", text1])



                          
                        except:
                            print(f"[{time.strftime('%H:%M:%S')}] Key pressed - Code: {code}  {KEY_MAP[code]}")
                            
    except PermissionError:
        print("❌ Permission denied. Run with root (su) or fix permissions.")
    except FileNotFoundError:
        print(f"❌ Device {INPUT_DEVICE} not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # You may need root for this
    if os.geteuid() != 0:
        print("⚠️  This script works better as root.")
        print("Try: su -c '/usr/bin/python3 /mnt/us/kindle_key_bg.py'")
    main()


