"""
ui.py

Interface utilisateur simple et élégante avec Streamlit.
"""

import streamlit as st
import requests
from agent import AutonomousAgent


def run_ui():
    st.title("🤖 Autonomous Code-Generation Agent (CodeLAM)")
    st.markdown("---")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Paramètres")
        max_attempts = st.slider("Nombre maximum de tentatives", 1, 5, 3)
    
    # Main content
    st.write("Entrez une tâche de programmation en langage naturel :")
    user_request = st.text_area("Description de la tâche", height=150, 
                              placeholder="Ex: Créer une fonction qui calcule la factorielle d'un nombre")

    if st.button("🚀 Générer le code", type="primary"):
        if not user_request.strip():
            st.warning("Veuillez saisir une demande utilisateur valide.")
            st.stop()

        agent = AutonomousAgent(max_attempts=max_attempts)
        
        with st.spinner("🧠 Génération et exécution du code en cours..."):
            try:
                code, error = agent.run(user_request)
                
                if code:
                    st.subheader("✅ Code généré avec succès")
                    st.code(code, language="python")
                    st.balloons()
                else:
                    st.error("❌ Échec de la génération du code")
                    if "Impossible de se connecter au service Ollama" in str(error):
                        st.error("""
                        **Ollama n'est pas en cours d'exécution.**
                        
                        Pour utiliser cette application, vous devez :
                        1. Télécharger et installer Ollama depuis [ollama.ai](https://ollama.ai/)
                        2. Lancer Ollama
                        3. Télécharger le modèle CodeLlama en exécutant :
                           ```
                           ollama pull codellama
                           ```
                        4. Redémarrer cette application
                        """)
                    else:
                        st.error(f"Détail de l'erreur :\n{error}")
                    
            except requests.exceptions.ConnectionError as e:
                st.error("""
                ❌ Impossible de se connecter à Ollama
                
                Assurez-vous que :
                1. Ollama est installé et en cours d'exécution
                2. Le service Ollama est accessible à http://localhost:11434
                3. Le modèle CodeLlama est téléchargé (`ollama pull codellama`)
                """)
                st.code("# Pour installer Ollama :\n# 1. Téléchargez depuis https://ollama.ai/\n# 2. Installez et lancez Ollama\n# 3. Téléchargez le modèle : ollama pull codellama")
                
            except Exception as e:
                st.error(f"Une erreur inattendue s'est produite : {str(e)}")
                st.exception(e)
