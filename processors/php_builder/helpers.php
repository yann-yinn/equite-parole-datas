<?php

/**
 * Create a php array from a csv string.
 *
 * @param string $path to csv file path
 * @return array
 */
function parse_csv_file_as_array($path) {
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

/**
 * De "00:12:02" à un nombre de secondes
 * @param $time string
 * @return int
 */
function time_hhmmss_to_seconds($time) {
  return strtotime($time) - strtotime('TODAY');
}

/**
 * D'une nombre de secondes à 12h 23min 54s
 * @param $seconds int
 * @return string
 */
function secondes_to_readable_time($seconds) {
  $seconds = round($seconds);
  return sprintf('%02dh %02dm %02ds', ($seconds/3600),($seconds/60%60), $seconds%60);
}

