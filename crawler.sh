#!/bin/bash

# récupérer les fichiers originaux depuis le site du csa
# et les enregistre dans le dossier src
DESTINATION="src/releves-par-chaine"

echo "------------------------------------"
echo "Suppression des relevés précédents"
echo "------------------------------------"

# supprimer tous les relevés pour être sûr de n'avoir aucune données fausse
# ou obsolètes qui traine; attention à garder le fichier settings.json
rm -rf `find $DESTINATION -name "*" ! -name "settings.json"`

for CHAINE in 1 2 3 4 5 6 8 14 15 16 19 24 26 27 101 102 103 104 105 106 107 108 109 110
do
  echo ""
  echo "-----------------"
  echo "Chaîne $CHAINE"
  echo "-----------------"
  echo ""
  for VARIABLE in 1 2 3 4 5 6 7 8 9 10 11
  do
    FILE="http://www.csa.fr/csaelections/consultereleve/$CHAINE/$VARIABLE/1?csv=1"
    # on vérifie que le content type soit bien notre csv téléchargeable et pas une page html
    # ce qui peut arriver si le fichier est manquant
    ContentType=`curl $FILE -s -I | grep "Content-Type"`
    if [[ $ContentType =~ "application/force-download" ]]; then
      echo "téléchargement du fichier $FILE"
      OUTPUT="$DESTINATION/$CHAINE/$VARIABLE/releve-$VARIABLE.csv";
      curl $FILE --create-dirs --progress-bar --fail -o $OUTPUT;
      # attendre 3 à 6 secondes avant de retélécharger un rapport
      # pour ne pas être trop violent avec le site du csa
      sleep .$[ ( $RANDOM % 4 ) + 3 ]s
    fi
  done
done

