# Oiviranje
SQL Injection Analyzer
Opis
Orodje za statično analizo kode, ki zazna:
SQL Injection
HQL Injection
Command Injection

Podprti jeziki:
Python
JavaScript
PHP

Kako deluje
Parser analizira kodo
Detector prepozna nevarne vzorce
Pipeline oceni tveganje
Report vrne rezultat

## Project Structure
# 🛡️ SQL Injection Analyzer – SPECIFIKACIJA PROJEKTA

---

# 📁 STRUKTURA PROJEKTA

sql-injection-analyzer/
│
├── app/
│   ├── main.py
│   ├── cli.py
│   └── config.py
│
├── parsers/
│   ├── base.py
│   ├── python_parser.py
│   ├── js_parser.py
│   └── php_parser.py
│
├── detectors/
│   ├── base.py
│   └── injection_detector.py
│
├── models/
│   ├── finding.py
│   ├── result.py
│   └── enums.py
│
├── rules/
│   └── injection_rules.py
│
├── reporting/
│   └── report.py
│
├── examples/
│   ├── scenario1_sql.py
│   ├── scenario2_hql.java
│   └── scenario3_cmd.java
│
├── README.md
└── requirements.txt

---

# 🔁 GLAVNI FLOW APLIKACIJE

USER INPUT (koda + jezik)
        ↓
app/main.py
        ↓
Analyzer (glavni orchestrator)
        ↓
Parser (Python / JS / PHP)
        ↓
Findings (strukturirani rezultati)
        ↓
InjectionDetector (analiza + rules)
        ↓
Report (formatiranje izpisa)
        ↓
OUTPUT (security report)

---

# 📁 APP MODUL

## main.py
NAMEN:
Glavna vstopna točka aplikacije.

INPUT:
- koda (string)
- jezik (python/js/php)

OUTPUT:
- security report (string)

FUNKCIJA:
- zažene Analyzer
- izpiše rezultat

---

## cli.py
NAMEN:
CLI vmesnik za zagon iz terminala.

INPUT:
--file (pot do kode)
--lang (jezik)

OUTPUT:
- parsed arguments

FUNKCIJA:
- omogoča zagon programa preko terminala

---

## config.py
NAMEN:
Globalne nastavitve sistema.

VSEBINA:
- podprti jeziki
- tipi napadov

---

# 📁 PARSERS (ANALIZA KODE)

## base.py
NAMEN:
Interface za vse parserje.

FUNKCIJA:
def parse(code)

OUTPUT:
list[Finding]

---

## python_parser.py
NAMEN:
Analiza Python kode.

DETEKCIJA:
- string concatenation
- input()
- exec/system calls

INPUT:
Python koda (string)

OUTPUT:
list Finding

---

## js_parser.py
NAMEN:
Analiza JavaScript kode.

DETEKCIJA:
- "+"
- req.query / req.body
- exec()

OUTPUT:
list Finding

---

## php_parser.py
NAMEN:
Analiza PHP kode.

DETEKCIJA:
- "."
- $_GET / $_POST
- exec()

OUTPUT:
list Finding

---

# 📁 MODELS

## finding.py
NAMEN:
Predstavlja en najden problem v kodi.

ATRIBUTI:
- line (vrstica)
- type (concat, exec)
- code (del kode)
- variables (user input)
- risk (LOW/HIGH)
- attack_type (SQL/HQL/CMD)

---

## result.py
NAMEN:
Končni rezultat analize.

VSEBINA:
- findings
- score
- risk level

---

## enums.py
NAMEN:
Standardizacija vrednosti.

VSEBINA:
- LOW
- MEDIUM
- HIGH
- CRITICAL

---

# 📁 DETECTORS

## base.py
NAMEN:
Interface za vse detectorje.

FUNKCIJA:
detect(findings)

OUTPUT:
findings z risk informacijami

---

## injection_detector.py
NAMEN:
Glavni security detector.

FUNKCIJA:
- preverja findings proti rules
- določi risk
- določi attack type

INPUT:
findings iz parserja

OUTPUT:
obogateni findings

---

# 📁 RULES

## injection_rules.py
NAMEN:
Definicija vseh attack scenarijev.

SCENARIJI:

1. SQL Injection
- SELECT + concat + user input

2. HQL Injection
- createQuery + concat + input

3. Command Injection
- exec + concat + input

---

# 📁 REPORTING

## report.py
NAMEN:
Formatiranje rezultatov.

INPUT:
findings

OUTPUT:
readable security report

PRIMER OUTPUT:
[HIGH] SQL Injection at line 2

---

# 📁 EXAMPLES

## scenario1_sql.py
Python SQL Injection:
query = "SELECT * FROM users WHERE id='" + user + "'"

---

## scenario2_hql.java
HQL Injection:
createQuery("FROM users WHERE id='" + input + "'")

---

## scenario3_cmd.java
Command Injection:
Runtime.getRuntime().exec(cmd)

---

# 🧠 KAKO SISTEM DELUJE

1. uporabnik vnese kodo
2. parser najde sumljive vzorce
3. detector preveri pravila
4. rules določijo nevarnost
5. report prikaže rezultat

---

# 🧠 LOGIKA SISTEMA

Parser = kaj obstaja v kodi
Rules = kaj je nevarno
Detector = ali je nevarno
Report = rezultat za uporabnika