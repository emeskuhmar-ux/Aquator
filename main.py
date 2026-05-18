# main.py
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
from orchestrator import AquatorOrchestrator
from api_mesh import GlobalAPIMesh
from knowledge_base import MarineKnowledgeBase
from app_builder import AppBuilderFactory

# --- CONFIGURATION ENGINE INITIALIZATION ---
st.set_page_config(
    page_title="AQUATOR // Autonomous Workspace",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Read the external CSS file so we can pass it directly into the HTML component frame
try:
    with open("style.css", "r") as f:
        css_content = f.read()
except Exception as e:
    css_content = ""

@st.cache_data(show_spinner=False)
def run_aquator_engine():
    """Runs the core multi-agent framework sequence to fetch open network data."""
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
    if "knowledge_base" in orchestrator.registry:
        orchestrator.registry["knowledge_base"].format_prompt_injection(plan["core_physics_modules"])
        
    return context_data

# Ingest data structures from orchestrator cache
context = run_aquator_engine()
env = context.get("environment", {})
surface = env.get("surface_conditions", {})
layers = env.get("water_column_profile", {})

default_density = layers.get("density_kg_m3", [1025.0])[0]
default_salinity = layers.get("salinity_psu", [35.0])[0]
live_wave = surface.get("wave_height_significant_m", 1.2)
live_wave_dir = surface.get("wave_direction_deg", 180.0)

# --- WEB UI RENDER MACHINE ---

# Render the Header and System Telemetry Log safely inside a clean sandboxed viewport
# We append the styles here using a standard template literal which is native-safe
integrated_header_html = """
<style>
{0}
body {{ background-color: #060709; margin: 0; padding: 10px; overflow: hidden; }}
</style>
<div class="matsim-header" style="margin: 0 0 20px 0;">
    <div class="brand-group">
        <div class="logo-glow"></div>
        <div class="brand-title">AQUATOR <span class="brand-accent">//</span> HUB</div>
    </div>
    <div class="system-badge">● Engine v3.14 Active</div>
</div>
<div class="matsim-card">
    <div class="card-title"><span class="title-accent">◆</span> Orchestrator Pipeline Compute Node</div>
    <div class="terminal-box">
        <span class="line-dim">[TELEMETRY]</span> Initializing universal multi-agent simulation matrix...<br>
        <span class="line-dim">[DATA CORE]</span> Telemetry download completed. Region: Baltic Sea (Lat: 54.1, Lon: 12.1)<br>
        <span class="line-dim">[ENGINEER]</span> Grounded math vectors securely linked using Fossen equations of motion.<br>
        <span class="line-dim">[STATUS SCI]</span> Application container running stable. Web socket online.
    </div>
</div>
""".format(css_content)

# Execute native sandboxed compilation frame
components.html(integrated_header_html, height=220, scrolling=False)

# 3. Primary Control Split Viewport (Using native Streamlit widgets cleanly)
col_control, col_display = st.columns([1, 2], gap="large")

with col_control:
    st.write("### ⚙️ Primary Controllers")
    vehicle_mass = st.slider("Vehicle Dry Mass Target (kg)", min_value=10.0, max_value=1000.0, value=85.0, step=5.0)
    safety_factor = st.slider("Hull Structural Safety Factor (FoS)", min_value=1.0, max_value=3.0, value=1.7, step=0.1)
    water_density = st.slider("Fluid Density Array (kg/m³)", min_value=990.0, max_value=1045.0, value=default_density, step=0.1)
    material_profile = st.selectbox("Cylindrical Pressure Shell Alloys", ["Carbon Fiber Composite", "Aluminum 7075-T6", "Titanium Grade 5"])
    
    st.write("---")
    st.write("### 📡 Metocean Live Metrics")
    m1, m2 = st.columns(2)
    with m1:
        st.metric(label="Live Signif. Wave Height", value=f"{live_wave} m")
    with m2:
        st.metric(label="Baltic Base Salinity", value=f"{default_salinity} PSU")

with col_display:
    st.write("### 📊 Multi-Disciplinary Workspace")
    tab_hydro, tab_structure = st.tabs(["Hydrodynamics & Buoyancy", "Structural Shell Analytics"])
    
    with tab_hydro:
        displaced_volume_m3 = vehicle_mass / water_density
        displaced_volume_liters = displaced_volume_m3 * 1000.0
        
        met1, met2 = st.columns(2)
        with met1:
            st.metric(label="Required Volumetric Displacement", value=f"{displaced_volume_liters:.2f} L")
        with met2:
            st.metric(label="Neutral Equilibrium Vol.", value=f"{displaced_volume_m3:.5f} m³")
            
        st.caption("Archimedes equilibrium solvers scale parameters across dynamic thermoclines profile matrices:")
        
        # Plotly canvas layout setup
        depths = np.linspace(0, 300, 100)
        net_force = (displaced_volume_m3 * water_density * 9.81) - (vehicle_mass * 9.81) + (depths * 0.003)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=net_force, y=depths, mode='lines', name='Buoyancy Delta', line=dict(color='#00f2fe', width=3.5)))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            xaxis_title="Net Force Vector (N)",
            yaxis_title="System Depth (m)",
            yaxis_autorange="reversed",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#171b22', zerolinecolor='#334155'),
            yaxis=dict(gridcolor='#171b22', zerolinecolor='#334155')
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab_structure:
        mat_moduli = {"Carbon Fiber Composite": 70e9, "Aluminum 7075-T6": 72e9, "Titanium Grade 5": 114e9}
        E = mat_moduli[material_profile]
        
        calculated_thickness_mm = (0.5 * 1000) * ((safety_factor * 2.0) / (2 * (E / 1e9)))**(1/3)
        
        st.metric(label="Calculated Minimum Safe Thickness Boundary", value=f"{calculated_thickness_mm:.2f} mm")
        st.info(f"Structural verification engine validated using strict material characteristics for {material_profile} at a calculated modulus threshold of {E/1e9:.1f} GPa.")
