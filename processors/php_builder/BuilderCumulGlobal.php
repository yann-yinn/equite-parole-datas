<?php

class BuilderCumulGlobal {

  public $csv_as_array = [];
  public $mapping = [
    "Candidat" => 'candidat',
    "Soutiens" => 'soutien',
    "Antenne" => 'antenne',
    "Total Temps d'antenne" => 'total_temps_antenne',
    "Total Temps de parole" => 'total_temps_de_parole',
  ];

  function __construct($filepath) {
    $this->csv_as_array = parse_csv_file_as_array($filepath);
  }

  /**
   * Transforme le tableau du csv original en un tableau exploitable
   * @return array
   */
  function process($csv_as_array) {
    $array = [];
    foreach ($csv_as_array as $key => $datas) {
      if ($datas[1] == 'Total candidats') continue;
      $seconds = time_hhmmss_to_seconds($datas[3]);
      $readable = secondes_to_readable_time($seconds);
      $array[$datas[1]][$this->mapping[$datas[2]]] = [
        'temps_brut' => $datas[3],
        'pourcentage' => $datas[4],
        'secondes' => $seconds,
        'temps' => $readable
      ];
    }
    return $array;
  }

  function writeAsJson($destination) {
    $jsonArray = $this->process($this->csv_as_array);
    $json = json_encode($jsonArray, JSON_PRETTY_PRINT);
    file_put_contents($destination, $json);
  }

}


