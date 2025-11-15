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

```bash
# Anonymize email column in CSV
... -i data.csv:(type=email,column=2)

# Anonymize multiple columns
...  -i data.csv:(type=first_name,column=0) data.csv:(type=last_name,column=1)

# With wildcards
... -i data*.csv:(type=email,column=2)

# Overwrite original file
...  -i data.csv:(type=email,column=2) -o

# Custom delimiter (comma)
...  -i data.csv:(type=email,column=2) -d ','

# Different locale
...  -i data.csv:(type=name,column=0) -l en_US
```

## CLI Arguments

| **Short** | **Long** | **Destination** | **Default** | **Action** | **Description** |
|------------|-----------|----------------|--------------|-------------|------------------|
| `-i` | `--input` | `input` | — | `extend` | One or more input sources.<br><br>**Examples:**<br>• CSV: `inputfile1:(type=number,column=0)`<br>• XML: `inputfile1:(type=last_name,xpath=./person/lastname)`<br>• SQLite: `sqlite://[username:password@]server/database:(input_type=db,type=first_name,table=people,column=first_name)`<br><br>Use multiple arguments to anonymize across multiple files.<br>Supports mixing types (`csv`, `xml`, `json`, …) and wildcards (`*`, `?`). |
| `-t` | `--type` | `type` | `number` | — | Type of data to anonymize (e.g., `name`, `first_name`, `last_name`, `email`, `zip`, `city`, `address`, `number`, …). |
| `-e` | `--encoding` | `encoding` | `ISO-8859-15` | — | File encoding for reading/writing.<br>Example: `UTF-8`. |
| `-d` | `--delimiter` | `delimiter` | `;` | — | CSV column delimiter.<br>Use `--delimiter $'\t'` for tab-separated files. |
| `-l` | `--locale` | `locale` | `de_DE` | — | Locale for generating fake data (e.g., `en_US`, `fr_FR`). |
| `-o` | `--overwrite` | `overwrite` | `False` | `store_true` | Overwrite original file(s) with anonymized data. |
| `-j` | `--ignore-missing-file` | `ignoreMissingFile` | `False` | `store_true` | Ignore missing files instead of failing. |
| — | `--header-lines` | `headerLines` | `0` | — | Number of header lines in CSV files to skip. |
| — | `--namespace` | `namespace` | — | — | Define XML namespaces.<br>**Syntax:** `shortname=http://full-url-of-namespace.com`<br>Multiple can be provided, separated by spaces. |


Check also `.bin/tests.sh` for some sample usages.

See [here](https://github.com/CloudTooling/data-anonymizer/blob/develop/multi_anonymizer.py#L442) for supported [faker](https://faker.readthedocs.io/en/stable/providers.html) types.

## Extending

### As Python Module

```python
from faker import Factory
from jinja2 import Environment
from selector import Selector
from csv_anonymizer import anonymize_csv
from anonymizer import unidecode_filter

faker = Factory.create('de_DE')
template_env = Environment()
template_env.filters['unidecode'] = unidecode_filter

selector = Selector("(type=email,column=2)")
anonymize_csv(
    'input.csv', 'output.csv', [selector],
    0, 'utf-8', ';', faker, template_env
)
```
