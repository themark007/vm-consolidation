import openstack
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Step 1: Connect to OpenStack using the environment variables (ensure you've sourced the RC file)
conn = openstack.connect()

# Step 2: Read Instances from instances.txt
instances = []
with open("instances.txt", "r") as file:
    instance = {}
    for line in file:
        if line.startswith("Instance ID"):
            instance["Instance_ID"] = line.split(":")[1].strip()
        if line.startswith("Instance Name"):
            instance["Instance_Name"] = line.split(":")[1].strip()
            instances.append(instance)
            instance = {}  # Reset for the next instance

# Step 3: Fetch CPU Utilization for Each Instance
instance_cpu_util = {}
for instance in instances:
    instance_id = instance["Instance_ID"]
    instance_name = instance["Instance_Name"]
    
    # Fetching CPU utilization from OpenStack Telemetry (Ceilometer/Gnocchi)
    try:
        metrics = conn.telemetry.query_samples(
            meter_name="cpu_util", q=[{"field": "resource_id", "value": instance_id}]
        )
        cpu_util = sum(sample.volume for sample in metrics) / len(metrics) if metrics else 0
        if cpu_util == 0:  # Fallback in case of no data
            cpu_util = 100  # Assign a high value to indicate overutilization
        instance_cpu_util[instance_id] = cpu_util
    except Exception as e:
        print(f"Error fetching CPU utilization for {instance_name}: {e}")
        instance_cpu_util[instance_id] = 100  # Assign a high value in case of error

# Step 4: Debugging: Print CPU Utilization Data
print("CPU Utilization Data:")
for instance_id, cpu_util in instance_cpu_util.items():
    print(f"Instance ID: {instance_id}, CPU Utilization: {cpu_util}")

# Step 5: ILP Model to Select the Instance
problem = LpProblem("Instance_Selection", LpMinimize)

# Variables: Whether to select each instance (binary variable)
variables = {id: LpVariable(f"select_{id}", 0, 1, cat="Binary") for id in instance_cpu_util}

# Objective: Minimize CPU utilization of the selected instance
problem += lpSum(variables[id] * instance_cpu_util[id] for id in instance_cpu_util)

# Constraint: Select exactly one instance
problem += lpSum(variables.values()) == 1

# Solve the ILP Problem
problem.solve()

# Step 6: Save the Selected Instance ID
selected_instance = None
for id, var in variables.items():
    if var.varValue == 1:
        selected_instance = id
        break

if selected_instance:
    with open("id.txt", "w") as file:
        file.write(selected_instance)
    print(f"Selected Instance ID: {selected_instance} (saved to id.txt)")
else:
    print("No instance was selected.")

