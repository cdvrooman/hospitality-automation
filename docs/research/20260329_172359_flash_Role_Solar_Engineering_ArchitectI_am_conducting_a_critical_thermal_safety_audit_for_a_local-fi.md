# Research Instance: 20260329_172359

### **Executive Summary: Thermal Safety Audit for Casa Kolla 2.0**
**Project:** Casa Kolla 2.0 – Salta Capital, Argentina.
**Subject:** Cold-Weather $V_{oc}$ Analysis for Solar Array Resilience.
**Target Hardware:** Enphase IQ8P Micro-inverters (Max Input: 60V DC).
**Environmental Parameter:** $T_{min} = -5^\circ C$ (Design Minimum).

In high-altitude environments like Salta (1,200m ASL), the combination of high irradiance and low ambient temperatures creates a high-risk scenario for "Cold Start" over-voltage. If the $V_{max}$ exceeds the inverter's maximum input voltage, the DC-side MOSFETs will suffer catastrophic failure. 

---

### **1. Mathematical Analysis: Maximum Cold-Weather Voltage ($V_{max}$)**

The following calculations utilize the standard industry formula for temperature-corrected Open Circuit Voltage at $T_{min} = -5^\circ C$ ($\Delta T = -30^\circ C$ from STC).

| Brand/Model | $V_{oc}$ (STC) | $TC_{Voc}$ | Calculation ($V_{oc} \times [1 + (TC \times -30)/100]$) | **$V_{max}$ @ -5°C** |
| :--- | :--- | :--- | :--- | :--- |
| **Jinko Tiger Neo** | 42.71 V | -0.25% | $42.71 \times [1 + 0.075]$ | **45.91 V** |
| **Longi Hi-MO 6** | 39.12 V | -0.23% | $39.12 \times [1 + 0.069]$ | **41.82 V** |
| **Canadian Solar** | 41.00 V | -0.26% | $41.00 \times [1 + 0.078]$ | **44.20 V** |
| **Risen Titan S** | 41.30 V | -0.25% | $41.30 \times [1 + 0.075]$ | **44.40 V** |

---

### **2. Inverter Compatibility & Safety Margin Audit**

#### **A. Micro-inverter Configuration (Enphase IQ8P)**
*   **Limit:** 60V DC (Absolute Maximum).
*   **Analysis:** All scouted models remain well below the 60V threshold. The **Jinko Tiger Neo** presents the highest voltage at **45.91V**, leaving a safety margin of **23.4%**. Even in an extreme "Black Swan" event where temperatures drop to **-15°C**, the Jinko would hit **46.98V**, still safely within the IQ8P operating envelope.

#### **B. String Inverter Configuration (Standard 1000V DC)**
*   **Limit:** 1000V DC.
*   **Analysis:** For a standard string architecture, the maximum number of modules per string is limited by the $V_{max}$ to prevent total string over-voltage.
    *   **Jinko:** Max 21 panels per string.
    *   **Longi:** Max 23 panels per string.
    *   **Canadian/Risen:** Max 22 panels per string.

---

### **3. Final Verdict & Architectural Recommendations**

| Model | Verdict | Engineering Justification |
| :--- | :--- | :--- |
| **Jinko Tiger Neo** | **GO (PREMIUM)** | Highest efficiency and N-Type resilience. Despite higher $V_{oc}$, it is perfectly matched for IQ8P micro-inverters. Best for Salta’s high UV. |
| **Longi Hi-MO 6** | **GO (AESTHETIC)** | Lowest $V_{max}$ provides the widest safety margin. Ideal if the design requires "All-Black" modules for the "Mestizaje Elegante" look. |
| **Canadian Solar** | **GO (LOGISTIC)** | Solid performance. High local availability in the NOA region makes this the best choice for long-term maintenance/replacement. |
| **Risen Titan S** | **GO (BUDGET)** | Acceptable margins. Use only if Jinko or Canadian Solar stock is unavailable. |

---

### **4. Critical Implementation Directives (The "AntiGravity" Protocol)**

To ensure the "Local-First" resilience of Casa Kolla 2.0, the following systems must be implemented:

1.  **Edge Monitoring (Fault Tolerance):**
    *   The **Enphase Envoy-S** must be polled locally via **Node-RED** (Raspberry Pi 4) using the `/production.json` endpoint. 
    *   **Logic:** If any micro-inverter reports an "Input Overvoltage" flag, trigger a high-priority notification to the property manager via **Zoho CRM** and log the specific panel coordinates for inspection.

2.  **Physical Protection (Hail & Wind):**
    *   Salta is prone to severe summer hail. While these panels are Tier-1 rated, the architectural mounting must include **35mm anodized aluminum rails** with stainless steel mid-clamps. Do not use plastic or "hobbyist" mounting kits.

3.  **DC/AC Isolation:**
    *   Each branch of IQ8P micro-inverters must terminate in a dedicated **AC Combiner Box** with a **20A Double-Pole Circuit Breaker** and a **Type 2 Surge Protective Device (SPD)** (e.g., Schneider Electric or Phoenix Contact) to protect against EDESA grid spikes.

4.  **Fallback Scenario:**
    *   **What happens if the grid fails during a cold morning?** The IQ8P (if paired with IQ System Controller 3) will form a microgrid. The $V_{max}$ remains critical here as the system will be "Cold Starting" without grid reference. The calculated margins confirm that the hardware will not fry during an off-grid transition in winter.

**Status:** **APPROVED.** Proceed with procurement of **Jinko Tiger Neo** or **Longi Hi-MO 6** based on aesthetic preference. The thermal risk is mitigated.