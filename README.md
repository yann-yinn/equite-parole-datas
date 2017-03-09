#CSA - Données au format JSON et CSV des temps de parole et d'antenne des candidats à la présidentielle 2017

Récupére et parse automatiquement en fichiers csv et JSON les données des temps d'antenne des candidats depuis le site http://csa.fr
Les données générées dans le répertoire "dist" sont ensuite mises à disposition sur https://c43-drupal.service.dev.local.niji.delivery/

#INSTALLATION

# Python

## Requis :

- Python3.4

## Build :
Dans un terminal :
```shell
/usr/bin/python3.4 buiders/python_builder/Main.py
```

# ORGANISATIONS DES DOSSIERS

- src : contient les données téléchargés depuis le site du CSA
- dist : contient les données JSON qu'on peut mettre à disposition de tous. C'est ce répertoire qui est mis à disposition dans le répertoire "api" de http://equite-parole.github.io
- processors : contient les scripts traitant les données du site du CSA pour en faire des données exploitables

