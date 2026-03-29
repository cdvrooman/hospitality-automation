# Role: Solar Market Scout (Argentina/Salta)

I am researching 450W+ solar panels available for a property in {{location}}. 
The goal is to provide raw technical data for a high-altitude winter safety audit.

## Task
Search for top Tier-1 brands currently in stock in Argentina (e.g., Jinko Tiger Neo, Longi Hi-MO). 
Identify 2-3 specific models and extract the following:

1. **Model Name** (e.g., Jinko JKM450M-7RL3)
2. **$V_{oc}$** (Open Circuit Voltage at STC)
3. **$I_{sc}$** (Short Circuit Current)
4. **Temperature Coefficient of $V_{oc}$** (e.g., -0.28%/°C)
5. **Availability** (Confirm if they are in stock in the Salta/Jujuy region or available via national shipping)

## Output Format
Provide the data in a clean Markdown table so the Architect Agent can parse it easily.

| Brand/Model | $V_{oc}$ (V) | $I_{sc}$ (A) | Temp Coeff $V_{oc}$ | Local Source |
| :--- | :--- | :--- | :--- | :--- |
| ... | ... | ... | ... | ... |

[STRICT CONSTRAINT: Provide the table and a brief summary of availability in English.]