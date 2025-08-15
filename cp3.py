import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import GRU, Dense
from pulp import LpMinimize, LpProblem, LpVariable, lpSum

# Step 1: Load and preprocess compute node data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "compp3.txt")
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
threshold = 0.6  # Define a threshold for migration

# Step 2: Decide if migration is needed
if median_predicted_value > threshold:
    print("Median exceeds threshold. Proceeding with migration...")

    # Step 3: Apply ILP for migration decision
    node_ids = df.index.tolist()
    cpu = df['cpu'].tolist()
    memory = df['memory'].tolist()
    bandwidth = df['bandwidth'].tolist()

    max_cpu = 0.8 * sum(cpu)  # Example constraint: CPU after migration
    max_memory = 0.8 * sum(memory)  # Example constraint: Memory after migration

    # Define ILP problem
    prob = LpProblem("Migration_Optimization", LpMinimize)

    # Decision variables: 1 if node is migrated, 0 otherwise
    x = LpVariable.dicts("x", node_ids, cat="Binary")

    # Objective function: Minimize the number of migrations
    prob += lpSum(x[i] for i in node_ids)

    # Constraints
    prob += lpSum(cpu[i] * x[i] for i in node_ids) <= max_cpu, "CPU_Constraint"
    prob += lpSum(memory[i] * x[i] for i in node_ids) <= max_memory, "Memory_Constraint"

    # Solve the problem
    prob.solve()

    # Output migration decision
    for i in node_ids:
        if x[i].varValue == 1:
            print(f"Node {i} is selected for migration.")
else:
    print("Median does not exceed threshold. No migration required.")

