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

function array_2_csv($array) {
  $csv = array();
  foreach ($array as $item) {
    if (is_array($item)) {
      $csv[] = array_2_csv($item);
    } else {
      $csv[] = $item;
    }
  }
  return implode(',', $csv);
}

/**
 * Formats a line (passed as a fields  array) as CSV and returns the CSV as a string.
 * Adapted from http://us3.php.net/manual/en/function.fputcsv.php#87120
 */
function arrayToCsv( array &$fields, $delimiter = ';', $enclosure = '"', $encloseAll = false, $nullToMysqlNull = false ) {
  $delimiter_esc = preg_quote($delimiter, '/');
  $enclosure_esc = preg_quote($enclosure, '/');

  $output = array();
  foreach ( $fields as $field ) {
    if ($field === null && $nullToMysqlNull) {
      $output[] = 'NULL';
      continue;
    }

    // Enclose fields containing $delimiter, $enclosure or whitespace
    if ( $encloseAll || preg_match( "/(?:${delimiter_esc}|${enclosure_esc}|\s)/", $field ) ) {
      $output[] = $enclosure . str_replace($enclosure, $enclosure . $enclosure, $field) . $enclosure;
    }
    else {
      $output[] = $field;
    }
  }

  return implode( $delimiter, $output );
}