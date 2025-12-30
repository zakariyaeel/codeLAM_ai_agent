"""
executor.py

Exécution sécurisée du code Python généré.
"""

import subprocess
import sys
import os
import tempfile
import re
import json


class CodeExecutor:
    def __init__(self):
        # Create a dedicated temp directory for our code execution
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'codelam_temp')
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_temp_file_path(self):
        """Generate a unique temporary file path."""
        return os.path.join(self.temp_dir, f'temp_{os.urandom(8).hex()}.py')

    def _execute_sql(self, code):
        """Exécute le code SQL en utilisant sqlite3 en mémoire."""
        try:
            import sqlite3
            from io import StringIO
            import contextlib
            
            # Nettoyer le code SQL
            code = code.strip()
            if not code:
                return False, "Le code SQL est vide"
                
            # Supprimer les commentaires SQL (-- et /* */)
            code = re.sub(r'--.*?$', '', code, flags=re.MULTILINE)
            code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
            code = re.sub(r'\s+', ' ', code).strip()
            
            # Crée une base de données en mémoire
            conn = sqlite3.connect(':memory:')
            conn.row_factory = sqlite3.Row  # Pour un accès aux colonnes par nom
            output = StringIO()
            
            try:
                with contextlib.redirect_stdout(output):
                    cursor = conn.cursor()
                    
                    # Exécute chaque instruction SQL séparément
                    for statement in code.split(';'):
                        statement = statement.strip()
                        if not statement:
                            continue
                            
                        try:
                            cursor.execute(statement)
                            
                            # Si c'est une requête SELECT, affiche les résultats
                            if statement.strip().upper().startswith('SELECT'):
                                results = cursor.fetchall()
                                if results:
                                    # Affiche les noms des colonnes
                                    col_names = [description[0] for description in cursor.description]
                                    output.write(' | '.join(col_names) + '\n')
                                    output.write('-' * (sum(len(str(c)) for c in col_names) + 3 * (len(col_names) - 1)) + '\n')
                                    # Affiche les résultats
                                    for row in results:
                                        output.write(' | '.join(str(cell) for cell in row) + '\n')
                                output.write('\n')
                                
                        except sqlite3.Error as e:
                            return False, f"Erreur SQL: {str(e)}\nDans la requête: {statement}"
                    
                    conn.commit()
                    output_str = output.getvalue()
                    return (True, output_str) if output_str else (True, "Requête exécutée avec succès")
                    
            except Exception as e:
                return False, f"Erreur d'exécution: {str(e)}"
                
        except Exception as e:
            return False, f"Erreur lors de l'initialisation SQL: {str(e)}"
            
        finally:
            if 'conn' in locals():
                conn.close()

    def _execute_python(self, code, temp_file_path):
        """Exécute le code Python dans un sous-processus."""
        try:
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            result = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.temp_dir
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Délai d'exécution dépassé (10 secondes)"
        except Exception as e:
            return False, f"Erreur d'exécution: {str(e)}"

    def _execute_javascript(self, code):
        """Exécute du code JavaScript avec Node.js."""
        try:
            # Crée un fichier temporaire pour le code JavaScript
            with tempfile.NamedTemporaryFile(suffix='.js', delete=False, dir=self.temp_dir) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(code.encode('utf-8'))
                temp_file.flush()
            
            # Exécute le code avec Node.js
            result = subprocess.run(
                ['node', temp_file_path],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.temp_dir
            )
            
            # Nettoie le fichier temporaire
            try:
                os.unlink(temp_file_path)
            except:
                pass
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Délai d'exécution dépassé (10 secondes)"
        except Exception as e:
            return False, f"Erreur d'exécution JavaScript: {str(e)}"

    def execute(self, code, language='python'):
        """Exécute le code et retourne (succès, sortie ou message d'erreur)."""
        if not code.strip():
            return False, "Le code est vide"
            
        # Nettoyer le code (supprimer les backticks si présents)
        code = re.sub(r'^```(?:javascript|python|sql)?\s*', '', code, flags=re.IGNORECASE)
        code = re.sub(r'```\s*$', '', code, flags=re.IGNORECASE)
        code = code.strip()
        
        temp_file_path = None
        
        try:
            if language.lower() == 'sql':
                return self._execute_sql(code)
            elif language.lower() == 'javascript':
                return self._execute_javascript(code)
            else:  # Python par défaut
                temp_file_path = self._get_temp_file_path()
                return self._execute_python(code, temp_file_path)
                
        except subprocess.TimeoutExpired:
            return False, "Délai d'exécution dépassé (10 secondes)"
        except Exception as e:
            return False, f"Erreur d'exécution: {str(e)}"
        finally:
            # Nettoyer le fichier temporaire s'il existe
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass  # Ignore cleanup errors
