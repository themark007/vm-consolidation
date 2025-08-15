#!/bin/bash

# Define the paths to the files containing the ID and hostname
id_file="id.txt"
hostname_file="compute.txt"

# Read the ID and hostname from the respective files
id=$(cat "$id_file")
hostname=$(cat "$hostname_file")

# Run the nova evacuate command with the collected ID and hostname
nova evacuate "$id" "$hostname"

