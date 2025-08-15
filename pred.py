import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import GRU, Dense

# Load the dataset
df = pd.read_csv("/content/drive/MyDrive/Compute node dataset/compp1.txt")

# Compute averages for relevant columns
avg_bandwidth = df['bandwidth'].mean()
avg_latency = df['latency'].mean()
avg_cpu = df['cpu'].mean()
avg_memory = df['memory'].mean()

# Drop unnecessary columns
df = df[['cpu', 'memory', 'bandwidth', 'latency']]  # Use only selected features
df['cpu'] = df['cpu'].astype(float)
df['memory'] = df['memory'].astype(float)

# Function to compute utilization status
def compute_utilization(row):
    if (((row['cpu'] > avg_cpu or row['memory'] > avg_memory) or row['bandwidth'] < avg_bandwidth) and row['latency'] > avg_latency):
        return 1
    else:
        return 0

# Apply the function to create the target column
df['status(1-over,0-under)'] = df.apply(compute_utilization, axis=1)

# Prepare features and target
features = df[['cpu', 'memory', 'bandwidth', 'latency']]
target = df['status(1-over,0-under)']

# Scale features
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

# Convert data to sequences
timesteps = 1  # Adjust based on desired sequence length
features_scaled = features_scaled.reshape(features_scaled.shape[0], timesteps, features_scaled.shape[1])

# Define the GRU model
model = Sequential()
model.add(GRU(50, input_shape=(timesteps, features_scaled.shape[2]), return_sequences=False))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Assume the data is split into training and test sets
# Example: 80% training, 20% testing
split = int(0.8 * len(features_scaled))
X_train, X_test = features_scaled[:split], features_scaled[split:]
y_train, y_test = target[:split], target[split:]

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Initialize the last sequence for predictions
X_test_last_sequence = X_test[-1].reshape(1, timesteps, features_scaled.shape[2])

num_predictions = 20
predicted_values = []

for _ in range(num_predictions):
    predicted_value = model.predict(X_test_last_sequence)
    predicted_values.append(predicted_value[0][0])
    
    # Update the input sequence for the next prediction
    X_test_last_sequence = np.append(X_test_last_sequence[:, 0, 1:], [[predicted_value[0][0]]], axis=1)
    X_test_last_sequence = X_test_last_sequence.reshape(1, timesteps, features_scaled.shape[2])

# Calculate and print the median predicted value
median_predicted_value = np.mean(predicted_values)
print("Median Predicted Value:", median_predicted_value)

# Output the predicted values
print("Predicted Values for the Next 20 Tuples:", predicted_values)

