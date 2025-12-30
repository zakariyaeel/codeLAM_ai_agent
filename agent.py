"""
agent.py

Logique de l'agent autonome pour la génération, exécution, correction et validation du code.
"""

from llm_client import CodeLlamaClient
from executor import CodeExecutor
from memory import Memory
import re

class AutonomousAgent:
    def __init__(self, max_attempts=3):
        """Initialise l'agent avec un client LLM, un exécuteur de code et une mémoire."""
        self.llm_client = CodeLlamaClient()
        self.executor = CodeExecutor()
        self.memory = Memory()
        self.max_attempts = max_attempts

    def _extract_code_blocks(self, text):
        """Extrait les blocs de code entourés de ```python ... ``` ou ``` ... ```"""
        code_blocks = re.findall(r'```(?:python\n)?(.*?)```', text, re.DOTALL)
        return code_blocks[0].strip() if code_blocks else text.strip()

    def run(self, user_request):
        """Exécute la boucle principale de génération, exécution et correction du code."""
        # Détecter le langage à partir de la requête
        language = self.llm_client._detect_language(user_request)
        
        # Génération initiale du code
        raw_code = self.llm_client.generate_code(user_request)
        code = self._extract_code_blocks(raw_code)
        
        if not code:
            return None, "Impossible de générer le code à partir de la demande."

        attempts = 0
        last_error = None

        while attempts < self.max_attempts:
            # Nettoyer le code avant exécution
            clean_code = code.strip()
            if not clean_code:
                return None, "Le code généré est vide."

            # Exécuter le code avec le bon langage
            success, error = self.executor.execute(clean_code, language=language)
            
            if success:
                return clean_code, None
            
            # Enregistrer l'erreur
            last_error = error
            self.memory.add_error(clean_code, error)
            
            # Demander une correction
            if attempts < self.max_attempts - 1:  # Ne pas corger à la dernière tentative
                corrected_code = self.llm_client.correct_code(clean_code, error)
                if corrected_code and corrected_code != clean_code:
                    code = self._extract_code_blocks(corrected_code)
                    self.memory.add_correction(code)
            
            attempts += 1

        return None, f"Échec après {self.max_attempts} tentatives. Dernière erreur :\n{last_error}"
