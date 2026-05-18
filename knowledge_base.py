import json
from typing import List, Dict

class MarineKnowledgeBase:
    def __init__(self):
        # In a live deployment, this connects to a Vector Database (like Pinecone or Milvus)
        # loaded with thousands of PDFs of ITTC procedures, DNV rules, and hydrodynamics textbooks.
        self.vector_store = self._initialize_domain_physics()
        print("[KNOWLEDGE_BASE] Marine engineering standard vectors loaded and locked.")

    def _initialize_domain_physics(self) -> Dict[str, dict]:
        """
        Mocking the vector database. These are the absolute mathematical truths 
        the AI is forced to use when generating its simulation code.
        """
        return {
            "hydrodynamics": {
                "source": "Fossen, T.I. (2011) Marine Craft Hydrodynamics",
                "equations": [
                    "Rigid Body: M_RB * v_dot + C_RB(v)*v + M_A * v_dot + C_A(v_r)*v_r + D(v_r)*v_r + g(eta) = tau + tau_env",
                    "Lift Force: L = 0.5 * rho * V^2 * S * C_L"
                ],
                "strict_constraints": "Always recalculate added mass (M_A) dynamically if hull geometry changes."
            },
            "structures": {
                "source": "DNV-RU-OU-0512 Submersibles",
                "equations": [
                    "Critical Buckling Pressure: P_crit = (2 * E / (1 - mu^2)) * (t / D)^3"
                ],
                "strict_constraints": "Factor of Safety (FoS) must be >= 1.5 for unmanned pressure hulls. Never compromise."
            },
            "buoyancy": {
                "source": "Archimedes' Principle & Oceanographic Standard",
                "equations": [
                    "Required Volume: V_req = m_vehicle / rho_water"
                ],
                "strict_constraints": "Density (rho_water) MUST be injected dynamically from the API Mesh. DO NOT assume 1025 kg/m^3."
            }
        }

    def retrieve_context(self, domain: str) -> dict:
        """
        Retrieves the exact mathematical and regulatory context for a given engineering domain.
        """
        print(f"[KNOWLEDGE_BASE] Fetching rigid mathematical constraints for: [{domain.upper()}]")
        if domain in self.vector_store:
            return self.vector_store[domain]
        else:
            # Fatal error handling: If it doesn't know the math, it refuses to guess.
            raise ValueError(f"Domain '{domain}' not found in RAG. Halting to prevent physical hallucination.")

    def format_prompt_injection(self, domains: List[str]) -> str:
        """
        Creates the prompt payload that binds the LLM's code generation.
        This string is appended to the Orchestrator's prompt before contacting the AI.
        """
        injection = (
            "\n========================================\n"
            "CRITICAL SYSTEM INSTRUCTION:\n"
            "You are writing engineering code. You must strictly use the following physics "
            "and regulatory standards. Do not invent formulas.\n"
            "========================================\n\n"
        )
        
        for domain in domains:
            data = self.retrieve_context(domain)
            injection += f"--- DOMAIN: {domain.upper()} ---\n"
            injection += f"Source Standard: {data['source']}\n"
            injection += f"Governing Equations: {data['equations']}\n"
            injection += f"Absolute Constraint: {data['strict_constraints']}\n\n"
            
        print("[KNOWLEDGE_BASE] System Prompt Injection compiled successfully.")
        return injection

# For standalone testing
if __name__ == "__main__":
    db = MarineKnowledgeBase()
    # Test what the LLM will see before it writes the code for our glider
    injection_payload = db.format_prompt_injection(["hydrodynamics", "buoyancy", "structures"])
    print(injection_payload)