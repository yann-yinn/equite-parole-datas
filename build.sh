#!/bin/bash

# installer et mettre à jour les modules nodes
npm install csa-xlsx-converter
npm update csa-xlsx-converter

# Génération des fichiers JSON et csv par les processors existants
python3 processors/python_builder/Main.py

#php processors/php_builder/main.php

# generation des fichiers JSON par chaines / candidats
processors/csa-xlsx-converter/bin/csa-xlsx-converter -t "src/releves-par-groupe-de-chaines/2017-02-01--2017-02-26/originaux/Chaines Gen - Période du 1er au 26 février 2017.xlsx" -o "dist/api/v1/2017-02-01--2017-02-26/" -p "chaines-generalistes-"
processors/csa-xlsx-converter/bin/csa-xlsx-converter -t "src/releves-par-groupe-de-chaines/2017-02-01--2017-03-12/originaux/TV  - Période du 1er fév.  au 12-03.xlsx" -o "dist/api/v1/2017-02-01--2017-03-12/" -p "chaines-generalistes-"
processors/csa-xlsx-converter/bin/csa-xlsx-converter -t "src/releves-par-groupe-de-chaines/2017-02-01--2017-03-12/originaux/Info  - Période du 1er Fév. au 12 mars.xlsx" -o "dist/api/v1/2017-02-01--2017-03-12/" -p "chaines-informations-"
processors/csa-xlsx-converter/bin/csa-xlsx-converter -t "src/releves-par-groupe-de-chaines/2017-02-01--2017-03-12/originaux/Radio - 1 Fév au 12 mars.xlsx" -o "dist/api/v1/2017-02-01--2017-03-12/" -p "radios-"

