#CSA - Données ouvertes au format JSON et CSV des temps de parole et d'antenne des candidats à la présidentielle 2017

Récupére et parse automatiquement en fichiers JSON et csv les données des temps d'antenne des candidats depuis le site http://csa.fr
Les données générées sont dans le répertoire "dist" et sont ensuite mises à disposition sur http://equite-parole.github.io

#INSTALLATION

# Requis :
- Python3.4 ou >
- Node 7

## Build :
Dans un terminal :
```shell
# seulement si vous voulez re-télécharger tous les relevés csv par chaîne  (src/releves)
./crawlers.sh
# relancher le traitement des données du CSA et la génération des JSON et CSV
./build.sh
```

#COMMENT CONTRIBUER

Voir ici https://github.com/nyl-auster/equite-parole-datas/wiki/R%C3%A8gles-de-contributions-%C3%A0-%22%C3%89quit%C3%A9-de-parole%22

# ORGANISATIONS DES DOSSIERS ET FICHIERS

- crawler.sh : télécharge depuis le site du CSA les relevés par chaines et période
- build.sh : lance la génération des fichiers JSON et CSV compilés à partir des données sources
- src : contient les données téléchargés depuis le site du CSA
- dist : contient le répertoir csv et api directement servis ensuite par equite-parole.github.io
- processors : contient les scripts traitant les données du site du CSA pour en faire des données exploitables

