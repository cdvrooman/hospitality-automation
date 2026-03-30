import os
import sys
from pathlib import Path

# Ensure the 'common' directory is in the path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "common"))

from config import AI_MODELS, AI_TEMP_PRECISE, AI_TEMP_CREATIVE
from research_agent import ResearchAgent

def run_solar_validation():
    # Initialize agent (Defaulting to speed for the first step)
    agent = ResearchAgent(model_id=AI_MODELS["speed"])
    
    try:
        # 1. Load the Scenario
        scenario = agent.load_scenario("winter_solar_check")
        print(f"--- Starting: {scenario['scenario_name']} ---")

        # 2. STEP 1: Fast Scout (Temp AI_TEMP_CREATIVE)
        # Finds panel specs (Voc, Temp Coeff) in the local market.
        scout_config = scenario['steps'][0]
        scout_model = AI_MODELS.get(scout_config.get("agent_key"), AI_MODELS["speed"])
        
        try:
            scout_results = agent.run_step(
                scout_config, 
                override_model_id=scout_model,
                override_temp=AI_TEMP_CREATIVE
            )
        except KeyboardInterrupt:
            print("\n🚫 Scout aborted by user. Exiting.")
            sys.exit(0)
            
        if not scout_results:
            print("❌ Step 1 failed. Aborting.")
            return

        # 3. STEP 2: Deep Research Audit (Temp AI_TEMP_PRECISE)
        # Injects scout results into the 'scout_data' variable in the prompt.
        audit_config = scenario['steps'][1]
        audit_model = AI_MODELS.get(audit_config.get("agent_key"), AI_MODELS["logic"])
        
        print("\n--- Chaining Data to Deep Research Agent ---")
        final_verdict = None
        while final_verdict is None:
            try:
                final_verdict = agent.run_step(
                    audit_config, 
                    context_data={"scout_data": scout_results},
                    is_chained=True,
                    override_model_id=audit_model,
                    override_temp=AI_TEMP_PRECISE
                )
            except KeyboardInterrupt:
                print("\n🚫 Audit aborted by user. Exiting.")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Execution Error: {type(e).__name__} - {str(e)[:100]}...")
                print("\nHow would you like to proceed?")
                print("1. Execute with Fast Model (Speed)")
                print("2. Execute with Pro Model (Logic, NO Deep Research)")
                print("3. Quit")
                
                try:
                    choice = input(f"Select an option (1/2/3): ")
                    if choice == "1":
                        audit_config["use_deep_research"] = False
                        audit_model = AI_MODELS["speed"]
                    elif choice == "2":
                        audit_config["use_deep_research"] = False
                        audit_model = AI_MODELS["logic"]
                    else:
                        print("Exiting.")
                        sys.exit(0)
                except KeyboardInterrupt:
                    print("\n🚫 Fallback aborted by user. Exiting.")
                    sys.exit(0)

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