'use strict';

const XLSX = require('xlsx');
const _ = require('lodash');

module.exports = function(filename) {
  const workbook = XLSX.readFile(filename);

  const perPersona = {};
  const perChannel = {};

  const PERSONA_RECOGNITION = /^([A-Z\s]+)(?:\s\(.+\))?$/;

  // on va considérer que tout ce qui n'est pas une de ses clefs sera un prénom - nom
  const ROWS = ['Candidat', 'Soutiens', 'Total Temps de parole', "Total Temps d'antenne", "Antenne"]

  //const TOTAL_RECO = /^Total candidats/i;

  channelLoop:
  for(const canal of workbook.SheetNames) {
    let persona = '';
    let truePersona = '';
    let attrs = [];
    let finalattrs = [];
    for (const cell in workbook.Sheets[canal]) {
      if(cell[0] === '!' || cell[0] === 'C' || cell === 'A1' || cell === 'B1' ) continue;
      if(cell[0] === 'A') {
        if(ROWS.indexOf(workbook.Sheets[canal][cell].v) === -1) {
          if(persona) {
            finalattrs = _.fromPairs(_.chunk(attrs,2));
            _.set(perPersona, `${persona}.${canal}`, finalattrs);
            _.set(perChannel, `${canal}.${persona}`, finalattrs);
            attrs = [];
          }
          persona = workbook.Sheets[canal][cell].v;
          continue;
        } else {
          attrs.push(workbook.Sheets[canal][cell].v);
          continue;
        }
      }
      attrs.push(workbook.Sheets[canal][cell].w);
    }
  }

  return { perPersona, perChannel };
}
