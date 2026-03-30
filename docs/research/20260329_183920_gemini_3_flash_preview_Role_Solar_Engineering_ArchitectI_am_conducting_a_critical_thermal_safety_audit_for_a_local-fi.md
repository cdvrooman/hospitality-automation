# Research Instance: 20260329_183920

**To:** Project Stakeholders / Engineering Team
**From:** Senior Systems Architect
**Subject:** Thermal Safety Audit & Voltage Overload Analysis – Casa Kolla 2.0
**Project Code:** AntiGravity-Solar-01-TSA

### **1. Executive Summary**
This audit evaluates the risk of DC voltage spikes during cold-start conditions in Salta Capital. Given the deployment of **Enphase IQ8P Microinverters**, the critical failure point is the **60V DC Maximum Input Voltage**. Exceeding this threshold results in immediate hardware decommissioning (permanent failure). 

The following calculations utilize the design minimum temperature of **-5°C** to determine the maximum Open Circuit Voltage ($V_{max}$).

---

### **2. Mathematical Analysis**

**Constants:**
*   $T_{min} = -5°C$
*   $T_{ref} = 25°C$
*   $\Delta T = (T_{min} - T_{ref}) = -30°C$

#### **A. Jinko Tiger Neo N-Type (JKM475N-60HL4-V)**
*   $V_{oc}: 42.54V$
*   $TC_{Voc}: -0.25\%/°C$
*   **Calculation:**
    *   $V_{max} = 42.54 \times [1 + (-0.0025 \times -30)]$
    *   $V_{max} = 42.54 \times [1 + 0.075]$
    *   $V_{max} = 42.54 \times 1.075$
    *   **$V_{max} = 45.73V$**

#### **B. Longi Hi-MO 6 Explorer (LR5-54HTH-450M)**
*   $V_{oc}: 39.63V$
*   $TC_{Voc}: -0.23\%/°C$
*   **Calculation:**
    *   $V_{max} = 39.63 \times [1 + (-0.0023 \times -30)]$
    *   $V_{max} = 39.63 \times [1 + 0.069]$
    *   $V_{max} = 39.63 \times 1.069$
    *   **$V_{max} = 42.36V$**

#### **C. Canadian Solar HiKu6 (CS6R-450MS)**
*   $V_{oc}: 41.0V$
*   $TC_{Voc}: -0.26\%/°C$
*   **Calculation:**
    *   $V_{max} = 41.0 \times [1 + (-0.0026 \times -30)]$
    *   $V_{max} = 41.0 \times [1 + 0.078]$
    *   $V_{max} = 41.0 \times 1.078$
    *   **$V_{max} = 44.20V$**

---

### **3. Comparative Safety Audit**

| Model | $V_{max}$ (-5°C) | Margin to 60V Limit | Margin to 1000V String | Verdict |
| :--- | :---: | :---: | :---: | :--- |
| **Jinko Tiger Neo** | 45.73V | 23.78% | N/A (Micro) | **GO** |
| **Longi Hi-MO 6** | 42.36V | 29.40% | N/A (Micro) | **GO (Optimal)** |
| **Canadian Solar** | 44.20V | 26.33% | N/A (Micro) | **GO** |

---

### **4. Final Verdict & Architectural Directives**

#### **The "GO" Decision**
All three modules are **technically safe** for use with the Enphase IQ8P microinverters. Even under extreme thermal contraction, the voltage remains significantly below the 60V hardware limit. 

#### **The "AntiGravity" Recommendation: Longi Hi-MO 6**
While all are safe, the **Longi Hi-MO 6** is the superior choice for the following reasons:
1.  **Highest Safety Buffer:** It provides a ~30% headroom against voltage spikes, which is critical if Salta experiences an anomalous "Black Swan" weather event (e.g., -15°C).
2.  **Microinverter Optimization:** The lower $V_{oc}$ allows the microinverter to stay within its optimal MPPT tracking range longer during high-irradiance/low-temp mornings.

#### **Fault Tolerance & Fallback Protocols**
Since we are using a **Local-First** architecture, the following must be implemented:
*   **No Safety Disconnect Required:** Because we are using Microinverters (AC-coupled system), the risk of a high-voltage DC arc-flash is localized to the 1.5-meter cable between the panel and the IQ8P. We do not require a Z-Wave safety disconnect for the DC side; the Enphase system will naturally "Rapid Shutdown" via the PLC (Power Line Communication) if the Envoy detects a grid anomaly.
*   **Monitoring:** The **Node-RED** instance on the Raspberry Pi 4 must pull data from the Enphase Envoy local API every 60 seconds. If any single microinverter reports an input voltage $>55V$, a high-priority alert must be pushed to the Zoho CRM/Maintenance dashboard.
*   **Inductive Load Management:** Ensure that the **Shelly Pro DIN** relays managing the water heaters are interlocked via Node-RED logic to prevent "Load Shedding" during peak solar production, which could cause local AC voltage rises at the microinverter output.

**Status: APPROVED FOR PROCUREMENT.** Proceed with the **Longi Hi-MO 6** baseline.