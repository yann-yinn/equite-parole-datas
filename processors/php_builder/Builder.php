<?php

class Builder {

  public $csv_as_array = [];
  public $array = [];
  public $mapping = [
    "Candidat" => 'candidat',
    "Soutiens" => 'soutien',
    "Antenne" => 'antenne',
    "Total Temps d'antenne" => 'total_temps_antenne',
    "Total Temps de parole" => 'total_temps_de_parole',
  ];

  function __construct($filepath) {
    $this->filepath =$filepath;
    $this->csv_as_array = get_csv_file_and_parse_it_as_array($filepath);
  }

  function process() {
    $array = [];
    foreach ($this->csv_as_array as $key => $datas) {
      $this->array[$datas[1]][$this->mapping[$datas[2]]] = [
        'temps_brut' => $datas[3],
        'pourcentage' => $datas[4],
        'secondes' => strtotime($datas[3]) - strtotime('TODAY')
      ];
    }
    return $array;
  }

  function writeJson($destination) {
    $json = json_encode($this->process(), JSON_PRETTY_PRINT);
    file_put_contents($destination, $json);
  }

  function writeCsv($destination) {

  }

}


