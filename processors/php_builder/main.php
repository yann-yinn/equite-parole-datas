<?php

require('helpers.php');
require('BuilderCumulGlobal.php');

$builder = new BuilderCumulGlobal("src/releves-cumul_global/TP-TA_Presidentielle_2017_1er février au 5 mars 2017.csv");
$builder->writeAsJson("dist/api/v1/2017-02-01--2017-03-05/tous-les-medias.json");


