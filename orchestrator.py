# orchestrator.py
import json
import re
from typing import Dict, Any

class AquatorOrchestrator:
    def __init__(self):
        self.registry = {}
        print("[AQUATOR] Initializing Universal Ocean Engine Core...")

    def register_agent(self, name: str, agent_instance):
        self.registry[name] = agent_instance
        print(f"[AQUATOR] Agent '{name}' successfully docked to pipeline.")

    def parse_global_intent(self, user_prompt: str) -> Dict[str, Any]:
        """
        Bespoke parsing engine to map raw natural language queries 
        to explicit structural and spatial coordinate domains.
        """
        print(f"[AQUATOR] Analyzing unrestricted system intent: '{user_prompt}'")
        
        # Default fallback global coordinates
        coordinates = {"lat": -34.0, "lon": 115.0} # Global default (Indian Ocean)
        depth = 300.0

        # Autonomous Regional Parsing Router
        prompt_clean = user_prompt.lower()
        if "baltic" in prompt_clean:
            coordinates = {"lat": 54.1, "lon": 12.1} # Rostock / Baltic Bounding Coordinates
            depth = 120.0
        elif "mariana" in prompt_clean or "trench" in prompt_clean:
            coordinates = {"lat": 11.3, "lon": 142.2} # Challenger Deep coordinates
            depth = 6000.0
        elif "north sea" in prompt_clean:
            coordinates = {"lat": 56.5, "lon": 3.0}
            depth = 200.0

        # RegEx scanning to extract explicit depth declarations if stated by the user
        depth_match = re.search(r"(\d+)\s*(m|meter)", prompt_clean)
        if depth_match:
            depth = float(depth_match.group(1))

        execution_plan = {
            "spatial_coordinates": coordinates,
            "depth_profile_meters": depth,
            "core_physics_modules": ["hydrodynamics", "buoyancy", "structures"],
        }
        return execution_plan

    def execute_pipeline(self, user_prompt: str):
        plan = self.parse_global_intent(user_prompt)
        print(f"[AQUATOR] Generated execution plan: {json.dumps(plan, indent=2)}")
        
        context_data = {}
        
        # Phase 1: Ingest Live Global Web Data Streams
        if "api_mesh" in self.registry:
            print("[AQUATOR] Phase 1: Triggering global API web mesh scraper...")
            context_data["environment"] = self.registry["api_mesh"].fetch_global_column(plan)

        # Phase 2: Ground Code Synthesis in Mathematical Laws
        if "knowledge_base" in self.registry:
            print("[AQUATOR] Phase 2: Grounding intent logic in strict ITTC & Fossen standards...")
            self.registry["knowledge_base"].format_prompt_injection(plan["core_physics_modules"])

        # Phase 3: Compile Web App Shell Workspace
        if "app_builder" in self.registry:
            print("[AQUATOR] Phase 3: Launching factory interface compilation node...")
            self.registry["app_builder"].compile_frontend(context_data)
            
        print("[AQUATOR] Pipeline execution complete. Workspace fully operational.")