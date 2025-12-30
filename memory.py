"""
memory.py

Gestion de l'historique des erreurs et corrections.
"""

class Memory:
    def __init__(self):
        """Initialise la mémoire avec des listes pour erreurs et corrections."""
        self.errors = []
        self.corrections = []

    def add_error(self, code, error_message):
        """Ajoute une erreur avec le code correspondant."""
        self.errors.append({'code': code, 'error': error_message})

    def add_correction(self, corrected_code):
        """Ajoute un code corrigé."""
        self.corrections.append(corrected_code)

    def get_errors(self):
        """Retourne la liste des erreurs."""
        return self.errors

    def get_corrections(self):
        """Retourne la liste des corrections."""
        return self.corrections
