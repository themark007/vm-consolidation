#!/bin/bash

# Define the input file with instance details
input_file="instances.txt"
id_file="id.txt"

# Check if the input file exists
if [[ ! -f $input_file ]]; then
    echo "Error: $input_file not found."
    exit 1
fi

# Extract the Instance ID from the first line and save it to id.txt
awk 'NR==1 {print $3}' "$input_file" > "$id_file"

# Verify if ID was successfully extracted
if [[ ! -s $id_file ]]; then
    echo "Error: Failed to extract Instance ID."
    exit 1
else
    echo "Instance ID saved to $id_file: $(cat $id_file)"
fi

# Run the Python script
echo "Running python3 scripts.py..."
python3 fck.py

# Check if Python script ran successfully
if [[ $? -ne 0 ]]; then
    echo "Error: Python script failed."
    exit 1
else
    echo "Python script completed successfully."
fi

# Run the cold.sh script
echo "Running ./cold.sh..."
./cold.sh

# Check if cold.sh script ran successfully
if [[ $? -ne 0 ]]; then
    echo "Error: cold.sh script failed."
    exit 1
else
    echo "cold.sh script completed successfully."
fi

echo "migration  completed successfully."

sleep 2

echo "shutting down compute 4 ... "

sleep 10

echo "compute04 is off "

