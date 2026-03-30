import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv



load_dotenv()

# --- PATH CONFIG ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_DIR = PROJECT_ROOT / "docs" / "research"
PROMPT_DIR = PROJECT_ROOT / "prompts"
SCENARIO_DIR = PROJECT_ROOT / "scenarios"
INSTRUCTIONS_FILE = PROJECT_ROOT / "docs" / "system_instructions.md"

# Ensure directories exist
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
PROMPT_DIR.mkdir(parents=True, exist_ok=True)
SCENARIO_DIR.mkdir(parents=True, exist_ok=True)

# --- 2026 MODEL ALIASES ---
# Pull the specialized Research Agent ID from the environment
AGENT_ID = os.getenv("RESEARCH_AGENT_ID")

class ResearchAgent:
    def __init__(self, model_id):
        self.model_id = model_id
        self.api_key = self._get_api_key()
        self.client = genai.Client(api_key=self.api_key)
        self.system_instructions = self._load_instructions()

    def _get_api_key(self):
        """Checks for the 2026 standard key first, then falls back to the legacy name."""
        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not key:
            print("\n❌ ERROR: No API Key found in .env!")
            sys.exit(1)
        return key

    def _load_instructions(self):
        """Pulls property context. Critical failure if missing."""
        if not INSTRUCTIONS_FILE.exists():
            raise FileNotFoundError(f"CRITICAL ERROR: System instructions missing at {INSTRUCTIONS_FILE}")
        return INSTRUCTIONS_FILE.read_text(encoding="utf-8")

    def load_scenario(self, scenario_name):
        """Parses a JSON manifest from the /scenarios/ directory."""
        path = SCENARIO_DIR / f"{scenario_name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Scenario manifest missing: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_prompt_template(self, relative_path):
        """Reads a specific markdown prompt from the /prompts/ library."""
        path = PROJECT_ROOT / relative_path
        if not path.exists():
            raise FileNotFoundError(f"Prompt template missing: {path}")
        return path.read_text(encoding="utf-8")

    def get_token_count(self, prompt):
        """Calculates exact cost by including system instructions in the contents."""
        language_anchor = "\n\n[STRICT: ANSWER IN ENGLISH ONLY]"
        final_prompt = f"{prompt}{language_anchor}"
        
        contents = [
            types.Content(role="system", parts=[types.Part(text=self.system_instructions)]),
            types.Content(role="user", parts=[types.Part(text=final_prompt)])
        ]
        
        response = self.client.models.count_tokens(
            model=self.model_id,
            contents=contents
        )
        return response.total_tokens

    def run_step(self, step_config, context_data=None, is_chained=False, override_model_id=None, override_temp=0.7):
        """
        Loads the template, injects variables, and routes through the dry_run gate.
        """
        # Save baseline model and use the override if specified
        original_model = self.model_id
        if override_model_id:
            self.model_id = override_model_id
            
        template = self._load_prompt_template(step_config['prompt_file'])
        
        params = step_config.get('params', {})
        if context_data:
            params.update(context_data)
            
        final_prompt = template
        for key, value in params.items():
            final_prompt = final_prompt.replace(f"{{{{{key}}}}}", str(value))
        
        use_deep_research = step_config.get('use_deep_research', False)
        
        # Run execution
        result = self.dry_run(final_prompt, temperature=override_temp, use_deep_research=use_deep_research)
        
        # Restore baseline
        self.model_id = original_model
        return result

    def dry_run(self, prompt, temperature=0.7, use_deep_research=False):
        """Human-in-the-loop gate to prevent accidental quota depletion."""
        tokens = self.get_token_count(prompt)
        
        print(f"\n📊 QUOTA CHECK [{self.model_id.upper()}]")
        print(f"Total Tokens (with system context): {tokens}")
        print(f"Sampling Temperature: {temperature}")
        if use_deep_research:
            print("🧠 Deep Research: ENABLED")
        
        confirm = input("Spend 1 RPD (Request Per Day)? (y/n): ")
        if confirm.lower() == 'y':
            return self.execute_api_call(prompt, temperature=temperature, use_deep_research=use_deep_research)
        else:
            print("🚫 Operation cancelled.")
            raise KeyboardInterrupt("User cancelled the prompt")

    def execute_api_call(self, prompt, temperature=0.7, save_to_file=True, use_deep_research=False):
        """Sends the final payload and enables Deep Research thinking where applicable."""
        print(f"\n🚀 [Casa Kolla Agent] Requesting {self.model_id.upper()}...")
        
        config = types.GenerateContentConfig(
            system_instruction=self.system_instructions,
            temperature=temperature
        )
        if use_deep_research:
            config.thinking_config = types.ThinkingConfig(include_thoughts=True)

        language_anchor = "\n\n[STRICT CONSTRAINT: Provide all output and analysis in English only.]"
        final_prompt = f"{prompt}{language_anchor}"

        try:
            response = self.client.models.generate_content(
                model=self.model_id, 
                contents=final_prompt, 
                config=config
            )
        except Exception as e:
            raise e

        content = response.text
        if save_to_file:
            self._save_research(prompt, content)

        return content

    def _save_research(self, prompt, content):
        """Handles filename generation and research logging."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        is_draft = "draft" in prompt.lower()
        
        clean_title = re.sub(r'\bdraft\b', '', prompt[:100], flags=re.IGNORECASE)
        safe_title = "".join(x for x in clean_title if x.isalnum() or x in " -_").strip().replace(" ", "_")
        safe_title = re.sub(r'_{2,}', '_', safe_title).strip('_')
        
        suffix = "-draft" if is_draft else ""
        safe_model = self.model_id.replace("-", "_")
        filename = f"{timestamp}_{safe_model}_{safe_title}{suffix}.md"
        
        if len(filename) > 250:
            filename = filename[:240] + suffix + ".md"

        with open(RESEARCH_DIR / filename, "w", encoding="utf-8") as f:
            f.write(f"# Research Instance: {timestamp}\n\n{content}")
        
        print(f"💾 Logged: docs/research/{filename}")

if __name__ == "__main__":
    # If run standalone, import from config locally
    sys.path.insert(0, str(PROJECT_ROOT / "common"))
    from config import AI_MODELS, AI_TEMP_PRECISE

    agent = ResearchAgent(model_id=AI_MODELS["logic"])
    # Immediate use of Deep Research for the initial solar scan
    agent.execute_api_call("Deep Research the specific V_oc temperature coefficients of 450W Longi panels vs Jinko panels.", temperature=AI_TEMP_PRECISE, use_deep_research=True)