#!/bin/bash

# installer et mettre à jour les modules nodes
npm install
npm update

# Génération des fichiers csv
python3 processors/python_builder/Main.py

php processors/php_builder/main.php

node_modules/csa-xlsx-converter/bin/csa-xlsx-converter -t "src/releves-par-groupe-de-chaines/2017-02-01--2017-02-26/originaux/Chaines Gen - Période du 1er au 26 février 2017.xlsx" -o "dist/api/v1/2017-02-01--2017-02-26/" -p "chaines-generalistes-"

