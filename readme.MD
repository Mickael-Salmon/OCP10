﻿
<p align="center">
<img src="https://legacy.python.org/community/logos/python-logo-master-v3-TM.png">
</p>

# Bienvenue !
## Vous trouverez ici le Projet 10 du parcours Développeur d'application - Python 👋

# Créez une API sécurisée RESTful en utilisant Django REST 💻 !

# Scénario SoftDesk Support API 🚀

Bienvenue sur le dépôt du projet **SoftDesk Support API** ! Notre mission est de fournir une solution de suivi des problèmes techniques pour les entreprises en B2B.

![SoftDesk Logo](https://user.oc-static.com/upload/2023/06/28/16879473703315_P10-02.png)

___

## 📌 Fonctionnalités

-   **Modèles d'objets** : Gérez efficacement vos objets dans notre application.
-   **Fonctionnalités principales** : Une suite complète d'outils pour le suivi des problèmes techniques.
-   **Points de terminaison d'API** : Une interface robuste pour servir des applications front-end sur différentes plateformes.

___

## 🛡️ Sécurité & Optimisation

-   **OWASP** : Respect des mesures de sécurité OWASP, authentification via JWT et permissions d'accès granulaires.
-   **RGPD** : Garantit la protection des données et la confidentialité des utilisateurs.
-   **Green Code** : Nous visons à optimiser et simplifier le code pour la sobriété énergétique.

___

## 📂 Documentation

1.  **Conception de la mise en œuvre** : Diagramme et description des modèles d'objets, fonctionnalités principales, et points de terminaison d'API.
2.  **Exigences de sécurité et d’optimisation** : Détails sur les spécifications OWASP, RGPD et Green Code.

___

## 🖥️ Comment commencer ?

## 🛠️ Instructions d'installation

### Prérequis :

-   Avoir Python d'installé. Si ce n'est pas le cas, vous pouvez le télécharger [ici](https://www.python.org/downloads/).
-   [Poetry](https://python-poetry.org/), un outil pour la gestion des dépendances en Python.

### Étapes :

1.  **Clonage du dépôt :**

    ``` bash
    git clone <URL_DU_REPO>
    cd <NOM_DU_REPO>

    ```

2.  **Installation de Poetry :**

    -   **Sur Linux/macOS :**

        ``` bash
        curl -sSL https://install.python-poetry.org | python3 -

        ```

    -   **Sur Windows (PowerShell) :**

        ``` powershell
        (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

        ```

3.  **Installation des dépendances :**
    Utilisez Poetry pour installer les dépendances du projet.

    ``` bash
    poetry install

    ```

4.  **Activation de l'environnement virtuel créé par Poetry :**

    -   **Sur Linux/macOS :**

        ``` bash
        poetry shell

        ```

    -   **Sur Windows :** Ouvrez une nouvelle fenêtre de terminal et naviguez vers le dossier du projet, puis exécutez :

        ``` powershell
        poetry shell

        ```

5.  **Effectuez les migrations initiales :**

    ``` bash
    python manage.py migrate

    ```

6.  **Lancez le serveur de développement :**

    ``` bash
    python manage.py runserver

    ```


Le serveur devrait démarrer, et l'API devrait être accessible à `http://localhost:8000/`.

___

## 📞 Contact


___

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

___

💡 N'oubliez pas de jeter un œil à nos autres projets chez **SoftDesk**. Bon codage ! 🎉
