

```markdown
# Projet NLP Enriched News

Ce projet a pour but d'enrichir des articles de presse à l'aide de techniques de traitement du langage naturel (NLP). Ce `README.md` explique comment installer les dépendances, configurer l'environnement, et exécuter le script principal.


## Installation des dépendances

### 1. Cloner le projet

Clone ce projet depuis le dépôt Git :

```bash
git clone https://url_de_ton_projet.git
cd ton_projet
```

### 2. Créer et activer un environnement virtuel

Il est recommandé de créer un environnement virtuel pour isoler les dépendances de ton projet.

- Sur **Linux/macOS** :

  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

- Sur **Windows** :

  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Installer les dépendances

Installe toutes les dépendances nécessaires en utilisant le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 4. Lancer le script principal

Une fois les dépendances installées, tu peux exécuter le script principal du projet :

```bash
python nlp_enriched_news.py
```

install requirement
conda create --name <env> --file <this file>

Cela devrait démarrer le processus de traitement des articles de presse enrichis par NLP.


**Note**

Modèle avec une bonne capacité de généralisation : Si la courbe de test s'améliore continuellement, cela montre que le modèle apprend de manière stable et qu'il est capable de généraliser de mieux en mieux à mesure que l'on lui donne plus d'exemples.

Absence de sur-apprentissage (overfitting) : La courbe d'entraînement constante indique que le modèle ne continue pas à sur-ajuster les données d'entraînement. S'il y avait du sur-apprentissage, on s'attendrait à voir la courbe d'entraînement diminuer rapidement, tandis que la courbe de test stagnerait ou empirerait.

Absence de sous-apprentissage (underfitting) : Si le modèle était sous-apprenant, la courbe d'entraînement et la courbe de test resteraient toutes deux à des niveaux élevés d'erreur (ou faibles de performance) et ne s'amélioreraient pas beaucoup, même avec plus de données d'entraînement. Ici, ton modèle semble assez bien apprendre, car la courbe de test s'améliore



# pip install -U spacy
# python -m spacy download en_core_web_sm


Pourquoi choisir le score maximum dans ce cas ?
Le score maximum semble être le meilleur choix dans ce contexte pour plusieurs raisons :
Mettre en avant les articles les plus frappants : Le score maximum permettra de repérer immédiatement les articles qui contiennent les passages les plus pertinents, même si seulement une ou deux phrases dans l'article mentionnent le sujet clé. Si une phrase est particulièrement pertinente, vous voulez que l'article soit classé parmi les meilleurs, même si d'autres phrases sont moins pertinentes.
Identifier les articles les plus marquants : Lorsque vous sélectionnez les 10 articles les plus marquants, l'impact de chaque phrase individuelle (et pas simplement la moyenne) doit être pris en compte. Un article avec une phrase particulièrement forte, même s'il y a d'autres mentions faibles, devrait apparaître dans votre top 10.
Réflexion de l'intensité du scandale : Un seul passage très pertinent dans un article pourrait signaler un scandale environnemental majeur. Par exemple, un article qui mentionne explicitement la déforestation dans un contexte très critique doit être sélectionné même si une majorité des autres phrases n'ont pas de lien direct.



https://googlechromelabs.github.io/chrome-for-testing/

curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh

https://medium.com/eni-digitalks/text-preprocessing-nlp-fundamentals-with-spacy-54f32e520bc8

https://scikit-learn.org/dev/auto_examples/model_selection/plot_learning_curve.html#sphx-glr-auto-examples-model-selection-plot-learning-curve-py

https://www.alliage-ad.com/data-science/structures-de-sauvegarde-de-modele-de-machine-learning-le-format-pickle/