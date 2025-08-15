#!/bin/bash

# Ensure the correct number of arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <compute_node> <output_file>"
    exit 1
fi

# Input arguments from the script
compute_node=$1
output_file=$2

# Initialize or clear the output file
: > "$output_file"

# Fetch instance information for the specified compute node
instance_info=$(nova list --minimal --host "$compute_node" 2>&1)

# Check if the nova command was successful
if [[ $? -ne 0 ]]; then
    echo "Error fetching instance information: $instance_info"
    exit 1
fi

# Extract instance IDs and names and save to the output file
echo "$instance_info" | awk 'NR > 3 && $2 != "" {print "Instance ID:", $2, "Instance Name:", $4}' >> "$output_file"

# Check if output file is not empty
if [[ -s $output_file ]]; then
    echo "Instance information saved to $output_file"
else
    echo "No instances found on compute node $compute_node."
    rm -f "$output_file"  # Clean up empty file
    exit 1
fi

exit 0

