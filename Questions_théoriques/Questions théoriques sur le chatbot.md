# *Architecture et Déploiement en Production*

---

## 1. Plan de déploiement Azure

### 1.1 Étapes principales

1. **Préparation de l’environnement** : compte Azure, quotas GPU, installation d’Azure CLI, Docker, Terraform/Kubectl, application containerisée.
2. **Création des ressources** : *Resource Group* dédié ; Azure Container Registry (ACR) pour stocker les images.
3. **Build & push d’images** : images séparées pour le *backend* et le service Ollama, `docker push` vers l’ACR.
4. **Provisionnement AKS** : cluster Kubernetes managé ; pool GPU (p. ex. **Standard\_NC6s\_v3**, V100 16 Go) ; installation du plugin NVIDIA si besoin.
5. **Déploiement applicatif** : manifestes / charts Helm pour  —

   * *Deployment* du backend (API).
   * *Deployment* d’Ollama (avec ressource `nvidia.com/gpu: 1`, *taint* GPU).
   * Services Kubernetes (ClusterIP ou LoadBalancer) + Ingress/TLS.
6. **Configuration & tests** : DNS / CNAME, règles NSG/Firewall, appels `curl` de validation.

### 1.2 Prérequis clés

* Abonnement Azure actif + quotas GPU (série NC, NCSv3 ou autre).
* Outils CI/CD, Docker, kubectl.
* Accès à Llama ou autre modèle & stockage suffisant.
* Gestion des secrets (Azure Key Vault).

### 1.3 Estimation des coûts mensuels (ordre de grandeur)

| Ressource                     | Coût *pay‑as‑you‑go*          |
| ----------------------------- | ----------------------------- |
| VM GPU **Standard\_NC6s\_v3** | \~3,06 \$/h ⇒ \~2 300 \$/mois |
| Tier AKS Standard (option)    | \~72 \$/mois                  |
| ACR + stockage images         | < 1 \$/mois                   |
| Logs/Monitoring (1 Go/j)      | \~70 \$/mois                  |

* Le prix mensuel peut fortement varier en fonction du type de gpu et du type de plan Azure que l'on souhaite. Ce qui coute vraiment le plus cher est donc la ressource GPU, qui peut être fortement réduite si l'on possède sa propre capacité GPU ou passer par d'autres fournisseur comme OVH.


### 1.4 Architecture scalable proposée

* **AKS** Pod Backend + pods Ollama.
* **Horizontal Pod Autoscaler** pour les pods LLM ; **Cluster Autoscaler** pour pool GPU.
* **Azure Key Vault** pour secrets ; **Azure Monitor** pour métriques/logs.
* Stockages PaaS externes (Cosmos DB, Azure SQL, Blob) pour persistance.

### 1.5 Points d’attention

* Rôles Azure (least‑privilege, Service Principal CI/CD).
* Sécuriser l’API : auth, NSG/IP allowlist, TLS.
* Intégration Azure AD pour AKS & Managed Identity pour pods.
* Prompt‑injection & rate‑limiting côté LLM.

### 1.6 Services Azure recommandés

| Besoin                   | Service                                                    |
| ------------------------ | -----------------------------------------------------------|
| Orchestration conteneurs | **Azure Kubernetes Service**                               |
| Registre d’images        | **Azure Container Registry**                               |
| Secrets & certificats    | **Azure Key Vault**                                        |
| Observabilité            | **Azure Monitor + Application Insights**                   |
| CI/CD                    | **GitHub Actions** ou **Azure DevOps Pipelines**           |
| Stockage persistant      | Cosmos DB / Azure SQL / ou autre service de base de données|

* Azure Kubernetes Service (AKS): Idéal pour les déploiements à grande échelle nécessitant orchestration, montée en charge automatique et gestion fine des ressources. Supporte les nodes GPU pour l’inférence en temps réel.

* Azure Container Instances (ACI): Option serverless pour des déploiements plus simples ou des proofs of concept, sans gestion de cluster. Adapté aux charges variables et facturation à la seconde.

* Azure Virtual Machines (VM) GPU NVv4 / NCas_T4_v3: Pour un contrôle total de l’environnement d’exécution et des performances optimales : VM à GPU pour l’hébergement direct du modèle.

* Azure Container Registry (ACR): Registre privé de conteneurs pour stocker et versionner vos images Docker, avec intégration native aux services Azure.

* Azure Key Vault: Stockage sécurisé des secrets, certificats et clés d’API. Intégration transparente avec AKS et autres services.

* Azure Storage (Blob Storage): Pour stocker les données d’entraînement, journaux ou artefacts, avec haute disponibilité et durabilité.

* Azure Monitor & Log AnalyticsCollecte, analyse et visualisation des métriques et logs : métriques GPU, latences, consommation CPU/mémoire.

* Azure Load Balancer / Application Gateway: Répartition du trafic réseau, routage SSL/TLS et WAF (Application Gateway) pour la sécurité.

* Azure DevOps / GitHub Actions: Pipelines CI/CD pour automatiser les tests, la construction des images Docker et le déploiement sur les environnements Azure.

### 1.7 Considérations de sécurité

* Chiffrement en transit (HTTPS, TLS).
* Scans vulnérabilités images (Defender, ACR scan).
* Logs d’audit activés (KV, AKS, Azure Activity Log).

---

## 2. Stratégie de mise en production

### 2.1 Pipeline CI/CD

1. **CI** : tests (unitaires & intégration), analyse statique, build des images.
2. **Tag & Push** : versionner dans l’ACR.
3. **CD** : déploiement *staging* → tests fumée → *production* (rolling update).
4. **Gestion config** : ConfigMap/Secret, Helm/Kustomize, namespaces isolés.
5. **Rollback** : images précédentes, *kubectl rollout undo* ou blue/green.

### 2.2 Monitoring & Logs

* **Container Insights** : CPU/RAM, GPU usage, logs pod.
* **Application Insights** : latence API, taux erreurs, traces.
* **Alertes** : CPU > 80 %, 5xx > 5 %, restart pods.
* **Dashboards/Workbooks** pour visibilité centralisée.

### 2.3 Gestion des erreurs

* Exceptions gérées + messages clairs.
* Retries sur appels LLM.
* CrashLoop → alerte immédiate.
* Scénario de stresse ou mode dégradé si GPU indisponible.

### 2.4 Stratégie de backup

| Élément           | Méthode                             |
| ----------------- | ----------------------------------- |
| Base de données   | Sauvegarde Azure PITR + export Blob |
| Secrets Key Vault | Soft‑delete + export mensuel        |
| Images ACR        | Geo‑replication, pas de purge       |
| Manifests AKS     | Git ( IaC / GitOps )                |

Test périodique de restauration pour valider les sauvegardes.

---
