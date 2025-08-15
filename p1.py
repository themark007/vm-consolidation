import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import GRU, Dense

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the dataset file in the same directory
file_path = os.path.join(script_dir, "compp1.txt")

# Load the dataset
df = pd.read_csv(file_path)

# Compute averages
avg_bandwidth = df['bandwidth'].mean()
avg_latency = df['latency'].mean()
avg_cpu = df['cpu'].mean()
avg_memory = df['memory'].mean()

# Drop latency column if not needed for further processing
df = df.drop('latency', axis=1)

# Convert cpu and memory to float for consistency
df['cpu'] = df['cpu'].astype(float)
df['memory'] = df['memory'].astype(float)

# Function to compute utilization status
def compute_utilization(row):
    if (((row['cpu'] > avg_cpu or row['memory'] > avg_memory) or row['bandwidth'] < avg_bandwidth)):
        return 1
    else:
        return 0

df['status(1-over,0-under)'] = df.apply(compute_utilization, axis=1)

# Prepare features and target
features = df[["cpu", "memory", "bandwidth"]]
target = df["status(1-over,0-under)"]

# Normalize the features
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

# Define LSTM (changed to GRU here) parameters
timesteps = 1  # Adjust based on sequence length
features_count = features.shape[1]

# GRU Model Creation
model = Sequential()
model.add(GRU(units=50, return_sequences=False, input_shape=(timesteps, features_count)))
model.add(Dense(units=1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy')

# Dummy data for testing predictions (replace with actual test data)
X_test_last_sequence = np.random.rand(1, timesteps, features_count)

# Predict the next 20 values
num_predictions = 20
predicted_values = []

for _ in range(num_predictions):
    predicted_value = model.predict(X_test_last_sequence)
    predicted_values.append(predicted_value[0][0])
    X_test_last_sequence = np.append(X_test_last_sequence[:, 0, 1:], [[predicted_value[0][0]]], axis=1)
    X_test_last_sequence = X_test_last_sequence.reshape(1, timesteps, features_count)

median_predicted_value1 = np.mean(predicted_values)

# Print the results
print("Predicted Values for the Next 20 Tuples:", predicted_values)
print("Median Predicted Value:", median_predicted_value1)

