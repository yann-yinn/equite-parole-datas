<?php

/**
 * Create a php array from a csv string.
 *
 * @param string $path csv file path
 * @return array
 */
function get_csv_file_and_parse_it_as_array($path, $csv_separator = ',') {
  $row = 1;
  $csv = [];
  if (($handle = fopen($path, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, $csv_separator)) !== FALSE) {
      $num = count($data);
      $row++;
      for ($c=0; $c < $num; $c++) {
        $csv[$row][] = $data[$c];
      }
    }
    fclose($handle);
  }
  return $csv;
}

$paths = [
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/tf1.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/france2.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/france3.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/canal-plus.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/france5.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/m6.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/c8.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/tmc.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/rmc-decouverte.csv",
  "src/2017-02-01--2017-02-26/csv/chaines-generalistes/franceo.csv",
];

$datas = [];
foreach ($paths as $path) {
  $datas[$path] = get_csv_file_and_parse_it_as_array($path);
}

print_r($datas);