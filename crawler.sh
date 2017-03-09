#!/bin/bash

# récupérer les fichiers originaux depuis le site du csa
# et les enregistre dans le dossier src

echo "-----------------"
echo "Suppression des relevés précédents"
echo "-----------------"
rm -rf "src/releves"

for CHAINE in 1 2 3 4 5 6 8 14 15 16 19 24 26 27 101 102 103 104 105 106 107 108 109 110
do
  echo ""
  echo "-----------------"
  echo "Chaîne $CHAINE"
  echo "-----------------"
  echo ""
  for VARIABLE in 1 2 3 4
  do
    FILE="http://www.csa.fr/csaelections/consultereleve/$CHAINE/$VARIABLE/1?csv=1"
    echo "téléchargement du fichier $FILE"
    DESTINATION="src/releves/$CHAINE/$VARIABLE/releve-$VARIABLE.csv";
    curl $FILE --create-dirs --progress-bar -o $DESTINATION;
    sleep .$[ ( $RANDOM % 4 ) + 3 ]s
  done
done

