# Autonomous Code-Generation Agent (CodeLAM)

## 1. Présentation du projet
Ce projet académique présente un agent autonome capable de générer, exécuter, corriger et valider du code Python à partir d'une demande en langage naturel.

## 2. Objectif académique
L'objectif est de démontrer l'utilisation d'un modèle de langage (LLM) pour automatiser la génération de code, la détection et correction d'erreurs, dans un cadre pédagogique et simple.

## 3. Architecture
Le projet est structuré en plusieurs modules :

- `main.py` : point d'entrée du projet
- `agent.py` : logique de l'agent autonome
- `llm_client.py` : connexion à l'API CodeLlama
- `executor.py` : exécution sécurisée du code
- `memory.py` : historique des erreurs et corrections
- `ui.py` : interface utilisateur simple avec Streamlit
- `requirements.txt` : dépendances Python

## 4. Explication du fonctionnement
L'utilisateur saisit une tâche de programmation en langage naturel via l'interface Streamlit.

L'agent autonome génère du code Python via l'API CodeLlama.

Le code est exécuté automatiquement.

En cas d'erreur, le message d'erreur est envoyé au LLM pour générer une correction.

Le processus se répète jusqu'à un succès ou un nombre maximal de tentatives.

## 5. Exemple d'utilisation

1. Lancer le projet :
```bash
pip install -r requirements.txt
python main.py
```

2. Dans l'interface, saisir une demande, par exemple :
"Créer une fonction Python qui calcule la factorielle d'un nombre."

3. Cliquer sur "Générer le code".

4. Le code généré s'affiche et est exécuté automatiquement.

5. En cas d'erreur, une correction est proposée.

## 6. Limites et améliorations futures

- Limitation à 3 tentatives de correction
- Sécurité d'exécution du code à renforcer
- Support d'autres langages de programmation
- Amélioration de l'interface utilisateur
- Intégration d'un système de logs plus complet


## Docker instructions : 
-Suivez ces commandes : 
 **Démarrer l'aplication**
    ```bash
        docker compose up -d
    ```
**Installer ollama model dans docker**
    ```bash
        docker exec -it ollama_backend ollama pull codellama:7b-instruct-q4_0
    ```
