# main.py
import streamlit as st
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
    universal_prompt = (
        "Design a high-endurance autonomous glider for research "
        "operations targeting the brackish water columns of the Baltic Sea."
    )

    print("\n[SYSTEM] Triggering global orchestration pipeline...")
    
    # 5. Run the master loop (this generates the context data dictionaries)
    plan = orchestrator.parse_global_intent(universal_prompt)
    context_data = {}
    
    if "api_mesh" in orchestrator.registry:
        context_data["environment"] = orchestrator.registry["api_mesh"].fetch_global_column(plan)
    if "knowledge_base" in orchestrator.registry:
        orchestrator.registry["knowledge_base"].format_prompt_injection(plan["core_physics_modules"])
        
    return context_data

# --- STREAMLIT CLOUD RENDERING INTEGRATION ---
# This runs the orchestration pipeline once to fetch open API data, 
# then immediately maps the output variables into the active layout viewport.
if "aquator_context" not in st.session_state:
    st.session_state["aquator_context"] = run_aquator_engine()

context = st.session_state["aquator_context"]
env = context.get("environment", {})
surface = env.get("surface_conditions", {})
layers = env.get("water_column_profile", {})

default_density = layers.get("density_kg_m3", [1025.0])[0]
default_salinity = layers.get("salinity_psu", [35.0])[0]
live_wave = surface.get("wave_height_significant_m", 1.2)
live_wave_dir = surface.get("wave_direction_deg", 180.0)

# Render the multi-tab visual workspace layout
import numpy as np
import plotly.graph_objects as go

st.title("🌊 AQUATOR: Multi-Disciplinary Digital Twin")
st.markdown("#### Bounded Software Automation Loop | Live Workspace Verification")
st.write("---")

with st.sidebar:
    st.header("🛠️ Vehicle Dimensions")
    vehicle_mass = st.slider("Dry Vehicle Weight (kg)", min_value=10.0, max_value=1000.0, value=75.0, step=5.0)
    safety_factor = st.slider("Structural Factor of Safety (FoS)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
    st.write("---")
    st.subheader("📡 Live Metocean Context")
    st.metric(label="Live API Surface Wave Height", value=f"{live_wave} m")
    st.metric(label="Live Wave Propagation Angle", value=f"{live_wave_dir}°")

tab1, tab2, tab3 = st.tabs(["📊 Hydrodynamics & Buoyancy", "📐 Structural Hull Mechanics", "🌊 Live Marine Environment"])

with tab1:
    st.subheader("Buoyancy Alteration Curve & Flow Profile")
    water_density = st.slider("Simulated Fluid Density (kg/m³)", min_value=990.0, max_value=1045.0, value=default_density, step=0.1)
    displaced_volume_m3 = vehicle_mass / water_density
    displaced_volume_l = displaced_volume_m3 * 1000.0
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="Target Displaced Volume for Equilibrium", value=f"{displaced_volume_l:.2f} Liters")
    with c2:
        st.metric(label="Regional Base Salinity Profile", value=f"{default_salinity} PSU")

    depths = np.linspace(0, 300, 100)
    net_force = (displaced_volume_m3 * water_density * 9.81) - (vehicle_mass * 9.81) + (depths * 0.003)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=net_force, y=depths, mode='lines', name='Buoyancy Delta', line=dict(color='#00f2fe', width=3)))
    fig1.update_layout(title="Net Rescaling Forces vs Target Depth Axis", xaxis_title="Force (N)", yaxis_title="Depth (m)", yaxis_autorange="reversed", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Pressure Hull Cylindrical Buckling Constraints")
    material_type = st.selectbox("Hull Material Profile", ["Carbon Fiber Composite", "Aluminum 7075-T6", "Titanium Grade 5"])
    hull_diameter = st.slider("Cylinder Outer Diameter (m)", 0.2, 1.0, 0.5, 0.05)
    mat_props = {"Carbon Fiber Composite": 70e9, "Aluminum 7075-T6": 72e9, "Titanium Grade 5": 114e9}
    E = mat_props[material_type]
    calculated_thickness_mm = (hull_diameter * 1000) * ((safety_factor * 2.0) / (2 * (E / 1e9)))**(1/3)
    st.metric(label="Calculated Minimum Safe Hull Thickness", value=f"{calculated_thickness_mm:.2f} mm")

with tab3:
    st.subheader("Raw Ingested Hydrographic Payload")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.write("**Target Depth Coordinates (m)**")
        st.write(layers.get('depth_layers_m', []))
    with col_b:
        st.write("**Density Matrix (kg/m³)**")
        st.write(layers.get('density_kg_m3', []))
    with col_c:
        st.write("**Salinity Column (PSU)**")
        st.write(layers.get('salinity_psu', []))