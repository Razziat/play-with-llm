# Script de génération avec Ollama CLI

## Description

Ce script Python permet de sélectionner une image via l'explorateur de fichier, de saisir un prompt dans la console, puis d'appeler le modèle **qwen2.5vl:3b** via la CLI Ollama pour générer une réponse basée sur l'image et le prompt.

## Prérequis

* **Python 3.6+**
* **Tkinter** (inclus par défaut dans la plupart des distributions Python)
* **Ollama** installé avec le modèle **qwen2.5vl:3b**

  ```bash
  ollama pull qwen2.5vl:3b
  ```

## Installation

1. Clonez ce dépôt ou téléchargez le script :

   ```bash
   git clone git@github.com:Razziat/play-with-llm.git ou https://github.com/Razziat/play-with-llm.git
   cd play-with-llm/local_vlm_chatbot
   ```

2. (Optionnel) Créez un environnement virtuel et activez-le :

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate    # Windows
   ```

## Utilisation

1. Lancez le script :

   ```bash
   python challenge_optionnel.py
   ```

2. Une fenêtre de sélection de fichier s'ouvre. Choisissez une image (PNG, JPG, JPEG, BMP, GIF).

3. Si aucun fichier n'est sélectionné, le programme s'arrête.

4. Dans la console, saisissez votre prompt et validez.

5. Le script appelle Ollama CLI et affiche la réponse du modèle.

### Exemple de sortie

```console
Entrez votre prompt : Décris cette image en détail.

Réponse du modèle :
...
```

## Personnalisation

* Pour utiliser un autre modèle, modifiez la ligne dans `subprocess.run` :

  ```python
  ["ollama", "run", "qwen2.5vl:3b", file_path, prompt],
  ```
