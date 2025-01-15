#!/usr/bin/env bash

inputFile=testfiles/addresses.xml
./multi_anonymizer.py -t xml -i \
    "$inputFile:(type=name,xpath=//firstname)" \
    "$inputFile:(type=name,xpath=//lastname)" \
    "$inputFile:(type=city,xpath=//city)" \
    "$inputFile:(type=zip,xpath=//zip)"

inputFile=testfiles/addresses_ns.xml
./multi_anonymizer.py -t xml -i \
    "$inputFile:(type=name,xpath=//firstname)" \
    "$inputFile:(type=name,xpath=//lastname)" \
    "$inputFile:(type=city,xpath=//city)" \
    "$inputFile:(type=zip,xpath=//zip)"

inputFile=testfiles/addresses.json
./multi_anonymizer.py -t json -i \
    "$inputFile:(type=name,jsonpath=$.addressbook.person[*].firstname)" \
    "$inputFile:(type=name,jsonpath=$.addressbook.person[*].lastname)" \
    "$inputFile:(type=street,jsonpath=$.addressbook.person[*].address[*].street)" \
    "$inputFile:(type=zip,jsonpath=$.addressbook.person[*].address[*].zip)" \
    "$inputFile:(type=city,jsonpath=$.addressbook.person[*].address[*].city)"

inputFile=testfiles/addresses_simple.json
./multi_anonymizer.py -t json -i \
    "$inputFile:(type=name,jsonpath=$.addressbook.person[*].firstname)" \
    "$inputFile:(type=name,jsonpath=$.addressbook.person[*].lastname)" \
    "$inputFile:(type=street,jsonpath=$.addressbook.person[*].address[*].street)" \
    "$inputFile:(type=zip,jsonpath=$.addressbook.person[*].address[*].zip)" \
    "$inputFile:(type=city,jsonpath=$.addressbook.person[*].address[*].city)"

inputFile=testfiles/addresses.csv
./multi_anonymizer.py -t csv -i \
    "$inputFile:(type=number,column=1)" \
    "$inputFile:(type=address,column=2)"

inputFile=testfiles/persons.csv
./multi_anonymizer.py -t csv -i \
    "$inputFile:(type=first_name,column=1)" \
    "$inputFile:(type=last_name,column=1)"

inputFile=testfiles/persons_regexp.csv
./multi_anonymizer.py -t csv -i \
    "$inputFile:(type=name,column=1)" \
    "$inputFile:(type=email,column=1)"
