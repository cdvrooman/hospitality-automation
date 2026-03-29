import os
import sys
from pathlib import Path

# Ensure the 'common' directory is in the path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "common"))

from research_agent import ResearchAgent

def run_solar_validation():
    # Initialize agent (Defaulting to flash for the first step)
    agent = ResearchAgent(model_key="flash")
    
    try:
        # 1. Load the Scenario
        scenario = agent.load_scenario("winter_solar_check")
        print(f"--- Starting: {scenario['scenario_name']} ---")

        # 2. STEP 1: Fast Scout (Temp 0.7)
        # Finds panel specs (Voc, Temp Coeff) in the local market.
        scout_config = scenario['steps'][0]
        scout_results = agent.run_step(scout_config)
        
        if not scout_results:
            print("❌ Step 1 failed or was cancelled. Aborting.")
            return

        # 3. STEP 2: Deep Research Audit (Temp 0.2)
        # Injects scout results into the 'scout_data' variable in the prompt.
        audit_config = scenario['steps'][1]
        
        print("\n--- Chaining Data to Deep Research Agent ---")
        final_verdict = agent.run_step(
            audit_config, 
            context_data={"scout_data": scout_results},
            is_chained=True
        )

        if final_verdict:
            print("\n✅ Engineering Audit Complete.")
            # Focus on the 'Recommendation' section of the output
            if "GO" in final_verdict or "NO-GO" in final_verdict:
                print("--- Final Verdict Found in Research Log ---")

    except FileNotFoundError as e:
        print(f"❌ Path Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_solar_validation()    