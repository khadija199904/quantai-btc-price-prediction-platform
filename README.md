Voici une version enrichie et finalisée de votre **README.md**, intégrant les éléments que vous avez fournis tout en respectant une structure professionnelle adaptée à un projet de certification (RNCP).

---

# 🪙 Quant-AI : Plateforme de Prédiction Haute Fréquence BTC/USDT

[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://www.python.org/)
[![Spark](https://img.shields.io/badge/Apache_Spark-3.5-orange)](https://spark.apache.org/)

## 1. Présentation du Projet
Ce projet consiste à développer une plateforme **"end-to-end"** capable de transformer des flux de données financiers bruts en prédictions actionnables. La plateforme récupère les données de marché (OHLC, volumes) sur l'API Binance, les traite via une infrastructure distribuée, entraîne un modèle de Machine Learning pour prédire le prix du Bitcoin à **T+10 minutes**, et expose les résultats via une API REST sécurisée.

### Contexte Métier
Dans le secteur de la Fintech et des hedge funds, la capacité à traiter des flux de données massifs en temps réel est un avantage concurrentiel majeur. La société **Quant-AI** souhaite valider ce prototype pour passer d'une analyse statique à un système industriel automatisé, robuste et sécurisé.

---

## 2. Fonctionnalités Clés
- **Ingestion Temps Réel** : Collecte automatisée des Klines (1 min) via l'API Binance.
- **Architecture Medallion** : Pipeline de données structuré en zones (Bronze, Silver).
- **Traitement Distribué** : Feature engineering à grande échelle avec **PySpark**.
- **Prédiction IA** : Modèle de régression sur séries temporelles (cible T+10 min).
- **Orchestration** : Automatisation complète des flux avec **Airflow**.
- **API REST Sécurisée** : Accès aux prédictions via **FastAPI** avec authentification **JWT**.

---

## 3. Stack Technologique
| Domaine | Technologies |
| :--- | :--- |
| **Langage** | Python (PySpark, Pandas, Scikit-learn) |
| **Big Data** | Apache Spark, Parquet |
| **Bases de données** | PostgreSQL |
| **Backend & Sécurité** | FastAPI, JSON Web Tokens (JWT) |
| **Orchestration** | Apache Airflow, Docker, Docker Compose |
| **Versionning & Agilité** | Git, Kanban |

---

##  4. Architecture de la Donnée
Le projet suit une logique de montée en qualité de la donnée :

1.  **Zone Bronze** : Stockage des données brutes JSON issues de l'API Binance.
2.  **Zone Silver** : Données nettoyées, typées et enrichies d'indicateurs techniques via PySpark.
3.  **Service Layer (Gold)** : Prédictions stockées en SQL et exposées via l'API.

### Logic de Feature Engineering (PySpark)
Pour chaque minute ($t$), nous calculons :
- **Target ($y$)** : Prix de clôture à $t+10$ (via `F.lead("close", 10)`).
- **Returns** : Variation relative du prix de clôture.
- **Moyennes Mobiles** : MA(5) et MA(10) pour lisser les bruits de marché.
- **Taker Ratio** : Mesure de l'agressivité des acheteurs (`taker_buy_base_asset_volume / volume`).

---

## 5. Organisation de l'Équipe
Le projet est réalisé par une équipe de 3 experts :

*   **Data Engineer (Lead Pipeline)** : Ingestion Binance, stockage Medallion, PySpark ETL et orchestration Airflow.
*   **Machine Learning Engineer (Lead Modèle)** : Feature engineering, entraînement du modèle de régression, évaluation (RMSE/MAE) et sérialisation.
*   **Backend & Security Engineer (Lead API)** : Développement de l'API FastAPI, sécurisation JWT et endpoints analytiques.

---

##  6. Installation et Lancement

### Prérequis
- Docker & Docker Compose
- Un environnement Python 3.10

### Installation
1. **Cloner le projet** :
   ```bash
   git clone https://github.com/votre-repo/quant-ai-prediction.git
   cd quant-ai-prediction
   ```
2. **Configurer l'environnement** :
   Créer un fichier `.env` avec vos accès API Binance et secrets JWT.
3. **Lancer l'infrastructure** :
   ```bash
   docker-compose up -d
   ```

---

## 📈 7. Cas d'Utilisation
- **Aide à la décision** : Fournir aux traders une tendance court terme fiable.
- **Algorithmic Trading** : Intégration des prédictions dans des bots d'exécution.
- **Analyse de Marché** : Centralisation des indicateurs techniques enrichis pour la recherche quantitative.

---

## 🎓 8. Certification
Ce projet s'inscrit dans le cadre de la **Certification RNCP Développeur.se en intelligence artificielle (2023)**. Il valide les compétences en :
- Algorithmique & SQL
- Big Data (Spark)
- Machine Learning (Régression sur séries temporelles)
- DevOps & Orchestration
- Développement d'API sécurisées

---
**Période du projet :** 19/01/2026 - 23/01/2026
**Société :** Quant-AI