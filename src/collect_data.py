# ##Data Collect 
#
# import time
# import board
# import adafruit_dht

# dhtDevice = adafruit_dht.DHT22(board.D4)

# while True:
#     try:
#         temp_c = dhtDevice.temperature
#         humidity = dhtDevice.humidity
#         print(f"Temp: {temp_c:.1f}°C   Humidity: {humidity:.1f}%")
#     except RuntimeError as error:
        
#         print(error.args[0])
#     time.sleep(2)
#
#

import csv
import time
import board
import adafruit_dht

dht_device = adafruit_dht.DHT22(board.D4)

csv_file = "sensor_data.csv"

with open(csv_file, mode="a", newline="") as file:
    writer = csv.writer(file)
    if file.tell() == 0:  # file is empty
        writer.writerow(["timestamp", "temperature", "humidity"])


try:
    while True:
        try:
            temp = dht_device.temperature
            hum = dht_device.humidity
            ts = time.strftime("%Y-%m-%d %H:%M:%S")

            if temp is not None and hum is not None:
                with open(csv_file, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([ts, temp, hum])
                print(f"{ts} | Temp: {temp:.1f}°C  Hum: {hum:.1f}%")

        except RuntimeError as e:
            print(f"Sensor read error: {e}")
            time.sleep(2)
            continue

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped logging.")






