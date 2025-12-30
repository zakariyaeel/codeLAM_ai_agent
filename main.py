"""
main.py

Point d'entrée du projet Autonomous Code-Generation Agent (CodeLAM).
"""

import streamlit as st
from ui import run_ui

def main():
    """Lance l'interface utilisateur."""
    st.set_page_config(
        page_title="CodeLAM - Autonomous Code Generation",
        page_icon="🤖",
        layout="wide"
    )
    run_ui()

if __name__ == '__main__':
    import os
    # Suppress the ScriptRunContext warning
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    main()
