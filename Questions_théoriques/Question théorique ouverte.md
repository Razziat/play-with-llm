# Pipeline RAG Multimodal (Texte + Visuels)

Voici les grandes étapes de l’architecture

1. **Ingestion des documents**

   * **Quoi ?** Rassembler les sources (PDF, HTML, scans, images, graphiques).
   * **Comment ?** Un service d’ingestion lit les fichiers depuis un stockage central (bucket, dossier partagé) et les prépare pour le pipeline.
   * **Qui ?** Composant **Ingestion Service** du backend.

2. **Segmentation intelligente**

   * **Quoi ?** Découper en unités cohérentes (chunks) pour le texte et les visuels.
   * **Comment ?** Utilisation d’un LLM (Ollama/OpenAI...) ou d’algorithmes de segmentation (TextTiling, heuristiques) pour identifier des frontières naturelles.
   * **Qui ?** **Segmentation Service** du pipeline.

3. **Vectorisation multimodale**

   * **Quoi ?** Calculer un embedding pour chaque chunk :

     * Texte → encodeur SentenceTransformer
     * Visuel → modèle Vision–Language (CLIP, OpenCLIP…)
   * **Comment ?** Appel aux modèles d’embedding respectifs, puis normalisation des vecteurs.
   * **Qui ?** **Embedding Service** du backend.

4. **Indexation et création du graphe**

   * **Quoi ?** Stocker les embeddings dans un graphe ou un magasin de vecteurs.
   * **Comment ?**

     * Créer un nœud par chunk avec ID, type, embedding, contenu.
     * Ajouter des arêtes structurelles.
     * Calculer k‑NN sur les embeddings et créer des arêtes.
   * **Qui ?** **Indexer Service** (Graph Builder).

5. **Retrieval**

   * **Quoi ?** Récupérer les K chunks les plus proches de la requête.
   * **Comment ?**

     * Encoder la question en embedding.
     * Interroger le graphe vectoriel.
   * **Qui ?** **Retrieval Service** de l’API backend.

6. **Assemblage du contexte**

   * **Quoi ?** Récupérer le contenu des chunks sélectionnés et les ordonner.
   * **Comment ?** Fonction backend qui trie par similarité et extrait les textes/légendes.
   * **Qui ?** **Context Assembler** du handler.

7. **Construction du prompt RAG**

   * **Quoi ?** Formater les extraits en numérotation \[1], \[2], … avant la question.
   * **Comment ?** Routine qui assemble system prompt, extraits et question.
   * **Qui ?** **Prompt Builder** du backend.

8. **Génération par le LLM (Ollama)**

   * **Quoi ?** Envoyer le prompt contextuel à Ollama pour générer la réponse.
   * **Comment ?** Appel du modèle via ollama par exemple.
   * **Qui ?** **LLM Service** du backend.
