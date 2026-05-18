# main.py
from orchestrator import AquatorOrchestrator
from api_mesh import GlobalAPIMesh
from knowledge_base import MarineKnowledgeBase
from app_builder import AppBuilderFactory

def run_aquator_engine():
    print("====================================================")
    print("          🌟 PROJECT AQUATOR: LAUNCH VECTOR          ")
    print("====================================================\n")

    # 1. Initialize the master orchestrator brain
    orchestrator = AquatorOrchestrator()

    # 2. Instantiate the software and data agents
    api_mesh_agent = GlobalAPIMesh()
    knowledge_agent = MarineKnowledgeBase()
    app_builder_agent = AppBuilderFactory()

    # 3. Dock the agents to the orchestrator registry
    orchestrator.register_agent("api_mesh", api_mesh_agent)
    orchestrator.register_agent("knowledge_base", knowledge_agent)
    orchestrator.register_agent("app_builder", app_builder_agent)

    # 4. Define your global boundaryless prompt
    # Change this query to test any vehicle configuration on Earth
    universal_prompt = (
        "Design a high-endurance autonomous glider for research "
        "operations targeting the brackish water columns of the Baltic Sea."
    )

    print("\n[SYSTEM] Triggering global orchestration pipeline...")
    
    # 5. Run the master loop
    # This will fetch the web data, pull strict math formulas, and synthesize the app
    orchestrator.execute_pipeline(universal_prompt)

if __name__ == "__main__":
    run_aquator_engine()