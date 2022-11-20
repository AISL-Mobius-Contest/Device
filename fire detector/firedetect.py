import serial
import requests
import json
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            time.sleep(3)
            line = ser.readline().decode('utf-8').rstrip()
            room_data = line.split()
            if room_data.__len__() != 1:
                gas_sensor_url = "XXX"
                fire_sensor_url = "XXX"
                
                fire_data_payload = {}
                gas_data_payload = {}
                fire_data_payload["m2m:cin"] = {"con":room_data[2]}
                gas_data_payload["m2m:cin"] = {"con":room_data[4]}
                fire_data_payload = json.dump(fire_data_payload)
                gas_data_payload = json.dump(gas_data_payload)
                headers = {
                    'Accept': 'application/json',
                    'X-M2M-RI': '12345',
                    'X-M2M-Origin': 'SOrigin',
                    'Content-Type': 'application/json;ty=4'
                }
                
                response = requests.request("POST", fire_sensor_url, headers=headers, data=fire_data_payload)
                response = requests.request("POST", fire_sensor_url, headers=headers, data=gas_data_payload)