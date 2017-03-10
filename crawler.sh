#!/bin/bash

# récupérer les fichiers originaux depuis le site du csa
# et les enregistre dans le dossier src

echo "------------------------------------"
echo "Suppression des relevés précédents"
echo "------------------------------------"
rm -rf !(settings.json) "src/releves"

for CHAINE in 1 2 3 4 5 6 8 14 15 16 19 24 26 27 101 102 103 104 105 106 107 108 109 110
do
  echo ""
  echo "-----------------"
  echo "Chaîne $CHAINE"
  echo "-----------------"
  echo ""
  for VARIABLE in 1 2 3 4 5 6
  do
    FILE="http://www.csa.fr/csaelections/consultereleve/$CHAINE/$VARIABLE/1?csv=1"
    # on vérifie que le content type soit bien notre csv téléchargeable et pas une page html
    # ce qui peut arriver si le fichier est manquant
    ContentType=`curl $FILE -s -I | grep "Content-Type"`
    if [[ $ContentType =~ "application/force-download" ]]; then
      echo "téléchargement du fichier $FILE"
      DESTINATION="src/releves/$CHAINE/$VARIABLE/releve-$VARIABLE.csv";
      curl $FILE --create-dirs --progress-bar --fail -o $DESTINATION;
      # attendre 3 à 6 secondes avant de retélécharger un rapport
      # pour ne pas être trop violent avec le site du csa
      sleep .$[ ( $RANDOM % 4 ) + 3 ]s
    fi
  done
done

