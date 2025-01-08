[![Build](https://github.com/CloudTooling/data-anonymizer/actions/workflows/build.yml/badge.svg)](https://github.com/CloudTooling/data-anonymizer/actions/workflows/build.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/cloudtooling/data-anonymizer)](https://hub.docker.com/r/cloudtooling/data-anonymizer)


# Usage

```
docker run -v $(pwd):/input cloudtooling/data-anonymizer -t xml -i "input/my.xml:(type=street,xpath=//Strasse)"
```
or
```
inputFile=input/my.xml
docker run -v $(pwd):/input cloudtooling/data-anonymizer -t xml -i \
  "$inputFile:(type=street,xpath=//Strasse)" \
  "$inputFile:(type=number,xpath=//HausNr)" \
  "$inputFile:(type=zip,xpath=//PLZ)" \
  "$inputFile:(type=city,xpath=//Ort)" \
  "$inputFile:(type=city_suffix,xpath=//Ortsteil)" \
  "$inputFile:(type=city_suffix,xpath=//KreisRegion)" \
  "$inputFile:(type=last_name,xpath=//Nachname)" \
  "$inputFile:(type=first_name,xpath=//Vorname)" \
  "$inputFile:(type=name,xpath=//Ansprechpartner)" \
  "$inputFile:(type=name,xpath=//GeschFuehrer)" \
  "$inputFile:(type=passport_number,xpath=//HRNr)" \
  "$inputFile:(type=url,xpath=//Homepage)" \
  "$inputFile:(type=email,xpath=//Email)" \
  "$inputFile:(type=phone_number,xpath=//TelefonNr)" \
  "$inputFile:(type=phone_number,xpath=//MobilNr)" \
  "$inputFile:(type=phone_number,xpath=//FaxNr)"
```

See [here](https://github.com/CloudTooling/data-anonymizer/blob/develop/multi_anonymizer.py#L442) for supported [faker](https://faker.readthedocs.io/en/stable/providers.html) types.
