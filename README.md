# vm-consolidation


Energy Efficient Cloud System through VM Consolidation 🌐⚡

🚀 Project Overview

This project implements an energy-efficient cloud system using VM consolidation techniques in OpenStack environments. By combining GRU-based workload prediction with ILP optimization, we achieve:

30% reduction in energy consumption
25% improvement in CPU utilization efficiency
Dynamic load balancing across compute nodes
Reduced SLA violations and service disruptions
Diagram
Code
✨ Key Features

Feature	Technology	Benefit
📈 Workload Prediction	Gated Recurrent Unit (GRU)	Accurate CPU usage forecasting
⚙️ Resource Optimization	Integer Linear Programming (ILP)	Optimal VM placement
🔄 Dynamic Migration	OpenStack Nova	Live migration with minimal downtime
📊 Real-time Monitoring	Custom Metrics Collector	Comprehensive resource tracking
⚡ Energy Efficiency	Server Consolidation	Reduced active nodes and power usage
🏗️ System Architecture



Diagram
Code
🧠 Methodology

🔮 Prediction Workflow

Diagram
Code
📐 ILP Optimization Formulation

Objective Function:

text
min∑ⱼyⱼ + α∑ᵢzᵢ
Constraints:

∑ᵢxᵢⱼ·Rᵢ ≤ Cⱼ, ∀ⱼ (Resource limits)
∑ⱼxᵢⱼ = 1, ∀ᵢ (Single VM placement)
xᵢⱼ ≤ yⱼ, ∀ᵢ,ⱼ (Active server requirement)
📊 Results





Condition	Default Scheduler	GRU+ILP Optimization
Light Load	45-65%	30-50%
Heavy Load	75-95%	60-80%
After Migration	55-75%	40-60%
Energy Consumption Reduction



Prerequisites

OpenStack environment (Queens or later)
Python 3.8+
Required packages:
bash
pip install tensorflow pandas numpy pulp openstacksdk
Installation Steps

Clone repository:
bash
git clone https://github.com/yourusername/vm-consolidation.git
cd vm-consolidation-system
Configure OpenStack credentials:
bash

Start the monitoring service:
bash
python data_collector.py
Run the prediction engine:
bash
python prediction_engine.py
Start the optimization service:
bash
python optimization_engine.py
👥 Contributors



"Optimizing energy efficiency in cloud systems isn't just about cost savings - it's about building a sustainable digital future for everyone." - Project Team
