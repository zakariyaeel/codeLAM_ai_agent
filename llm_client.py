"""
llm_client.py

Connexion à l'API CodeLlama pour générer et corriger du code Python.
"""

import os
import re
import requests
import json

class CodeLlamaClient:
    def __init__(self, api_url="http://localhost:11434/api/generate", model="codellama"):
        """Initialise le client avec l'URL de l'API Ollama et le modèle par défaut."""
        self.api_url = api_url
        self.model = model

    def _call_ollama(self, prompt):
        """Fonction utilitaire pour appeler l'API Ollama."""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 1024
                    }
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json().get('response', '')
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion à Ollama: {e}")
            return None

    def _detect_language(self, prompt):
        """Détecte le langage de programmation à partir du prompt."""
        prompt_lower = prompt.lower()
        
        if any(ext in prompt_lower for ext in ['javascript', 'js', 'node']):
            return 'javascript'
        elif any(ext in prompt_lower for ext in ['python', 'py']):
            return 'python'
        elif any(ext in prompt_lower for ext in ['sql']):
            return 'sql'
        else:
            return 'python'  # Par défaut

    def generate_code(self, prompt):
        """Génère du code dans le langage approprié."""
        language = self._detect_language(prompt)
        
        if language == 'javascript':
            system_prompt = """Tu es un assistant de programmation expert en JavaScript. 
            Génère uniquement le code JavaScript sans commentaires explicatifs supplémentaires.
            Ne mets pas de backticks (```) autour du code.
            Voici la tâche : """
        elif language == 'sql':
            system_prompt = """Tu es un expert en bases de données SQL. 
            Génère UNIQUEMENT le code SQL valide pour SQLite, sans commentaires, sans texte explicatif et sans backticks.
            Pour les noms de tables et de colonnes, utilise des mots simples sans accents.
            Voici la tâche : """
        else:  # Python par défaut
            system_prompt = """Tu es un assistant de programmation expert en Python. 
            Génère uniquement le code Python sans commentaires explicatifs supplémentaires.
            Ne mets pas de backticks (```) autour du code.
            Voici la tâche : """
        
        full_prompt = f"{system_prompt}{prompt}"
        response = self._call_ollama(full_prompt)
        
        if response is None:
            return """-- Erreur: Impossible de générer de code. Vérifiez que le serveur Ollama est en cours d'exécution.
-- Assurez-vous d'avoir lancé la commande: ollama run codellama
"""
        
        # Nettoyage de la réponse
        try:
            # Supprime les backticks et les marqueurs de langage
            response = re.sub(r'^```(?:sql)?\s*', '', response, flags=re.IGNORECASE)
            response = re.sub(r'```\s*$', '', response, flags=re.IGNORECASE)
            response = response.strip()
            
            # Supprime les numéros de ligne si présents
            response = re.sub(r'^\s*\d+\s*\|?', '', response, flags=re.MULTILINE)
            
            # Supprime les lignes vides au début et à la fin
            response = re.sub(r'^\s*\n', '', response)
            response = re.sub(r'\n\s*$', '', response)
            
            return response
            
        except Exception as e:
            print(f"Erreur lors du nettoyage de la réponse: {e}")
            return response if response else ""

    def correct_code(self, code, error_message):
        """Demande une correction du code en fournissant le code et le message d'erreur."""
        # Détecter le langage à partir du code ou du message d'erreur
        language = self._detect_language(code) or self._detect_language(error_message)
        
        # Déterminer le prompt système en fonction du langage
        if language == 'javascript':
            system_prompt = """Tu es un expert en JavaScript. Corrige le code suivant en fonction de l'erreur.
            Ne mets pas de backticks (```) autour du code corrigé.
            Code à corriger :
            """
        elif language == 'sql':
            system_prompt = """Tu es un expert en SQL. Corrige la requête suivante en fonction de l'erreur.
            Ne mets pas de backticks (```) autour du code corrigé.
            Requête à corriger :
            """
        else:  # Python par défaut
            system_prompt = """Tu es un expert en Python. Corrige le code suivant en fonction de l'erreur.
            Ne mets pas de backticks (```) autour du code corrigé.
            Code à corriger :
            """
            
        full_prompt = f"""{system_prompt}
        {code}
        
        Message d'erreur : {error_message}
        
        Fournis uniquement le code corrigé, sans commentaires explicatifs.
        """
        
        corrected_code = self._call_ollama(full_prompt)
        if not corrected_code:
            return code
            
        # Nettoyer la réponse
        corrected_code = re.sub(r'^```(?:javascript|python|sql)?\s*', '', corrected_code, flags=re.IGNORECASE)
        corrected_code = re.sub(r'```\s*$', '', corrected_code, flags=re.IGNORECASE)
        return corrected_code.strip()
