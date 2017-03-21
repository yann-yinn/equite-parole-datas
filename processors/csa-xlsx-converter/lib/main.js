'use strict';

const XLSX = require('xlsx');
const _ = require('lodash');

module.exports = function(filename) {
  const workbook = XLSX.readFile(filename);

  // ces deux objets seront transformés chacun en un json
  const perPersona = {};
  const perChannel = {};

  // on va considérer que tout ce qui n'est pas une de ses clefs sera un prénom - nom
  // on aura aussi le "Total Candidat" avec, ce n'est pas très grave.
  // Ce "Total Candidat" est d'ailleurs parfois au début de la feuille, parfois à la fin...
  const ROWS = ['Candidat', 'Soutiens', 'Total Temps de parole', "Total Temps d'antenne", "Antenne"];

  channelLoop:
  // le fichier excel contient une feuille par canal / chaine
  for(const canal of workbook.SheetNames) {
    let persona = '';
    let truePersona = '';
    let attrs = [];
    let finalattrs = [];
    for (const cell in workbook.Sheets[canal]) {
      if(cell[0] === '!' || cell[0] === 'C' || cell === 'A1' || cell === 'B1' ) continue;
      if(cell[0] === 'A') {
        // si on arrive sur une ligne qui contient uniquement le nom du candidat
        if(ROWS.indexOf(workbook.Sheets[canal][cell].v) === -1) {
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
          attrs.push(workbook.Sheets[canal][cell].v);
          continue;
        }
      }
      attrs.push(workbook.Sheets[canal][cell].w);
    }
  }

  return { perPersona, perChannel };
}
