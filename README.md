hydrogpt-toolkit/
├── README.md
├── LICENSE
├── .gitignore
├── tools/
│   ├── __init__.py
│   ├── hydrostatics.py
│   ├── structures.py
│   ├── acoustics.py
│   ├── mission_planning.py
│   ├── environment.py
│   └── regulations.py
├── prompts/
│   ├── system/
│   │   ├── hydrostatics_analyst.md
│   │   ├── structural_designer.md
│   │   ├── auv_mission_planner.md
│   │   ├── acoustic_analyst.md
│   │   └── regulatory_expert.md
│   └── context/
│       ├── ocean_engineering_basics.txt
│       ├── material_properties.txt
│       └── imo_codes.txt
├── gpt_config/
│   ├── hydrogpt_custom_gpt.yaml
│   └── functions.json
└── examples/
    ├── run_analysis.py
    └── streamlit_ui.py (optional)
