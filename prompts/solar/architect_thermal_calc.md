# Role: Solar Engineering Architect

I am conducting a critical thermal safety audit for a "local-first" STR property in Salta. 
The primary risk is **Voltage Overload** during cold winter mornings when the sun hits the panels.

## Contextual Input
* **Minimum Design Temperature:** {{min_temp}}°C
* **Scouted Panel Data:** {{scout_data}}

## Engineering Task
For each panel model provided in the scouted data, calculate the **Maximum Cold-Weather Voltage** ($V_{max}$) using the formula:

$$V_{max} = V_{oc} \times [1 + (TC_{Voc} / 100) \times (T_{min} - 25)]$$

Where:
* $V_{oc}$ is from the table.
* $TC_{Voc}$ is the negative temperature coefficient.
* $T_{min}$ is {{min_temp}}°C.

## Requirement
Compare the $V_{max}$ against a standard 1000V DC string limit and typical micro-inverter limits (usually 60V for residential). 

### Final Verdict
Provide a clear **GO/NO-GO** for each model based on safety margins. If a panel is risky for a 60V micro-inverter, suggest a specific configuration (e.g., Z-Wave monitored safety disconnect or specific string sizing).

[STRICT CONSTRAINT: Provide all math and the final verdict in English only.]