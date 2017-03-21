'use strict';

const XLSX = require('xlsx');
const _ = require('lodash');

/**
 * change "00:01:30" to number of seconds (90 in this case)
 */
function hhmmss_to_seconds(string) {
  const a = string.split(':'); // split it at the colons
  // minutes are worth 60 seconds. Hours are worth 60 minutes.
  var seconds = (+a[0]) * 60 * 60 + (+a[1]) * 60 + (+a[2]); 
  return seconds;
}

function mapping(value) {
  const mapping = {
    Candidat:  'candidat',
    Soutiens: 'soutiens',
    "Total Temps de parole":'total_temps_de_parole',
    Antenne: 'antenne',
    "Total Temps d'antenne": 'total_temps_antenne',
  }
  return mapping[value];
}

module.exports = function(filename) {
  const workbook = XLSX.readFile(filename);

  // ces deux objets seront transformés chacun en un json
  const perPersona = {};
  const perChannel = {};

  // on va considérer que tout ce qui n'est pas une de ses clefs sera un prénom - nom
  // on aura aussi le "Total Candidat" avec, ce n'est pas très grave.
  // Ce "Total Candidat" est d'ailleurs parfois au début de la feuille, parfois à la fin...
  const KEYS = ['Candidat', 'Soutiens', 'Total Temps de parole', "Total Temps d'antenne", "Antenne"];

  channelLoop:
  // le fichier excel contient une feuille par canal / chaine
  for(const canal of workbook.SheetNames) {
    let persona = '';
    let truePersona = '';
    let attrs = [];
    let finalattrs = [];
    for (const cell in workbook.Sheets[canal]) {

      // on ne s'occupe que des deux première collones (A et B), au delà on skip
      if(cell[0] === '!' || cell[0] === 'C' || cell === 'A1' || cell === 'B1' ) continue;

      // La colonne A contient le nom des candidats suivis de leurs attributs
      if(cell[0] === 'A') {
        // si on arrive sur une ligne qui contient le nom du candidat
        if(KEYS.indexOf(workbook.Sheets[canal][cell].v) === -1) {
          if(persona) {
            // il y a parfois des parenthèses qui trainent, on vire.
            // par exemple : François Bayrou (soutien de Macron depuis xxx)
            truePersona = persona.replace(/\s*\(.*?\)\s*/g, '');
            // on ne veut pas la ligne du total des candidats dans notre json
            if (persona !== 'Total candidats') {
              finalattrs = _.fromPairs(_.chunk(attrs,2));
              _.set(perPersona, `${truePersona}.${canal}`, finalattrs);
              _.set(perChannel, `${canal}.${truePersona}`, finalattrs);
            }
            attrs = [];
          }
          persona = workbook.Sheets[canal][cell].v;
          continue;
        }
        // si on est sur une ligne qui ne contient PAS le nom du candidat
        else {
          let value = workbook.Sheets[canal][cell].v;
          value = mapping(value);
          attrs.push(value);
          continue;
        }
      }

      // la colonne B contient la valeur de nos attributs contenus dans la colonne A
      if (cell[0] === 'B') {
        let value = hhmmss_to_seconds(workbook.Sheets[canal][cell].w);
        attrs.push(value);
      } 

    }
  }

  return { perPersona, perChannel };
}

