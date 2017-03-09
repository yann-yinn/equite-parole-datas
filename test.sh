#!/bin/bash

ContentType=`curl -I http://www.csa.fr/csaelections/consultereleve/1/1/1\?csv\=1 -s | grep "Content-Type"`
if [[ $ContentType =~ "application/force-download" ]]; then
    echo $ContentType
fi


