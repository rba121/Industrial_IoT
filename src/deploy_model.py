import joblib
import pandas as pd
import time
import board
import adafruit_dht

# Load trained model
model = joblib.load("sensor_predict_model.pkl")

# CSV log file
log_file = "deployment_log.csv"

# Create log file if not exists
try:
    pd.read_csv(log_file)
except FileNotFoundError:
    with open(log_file, "w") as f:
        f.write("timestamp,real_temp,real_hum,predicted_temp,predicted_hum\n")

# Initialize DHT22 sensor on GPIO4
dhtDevice = adafruit_dht.DHT22(board.D4)

past_temp, past_hum = [], []

while True:
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        if humidity is not None and temperature is not None:
            print(f"Real reading -> Temp: {temperature:.1f}°C  Hum: {humidity:.1f}%")

            past_temp.append(temperature)
            past_hum.append(humidity)

            if len(past_temp) > 3:
                past_temp.pop(0)
                past_hum.pop(0)

            if len(past_temp) == 3:
                features = ["temp_lag1", "temp_lag2", "temp_lag3", 
                            "hum_lag1", "hum_lag2", "hum_lag3"]

                X = pd.DataFrame([[past_temp[0], past_temp[1], past_temp[2],
                                    past_hum[0], past_hum[1], past_hum[2]]],
                                    columns=features)

                

                predicted_temp, predicted_hum = model.predict(X)[0]

                print(f"Predicted next temperature: {predicted_temp:.2f}°C")
                print(f"Predicted next humidity: {predicted_hum:.2f}%")

                with open(log_file, "a") as f:
                    ts = pd.Timestamp.now()
                    f.write(f"{ts},{temperature:.2f},{humidity:.2f},{predicted_temp:.2f},{predicted_hum:.2f}\n")

    except RuntimeError as error:
        print(f"Sensor error: {error.args[0]}")

    time.sleep(2)

