import subprocess
import tkinter as tk
from tkinter import filedialog

def main():
    # 1) Masquer la fenêtre principale Tkinter
    root = tk.Tk()
    root.withdraw()

    # 2) Sélectionner l'image via explorateur de fichiers
    file_path = filedialog.askopenfilename(
        title="Sélectionnez une image",
        filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Tous fichiers", "*.*")]
    )
    if not file_path:
        print("Aucun fichier sélectionné. Fin du programme.")
        return

    # 3) Saisir le prompt dans la console
    prompt = input("Entrez votre prompt : ").strip()
    if not prompt:
        print("Aucun prompt entré. Fin du programme.")
        return

    # 4) Appel à Ollama (CLI) avec encodage UTF-8 et gestion des erreurs
    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5vl:3b", file_path, prompt],
            check=True,
            capture_output=True,
            text=True,         # mode texte
            encoding="utf-8",  # forcer UTF-8
            errors="replace"   # remplacer les octets illisibles par �
        )
        print("\nRéponse du modèle :\n")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Afficher stderr en UTF-8 également
        err = e.stderr
        if isinstance(err, bytes):
            err = err.decode("utf-8", errors="replace")
        print(f"Erreur lors de l'appel à Ollama :\n{err}")

if __name__ == "__main__":
    main()

