'use strict';

const XLSX = require('xlsx');
const _ = require('lodash');

module.exports = function(filename) {
  const workbook = XLSX.readFile(filename);

  const perPersona = {};
  const perChannel = {};

  const PERSONA_RECOGNITION = /^([A-Z\s]+)(?:\s\(.+\))?$/;

  const END_INFOS = /^Total candidats/i;

  channelLoop:
  for(const canal of workbook.SheetNames) {
    let persona = '';
    let truePersona = '';
    let attrs = [];
    let finalattrs = [];
    for (const cell in workbook.Sheets[canal]) {
      if(cell[0] === '!' || cell[0] === 'C' || cell === 'A1' || cell === 'B1' ) continue;
      //if(END_INFOS.test(workbook.Sheets[canal][cell].v)) continue channelLoop;
      if(cell[0] === 'A') {
        if(PERSONA_RECOGNITION.test(workbook.Sheets[canal][cell].v)) {
          if(persona) {
            truePersona = PERSONA_RECOGNITION.exec(persona)[1];
            finalattrs = _.fromPairs(_.chunk(attrs,2));
            _.set(perPersona, `${truePersona}.${canal}`, finalattrs);
            _.set(perChannel, `${canal}.${truePersona}`, finalattrs);
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
