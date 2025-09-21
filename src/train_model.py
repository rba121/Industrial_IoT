import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt


df = pd.read_csv("cleaned_data.csv")

df["temp_lag1"] = df["temperature"].shift(1)
df["temp_lag2"] = df["temperature"].shift(2)
df["temp_lag3"] = df["temperature"].shift(3)

df["hum_lag1"] = df["humidity"].shift(1)
df["hum_lag2"] = df["humidity"].shift(2)
df["hum_lag3"] = df["humidity"].shift(3)

df = df.dropna()

features = ["temp_lag1","temp_lag2","temp_lag3","hum_lag1","hum_lag2","hum_lag3"]
X = df[features]
y = df[["temperature","humidity"]]   

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle = False)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mean = mean_squared_error(y_test, y_pred)
print("Mean Squared Error: ", mean)

joblib.dump(model, "sensor_predict_model.pkl")


plt.figure(figsize=(10,5))
plt.plot(y_test.values, label="Actual", alpha=0.7)
plt.plot(y_pred, label="Predicted", alpha=0.7)
plt.legend()
plt.title("Actual vs Predicted Sensor Values")
plt.show()