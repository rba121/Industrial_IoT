# import pandas as pd
# df = pd.read_csv("sensor_data.csv")

# print(df.head())
# print(df.describe())
# print(df.isnull().sum())

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


df = pd.read_csv("sensor_data.csv")


df["timestamp"] = pd.to_datetime(df["timestamp"])

plt.figure(figsize=(12,6))
plt.plot(df["timestamp"], df["temperature"], label="Temperature (°C)", alpha=0.7)
plt.plot(df["timestamp"], df["humidity"], label="Humidity (%)", alpha=0.7)
plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Raw Sensor Readings")
plt.legend()
plt.grid(True)
plt.show()

#Smoothen data values(reduce noise)
df["temp_avg"] = df["temperature"].rolling(window=30).mean()
df["hum_avg"] = df["humidity"].rolling(window=30).mean()

plt.figure(figsize=(12,6))
plt.plot(df["timestamp"], df["temp_avg"], label="Temperature Rolling Avg", color="red")
plt.plot(df["timestamp"], df["hum_avg"], label="Humidity Rolling Avg", color="blue")
plt.xlabel("Time")
plt.ylabel("Smoothed Value")
plt.title("Smoothed Sensor Trends")
plt.legend()
plt.grid(True)
plt.show()

#Normalization of values
features = ["temp_norm","hum_norm"] 
scaler = MinMaxScaler() 
df[features] = scaler.fit_transform(df[["temperature","humidity"]])

#drop NAN values
df=df.dropna()

print(df.head())
print(df.describe())