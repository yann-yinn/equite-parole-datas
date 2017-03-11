<?php

/**
 * Create a php array from a csv string.
 *
 * @param string $path csv file path
 * @return array
 */
function get_csv_file_and_parse_it_as_array($path) {
  $row = 1;
  $csv = [];
  if (($handle = fopen($path, "r")) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ";")) !== FALSE) {
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
