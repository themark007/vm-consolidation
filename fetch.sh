#!/bin/bash

# Input arguments
compute_node=$1
output_file=$2

# Fetch instance information using the compute node name
instance_info=$(nova list --minimal --host "$compute_node")

# Extract instance IDs and names
echo "Instances for Compute Node: $compute_node" > "$output_file"
echo "$instance_info" | awk 'NR>3 {print "Instance ID:", $2, "Instance Name:", $4}' >> "$output_file"

echo "Instance information saved to $output_file"

