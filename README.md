# 🌐⚡ Energy-Efficient Cloud System through VM Consolidation

> **"Optimizing energy efficiency in cloud systems isn't just about cost savings – it's about building a sustainable digital future for everyone."** – Project Team

---

## 🚀 Project Overview

This project implements an **energy-efficient cloud system** using **Virtual Machine (VM) consolidation techniques** in **OpenStack** environments.  
By combining **GRU-based workload prediction** with **ILP optimization**, we achieve:

- 🔋 **30% reduction in energy consumption**
- 💻 **25% improvement in CPU utilization efficiency**
- 🔄 Dynamic load balancing across compute nodes
- 🛡️ Reduced SLA violations and service disruptions

---

## ✨ Key Features

| Feature               | Technology                        | Benefit                                      |
|-----------------------|-----------------------------------|----------------------------------------------|
| 📈 Workload Prediction | Gated Recurrent Unit (GRU)        | Accurate CPU usage forecasting               |
| ⚙️ Resource Optimization | Integer Linear Programming (ILP) | Optimal VM placement                         |
| 🔄 Dynamic Migration   | OpenStack Nova                    | Live migration with minimal downtime         |
| 📊 Real-time Monitoring| Custom Metrics Collector          | Comprehensive resource tracking               |
| ⚡ Energy Efficiency   | Server Consolidation              | Reduced active nodes and power usage         |

---

## 🏗️ System Architecture

![System Architecture](https://github.com/user-attachments/assets/3dd36843-5aa6-4933-8d08-880f7cbeba69)

---

## 🧠 Methodology

### 🔮 Prediction Workflow
![Prediction Workflow](https://github.com/user-attachments/assets/6dfe5efe-d6b4-4255-accc-39e0501fb91d)

---

### 📐 ILP Optimization Formulation

![ILP Formulation](https://github.com/user-attachments/assets/80696102-9b28-41d5-9c59-c5d08ed25655)

**Objective Function:**


**Constraints:**
1. **Resource Limits:**  
   ∑ᵢ xᵢⱼ · Rᵢ ≤ Cⱼ, ∀ⱼ  
2. **Single VM Placement:**  
   ∑ⱼ xᵢⱼ = 1, ∀ᵢ  
3. **Active Server Requirement:**  
   xᵢⱼ ≤ yⱼ, ∀ᵢ,ⱼ  

---

## 📊 Results

| Condition       | Default Scheduler (%) | GRU+ILP Optimization (%) |
|-----------------|-----------------------|--------------------------|
| Light Load      | 45–65                  | 30–50                    |
| Heavy Load      | 75–95                  | 60–80                    |
| After Migration | 55–75                  | 40–60                    |

**Energy Consumption Reduction:** ~30%

---

## 📦 Prerequisites

- **OpenStack** environment (Queens or later)
- **Python 3.8+**
- Required packages:
- install openstack multinode setup
```bash
pip install tensorflow pandas numpy pulp 
git clone https://github.com/themark007/vm-consolidation.git
cd vm-consolidation

source openrc.sh
or
source creds


# Start monitoring
python fck.py

# Run prediction engine
./run.sh

```



