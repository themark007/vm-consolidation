import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import GRU, Dense
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# List of compute node filenames and their hostnames
compute_nodes = {
    "compute04": "compp1.txt",
    "compute06": "compp2.txt",
    "compute07": "compp3.txt"
}

threshold = 0.1  # Define a threshold for migration
script_dir = os.path.dirname(os.path.abspath(__file__))
no_migration_node = None  # To store the compute node where migration does not occur

for compute_node, file_name in compute_nodes.items():
    # Load the dataset
    file_path = os.path.join(script_dir, file_name)
    df = pd.read_csv(file_path)

    # Compute averages for resource usage
    avg_cpu = df['cpu'].mean()
    avg_memory = df['memory'].mean()
    avg_bandwidth = df['bandwidth'].mean()
    avg_latency = df['latency'].mean()

    # Ensure data types are correct
    df['cpu'] = df['cpu'].astype(float)
    df['memory'] = df['memory'].astype(float)
    df['bandwidth'] = df['bandwidth'].astype(float)

    # Add a 'status' column based on utilization thresholds
    def compute_utilization(row):
        if row['cpu'] > avg_cpu or row['memory'] > avg_memory or row['bandwidth'] < avg_bandwidth:
            return 1  # Over-utilized
        else:
            return 0  # Under-utilized

    df['status(1-over,0-under)'] = df.apply(compute_utilization, axis=1)

    # Features for the GRU model
    features = df[["cpu", "memory", "bandwidth", "latency"]]
    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)

    # GRU Model creation and prediction
    timesteps = 1
    features_count = features.shape[1]
    model = Sequential()
    model.add(GRU(units=50, return_sequences=False, input_shape=(timesteps, features_count)))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy')

    # Test with the last sequence
    X_test_last_sequence = features_scaled[-1].reshape(1, timesteps, features_count)

    # Predict the next 20 values
    num_predictions = 20
    predicted_values = []
    for _ in range(num_predictions):
        predicted_value = model.predict(X_test_last_sequence)
        predicted_values.append(predicted_value[0][0])
        X_test_last_sequence = np.append(X_test_last_sequence[:, 0, 1:], [[predicted_value[0][0]]], axis=1)
        X_test_last_sequence = X_test_last_sequence.reshape(1, timesteps, features_count)

    median_predicted_value = np.median(predicted_values)

    # Step 2: Check migration requirement
    if median_predicted_value <= threshold:
        no_migration_node = compute_node  # Save the first compute node where migration does not occur
        break  # Exit loop as we only need the first occurrence
    else:
        # Migration is required; call external script to handle instances
        # Assuming the script is `fetch_instances.sh`
        script_path = os.path.join(script_dir, "fetch_instances.sh")
        os.system(f"bash {script_path} {compute_node} instances.txt")

# Save the first hostname where migration does not occur to compute.txt
if no_migration_node:
    with open(os.path.join(script_dir, "compute.txt"), "w") as file:
        file.write(no_migration_node)
else:
    print("Migration is required on all nodes.")

