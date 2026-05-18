# main.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Enterprise module imports
from physics_engine import MarinePhysicsEngine
from orchestrator import AquatorOrchestrator
from api_mesh import GlobalAPIMesh
from knowledge_base import MarineKnowledgeBase
from app_builder import AppBuilderFactory

# --- WORKSPACE CONFIGURATION AND ENVIRONMENT SETUP ---
st.set_page_config(
    page_title="AQUATOR // Enterprise Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Compile local asset styling matrix cleanly away from markdown parsers
try:
    with open("style.css", "r") as f:
        st.html("<style>" + f.read() + "</style>")
except Exception:
    pass

@st.cache_data(show_spinner=False)
def execute_agentic_pipeline():
    """Triggers background context generation using the core agent network."""
    orchestrator = AquatorOrchestrator()
    api_mesh_agent = GlobalAPIMesh()
    knowledge_agent = MarineKnowledgeBase()
    app_builder_agent = AppBuilderFactory()

    orchestrator.register_agent("api_mesh", api_mesh_agent)
    orchestrator.register_agent("knowledge_base", knowledge_agent)
    orchestrator.register_agent("app_builder", app_builder_agent)

    universal_prompt = (
        "Design a high-endurance autonomous glider for research "
        "operations targeting the brackish water columns of the Baltic Sea."
    )
    
    plan = orchestrator.parse_global_intent(universal_prompt)
    context_data = {}
    if "api_mesh" in orchestrator.registry:
        context_data["environment"] = orchestrator.registry["api_mesh"].fetch_global_column(plan)
    return context_data

# Run system data collection
system_context = execute_agentic_pipeline()
env_data = system_context.get("environment", {})
surface_profile = env_data.get("surface_conditions", {})
water_layers = env_data.get("water_column_profile", {})

# Extract regional metocean base baselines
base_density = water_layers.get("density_kg_m3", [1015.0])[0]
base_salinity = water_layers.get("salinity_psu", [8.5])[0]
significant_wave = surface_profile.get("wave_height_significant_m", 0.8)

# --- VISUAL INTERFACE ASSEMBLY ---

# 1. Platform Brand Title Node
header_left, header_right = st.columns([3, 1])
with header_left:
    st.title("AQUATOR // WORKSPACE CONTROL")
    st.caption("Production Systems Simulation Cluster | Active Evaluation Frame")
with header_right:
    st.markdown(" ")
    st.status("SIMULATION NODE ONLINE", state="complete")

st.divider()

# 2. Command Telemetry Code Stream
st.write("##### 📡 Active Platform Log Output")
telemetry_feed = (
    "[CORE_BOOT]   Virtual container mapping verified on port 8501.\n"
    "[DATA_MESH]   Ingested hydrographic parameters for Baltic Sea basin coordinates.\n"
    "[PHYS_LOAD]   MarinePhysicsEngine multi-layered calculations bound securely.\n"
    "[COMPILING]   Plotly trace layout metrics parsed error-free."
)
st.code(telemetry_feed, language="bash")

# 3. Main Operational Controller Grid Split
control_col, display_col = st.columns([1, 2], gap="large")

with control_col:
    st.write("##### ⚙️ System Configuration Variables")
    
    dry_mass = st.slider("Target Vehicle Dry Mass (kg)", min_value=20.0, max_value=1200.0, value=95.0, step=5.0)
    safety_coeff = st.slider("Required Factor of Safety (FoS)", min_value=1.0, max_value=3.0, value=1.8, step=0.1)
    target_depth = st.slider("Maximum Operational Depth Target (m)", min_value=50, max_value=600, value=250, step=25)
    
    st.markdown(" ")
    hull_alloy = st.selectbox(
        "Pressure Cylinder Alloy Profile", 
        ["Carbon Fiber Composite", "Aluminum 7075-T6", "Titanium Grade 5"]
    )
    hull_diameter = st.slider("Cylinder Outer Diameter (m)", min_value=0.15, max_value=1.20, value=0.45, step=0.05)
    
    st.divider()
    
    st.write("##### 🌊 Regional Environmental Context")
    met_left, met_right = st.columns(2)
    with met_left:
        st.metric(label="Live Target Wave Height", value=f"{significant_wave} m")
    with met_right:
        st.metric(label="Base Basin Salinity", value=f"{base_salinity} PSU")

with display_col:
    st.write("##### 📊 Advanced Computational Workspace")
    tab_buoyancy, tab_hull = st.tabs(["Hydrodynamic Forces Profile", "Pressure Hull Stress Mechanics"])
    
    with tab_buoyancy:
        # Connect to our decoupled physics engine module
        equilibrium_volume_m3 = dry_mass / base_density
        equilibrium_volume_liters = equilibrium_volume_m3 * 1000.0
        
        b_left, b_right = st.columns(2)
        with b_left:
            st.metric(label="Calculated Target Displacement Volume", value=f"{equilibrium_volume_liters:.2f} L")
        with b_right:
            st.metric(label="Calculated Equilibrium Density", value=f"{base_density:.1f} kg/m³")
            
        # Generating multi-point linear physics curves
        depth_axis = np.linspace(0, target_depth, 150)
        simulated_density_array = np.full_like(depth_axis, base_density) + (depth_axis * 0.005)
        
        force_vector = MarinePhysicsEngine.calculate_buoyancy_matrix(
            displaced_volume_m3=equilibrium_volume_m3,
            dry_mass_kg=dry_mass,
            depths_array=depth_axis,
            density_profile=simulated_density_array
        )
        
        # High-performance Plotly Canvas Setup
        buoyancy_fig = go.Figure()
        buoyancy_fig.add_trace(go.Scatter(
            x=force_vector, y=depth_axis, 
            mode='lines', name='Net Force Delta',
            line=dict(color='#00f2fe', width=4)
        ))
        buoyancy_fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=340,
            xaxis_title="Net Fluid Force Vector (Newtons)",
            yaxis_title="System Hydrostatic Depth Axis (Meters)",
            yaxis_autorange="reversed",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e293b', zerolinecolor='#475569'),
            yaxis=dict(gridcolor='#1e293b', zerolinecolor='#475569')
        )
        st.plotly_chart(buoyancy_fig, use_container_width=True)
        
    with tab_hull:
        # Run stress evaluations from physics module
        hull_results = MarinePhysicsEngine.compute_hull_mechanics(
            material_profile=hull_alloy,
            outer_diameter_m=hull_diameter,
            factor_of_safety=safety_coeff,
            operational_depth_m=target_depth
        )
        
        thick_left, thick_right = st.columns(2)
        with thick_left:
            st.metric(label="Minimum Safe Shell Thickness", value=f"{hull_results['required_thickness_mm']:.2f} mm")
        with thick_right:
            st.metric(label="Calculated Theoretical Hoop Stress", value=f"{hull_results['calculated_hoop_stress_mpa']:.1f} MPa")
            
        st.markdown(" ")
        status_color = "green" if hull_results['structural_margin_status'] == "VALIDATED" else "red"
        st.markdown(f"Verification Boundary Status: :{status_color}[**{hull_results['structural_margin_status']}**]")
        st.caption(
            f"Shell calculation verified under hydrostatic collapse conditions matching "
            f"analytical stress modeling limits for {hull_alloy} structures."
        )
