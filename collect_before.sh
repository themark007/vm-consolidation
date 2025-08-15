#!/bin/bash

# Output file for data collection
OUTPUT_FILE="utilization_after.txt"
echo "Collecting data after migration..."
echo "Node,VM,CPU_Utilization" > $OUTPUT_FILE

# Get the list of compute nodes
compute_nodes=$(nova service-list | grep nova-compute | awk '{print $6}')

# Loop through each compute node
for node in $compute_nodes; do
    echo "Connecting to $node..."

    # Collect resource utilization for all VMs on the node
    ssh $node "virsh list --name | grep -v '^$' | while read vm; do
        cpu_time=\$(virsh domstats \$vm | grep 'cpu.time' | awk -F= '{print \$2}')
        cpu_time_ms=\$((cpu_time / 1000000)) # Convert nanoseconds to milliseconds
        echo \"$node,\$vm,\$cpu_time_ms\"
    done" >> $OUTPUT_FILE
done

echo "Data collection after migration completed. Results saved to $OUTPUT_FILE."

