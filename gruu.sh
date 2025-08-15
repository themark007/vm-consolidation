#!/bin/bash

# Function to fetch parameters of a compute node
get_parameters() {
    ip=$1
    # Command to fetch CPU usage (Replace `mpstat` or equivalent as needed)
    cpu=$(ssh $ip "mpstat 1 1 | awk '/^Average/ {print 100 - \$NF}'")

    # Command to fetch Memory usage (replace with an actual command, e.g., `free`)
    memory=$(ssh $ip "free -m | awk '/Mem:/ {print \$3}'") # Memory in MB

    # Command to fetch Bandwidth usage (replace with a specific tool or value)
    bandwidth=$(ssh $ip "ifstat 1 1 | tail -n 1 | awk '{print \$1}'") # Example with `ifstat`

    # Command to fetch Latency (e.g., use `ping` to a known address)
    latency=$(ping -c 1 -q $ip | awk -F '/' 'END {print (/^rtt/? $5:"-1") }') # Latency in ms

    echo "$cpu $memory $bandwidth $latency"
}

# IP addresses of compute nodes
compute07_ip="192.168.40.29"
compute06_ip="192.168.40.28"
compute04_ip="192.168.40.26"

# Collect parameters for all compute nodes
echo "Fetching parameters for compute nodes..."
compute07_params=$(get_parameters $compute07_ip)
compute06_params=$(get_parameters $compute06_ip)
compute04_params=$(get_parameters $compute04_ip)

# Display parameters
echo "Compute Node 07: $compute07_params (CPU Memory Bandwidth Latency)"
echo "Compute Node 06: $compute06_params (CPU Memory Bandwidth Latency)"
echo "Compute Node 04: $compute04_params (CPU Memory Bandwidth Latency)"

# Pass parameters to the Python script and display predictions
echo "Running predictions with GRU model..."
predictions=$(python3 pred.py $compute07_params $compute06_params $compute04_params)

# Display predictions
echo "Predictions:"
echo "$predictions"

