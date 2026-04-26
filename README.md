# SQL Injection Analyzer

SQL Injection Analyzer je orodje za osnovno statično analizo kode.  
Namen orodja je zaznati tri vrste injection ranljivosti:

1. SQL Injection
2. HQL / ORM Injection
3. Command Injection

Trenutna stabilna verzija je fokusirana predvsem na Python kodo.  
Projekt podpira osnovno zaznavo ranljivosti v isti vrstici in zaznavo prek vmesnih spremenljivk z uporabo taint tracking logike.

---

## Cilj projekta

Cilj projekta je analizirati izvorno kodo in ugotoviti, ali vsebuje nevarne vzorce, kjer uporabniški input pride v stik z nevarnimi operacijami.

Primer nevarnega SQL Injection vzorca:

```python
user_id = request.GET["id"]
query = "SELECT * FROM users WHERE id='" + user_id + "'"

```
Primer nevarnega HQL / ORM Injection vzorca:
```python
user_id = request.GET["id"]
query = "FROM accounts WHERE custID='" + user_id + "'"
session.createQuery(query)

```
Primer nevarnega Command Injection vzorca:
```python
domain = request.GET["domain"]
cmd = "nslookup " + domain
os.system(cmd)
```

## Trenutna struktura projekta
Oiviranje/
│
├── app/
│   ├── main.py
│   ├── cli.py
│   └── config.py
│
├── analysis/
│   └── taint_tracker.py
│
├── detectors/
│   ├── base.py
│   ├── pattern_utils.py
│   ├── sql_detector.py
│   ├── hql_detector.py
│   ├── command_detector.py
│   └── injection_detector.py
│
├── models/
│   ├── code_line.py
│   ├── finding.py
│   ├── result.py
│   └── enums.py
│
├── parsers/
│   ├── base.py
│   ├── python_parser.py
│   ├── js_parser.py
│   └── php_parser.py
│
├── pipeline/
│   └── analyzer.py
│
├── reporting/
│   └── report.py
│
├── rules/
│   └── injection_rules.py
│
├── examples/
│   └── python/
│       ├── scenario1_sql.py
│       ├── scenario1_sql_multiline.py
│       ├── scenario2_hql.py
│       ├── scenario2_hql_multiline.py
│       ├── scenario3_cmd.py
│       ├── scenario3_cmd_multiline.py
│       ├── all_scenarios_python.py
│       └── velika.py
│
├── README.md
└── requirements.txt




# Glavni tok aplikacije
User input / source code
        ↓
app/main.py
        ↓
pipeline/analyzer.py
        ↓
Parser
        ↓
CodeLine objects
        ↓
TaintTracker
        ↓
InjectionDetector
        ↓
SQLDetector / HQLDetector / CommandDetector
        ↓
Finding objects
        ↓
AnalysisResult
        ↓
Report



## Opis glavnih map

### app/

Mapa app vsebuje vstopne datoteke aplikacije.

#### main.py

Glavna vstopna točka programa.
Prebere argumente, odpre datoteko, zažene analizator in izpiše rezultat.

#### cli.py

Definira argumente za zagon iz terminala.

Podprti argumenti:

--file   pot do datoteke
--lang   programski jezik
--db     podatkovna baza

Primer:

python -m app.main --file examples/python/all_scenarios_python.py --lang python --db mysql
config.py

Hrani osnovne konfiguracijske vrednosti, na primer podprte jezike in podatkovne baze.

#### models/

Mapa models vsebuje podatkovne strukture, ki jih uporablja celoten projekt.

code_line.py

Definira CodeLine.

CodeLine predstavlja eno vrstico kode.

Primer:

CodeLine(
    number=10,
    content='query = "SELECT * FROM users WHERE id=" + user_id',
    language="python"
)
finding.py

Definira Finding.

Finding predstavlja eno najdeno ranljivost.

Vsebuje podatke, kot so:

line
type
code
language
risk
attack_type
description
recommendation
result.py

Definira AnalysisResult.

AnalysisResult predstavlja končni rezultat analize.

Vsebuje:

findings
total_findings
overall_risk
score
detected_scenarios
enums.py

Vsebuje standardne vrednosti, kot so:

RiskLevel
AttackType
FindingType
parsers/

Parserji pripravijo kodo za analizo.

Pomembno: parserji ne zaznavajo ranljivosti.
Njihova naloga je, da izvorno kodo razdelijo po vrsticah in ustvarijo CodeLine objekte.

python_parser.py

Parser za Python kodo.

js_parser.py

Osnovni parser za JavaScript kodo.

php_parser.py

Osnovni parser za PHP kodo.

base.py

Osnovni interface za parserje.

rules/

Mapa rules vsebuje pravila oziroma vzorce, ki jih uporabljajo detectorji.

injection_rules.py

Vsebuje vzorce za:

SQL keywords
user input patterns
string concatenation patterns
ORM/HQL patterns
command execution patterns

Primeri user input vzorcev:

request.GET
request.POST
request.args
request.form
input()
req.query
$_GET
analysis/

Mapa analysis vsebuje podporno analizo podatkovnega toka.

taint_tracker.py

TaintTracker sledi spremenljivkam, ki vsebujejo uporabniški input.

Primer:

user_id = request.GET["id"]
query = "SELECT * FROM users WHERE id='" + user_id + "'"

TaintTracker ugotovi:

user_id je tainted
query je tainted

To omogoča zaznavanje ranljivosti, ki niso zapisane samo v eni vrstici.

Taint tracking trenutno deluje na nivoju funkcije.
Ko se začne nova funkcija, se seznam tainted spremenljivk resetira.

To zmanjša false positive rezultate pri večjih datotekah.

detectors/

Detectorji so odgovorni za zaznavanje ranljivosti.

sql_detector.py

Zazna SQL Injection.

Pravilo:

Če vrstica vsebuje SQL keyword + user input ali tainted variable + concatenation,
potem je SQL Injection.

Primer:

user_id = request.GET["id"]
query = "SELECT * FROM users WHERE id='" + user_id + "'"
hql_detector.py

Zazna HQL / ORM Injection.

Pravilo:

Če vrstica vsebuje ORM/HQL pattern + user input ali tainted variable,
potem je HQL / ORM Injection.

Primer:

query = "FROM accounts WHERE custID='" + user_id + "'"
session.createQuery(query)
command_detector.py

Zazna Command Injection.

Pravilo:

Če vrstica vsebuje command execution function + user input ali tainted variable,
potem je Command Injection.

Primer:

domain = request.GET["domain"]
cmd = "nslookup " + domain
os.system(cmd)
injection_detector.py

Glavni koordinator detectorjev.

Njegova naloga je:

1. zagnati TaintTracker
2. za vsako vrstico pridobiti tainted variables
3. zagnati HQLDetector
4. zagnati SQLDetector
5. zagnati CommandDetector
6. vrniti vse Finding objekte

HQL detector se izvede pred SQL detectorjem, ker HQL izrazi pogosto vsebujejo besede FROM in WHERE, ki so podobne SQL stavkom.

pattern_utils.py

Vsebuje skupne pomožne funkcije za regex preverjanje, na primer:

contains_user_input
contains_concatenation
contains_orm_pattern
contains_command_execution
contains_tainted_variable
pipeline/
analyzer.py

Glavni orchestrator analize.

Naloge:

1. izbere parser glede na jezik
2. zažene parser
3. zažene InjectionDetector
4. izračuna najdene scenarije
5. izračuna overall risk
6. izračuna score
7. vrne AnalysisResult
reporting/
report.py

Pretvori AnalysisResult v berljiv tekstovni report.

Primer izpisa:

=== SECURITY REPORT ===

Total findings: 3
Overall risk: CRITICAL
Score: 100/100

Detected scenarios:
- Scenario #1: SQL Injection
- Scenario #2: HQL Injection
- Scenario #3: Command Injection


'''
# Podprti scenariji
Scenario #1: SQL Injection

Direktni primer:

query = "SELECT * FROM users WHERE id='" + request.GET["id"] + "'"

Multiline primer:

user_id = request.GET["id"]
query = "SELECT * FROM users WHERE id='" + user_id + "'"
Scenario #2: HQL / ORM Injection

Direktni primer:

session.createQuery("FROM accounts WHERE custID='" + request.GET["id"] + "'")

Multiline primer:

user_id = request.GET["id"]
query = "FROM accounts WHERE custID='" + user_id + "'"
session.createQuery(query)
Scenario #3: Command Injection

Direktni primer:

os.system("nslookup " + request.GET["domain"])

Multiline primer:

domain = request.GET["domain"]
cmd = "nslookup " + domain
os.system(cmd)
Ocena tveganja

Skupna ocena se izračuna glede na število najdenih scenarijev.

0 scenarijev → SAFE, score 0
1 scenarij   → HIGH, score 50
2 scenarija  → HIGH, score 75
3 scenariji  → CRITICAL, score 100

Primer:

Če so najdeni vsi trije scenariji:

Overall risk: CRITICAL
Score: 100/100


# Kako zagnati projekt

V terminalu se postavi v glavno mapo projekta:

cd C:\oiv_projektna_naloga\Oiviranje

Zaženi primer z vsemi tremi scenariji:

python -m app.main --file examples/python/all_scenarios_python.py --lang python --db mysql

Pričakovan rezultat:

Total findings: 3
Overall risk: CRITICAL
Score: 100/100

Detected scenarios:
- Scenario #1: SQL Injection
- Scenario #2: HQL Injection
- Scenario #3: Command Injection
Testni primeri
SQL Injection
python -m app.main --file examples/python/scenario1_sql.py --lang python --db mysql
python -m app.main --file examples/python/scenario1_sql_multiline.py --lang python --db mysql
HQL / ORM Injection
python -m app.main --file examples/python/scenario2_hql.py --lang python --db mysql
python -m app.main --file examples/python/scenario2_hql_multiline.py --lang python --db mysql
Command Injection
python -m app.main --file examples/python/scenario3_cmd.py --lang python --db mysql
python -m app.main --file examples/python/scenario3_cmd_multiline.py --lang python --db mysql
Vsi scenariji skupaj
python -m app.main --file examples/python/all_scenarios_python.py --lang python --db mysql
Večja Python datoteka
python -m app.main --file examples/python/velika.py --lang python --db mysql
Trenutne omejitve

Trenutna verzija je osnovni statični analizator.

## Omejitve:

- analiza se izvaja na eni datoteki naenkrat
- Python del je najbolj razvit
- JavaScript in PHP parserja obstajata, vendar nista še enako razvita kot Python
- taint tracking podpira osnovne assignmente oblike variable = value
- ne uporablja AST analize
- ne podpira kompleksnih primerov, kot so self.user_id = ...
- ne sledi podatkom med različnimi funkcijami
- ne preverja vseh možnih user input virov

# Kako prispevati k projektu

Če želi nekdo prispevati k tej verziji projekta, mora najprej razumeti trenutno arhitekturo.

# Pomembno pravilo!!!!

Ne spreminjaj hkrati več velikih delov projekta.


Kaj mora contributor vedeti
1. Parserji ne zaznavajo ranljivosti

Parserji samo pretvorijo kodo v CodeLine objekte.

Ne dodajaj SQL/HQL/Command logike v parserje.

Pravilno:

Parser → CodeLine

Napačno:

Parser → Finding
2. Pravila so v rules/injection_rules.py

Če želiš dodati nov vzorec za user input, concatenation ali command execution, ga dodaj v rules/injection_rules.py.

Primer:

USER_INPUT_PATTERNS = {
    "python": [
        r"request\.GET",
        r"request\.POST"
    ]
}
3. Detectorji ustvarjajo Finding

Če želiš spremeniti zaznavanje SQL Injection, spremeni:

detectors/sql_detector.py

Če želiš spremeniti HQL / ORM Injection:

detectors/hql_detector.py

Če želiš spremeniti Command Injection:

detectors/command_detector.py
4. InjectionDetector samo povezuje detectorje

detectors/injection_detector.py naj ostane koordinator.

Ne dodajaj preveč podrobne SQL ali Command logike v ta file.

5. Taint tracking je v analysis/taint_tracker.py

Če želiš izboljšati sledenje spremenljivkam, spreminjaj:

analysis/taint_tracker.py

Ta del je odgovoren za logiko:

user input → tainted variable → druga tainted variable
6. Report je samo za izpis

reporting/report.py ne sme zaznavati ranljivosti.

Njegova naloga je samo prikaz rezultata.

7. Analyzer povezuje celoten proces

pipeline/analyzer.py povezuje:

parser
detector
result
risk scoring
scenario scoring

Če spreminjaš score ali overall risk, spremeni pipeline/analyzer.py.

Kako preveriti, da sprememba ni pokvarila projekta

Po vsaki večji spremembi zaženi:

python -m app.main --file examples/python/all_scenarios_python.py --lang python --db mysql

Pričakovan rezultat mora ostati:

Total findings: 3
Overall risk: CRITICAL
Score: 100/100

Detected scenarios:
- Scenario #1: SQL Injection
- Scenario #2: HQL Injection
- Scenario #3: Command Injection

Priporočljivo je testirati tudi veliko datoteko:

python -m app.main --file examples/python/velika.py --lang python --db mysql

Pričakovano je, da zazna samo realne ranljivosti, ne vseh statičnih queryjev.

# Kako dodati podporo za JavaScript ali PHP

Trenutno sta JavaScript in PHP parserja osnovna.
Če želiš razširiti podporo za nov jezik, je treba narediti predvsem tri stvari:

1. dodati oziroma izboljšati pravila v rules/injection_rules.py
2. prilagoditi taint tracking za sintakso jezika
3. dodati testne primere v examples/

Za JavaScript bi bilo treba podpreti:

const userId = req.query.id;
const query = "SELECT * FROM users WHERE id='" + userId + "'";

Za PHP bi bilo treba podpreti:

$id = $_GET["id"];
$query = "SELECT * FROM users WHERE id='" . $id . "'";


# Status projekta

Trenutno je Python del stabilen in podpira:

SQL Injection direct + multiline
HQL / ORM Injection direct + multiline
Command Injection direct + multiline
function-level taint tracking
scenario-based risk scoring
tekstovni security report



## Testni primeri

Za preverjanje delovanja analizatorja je ustvarjena posebna mapa `test/`.

Mapa `test/` vsebuje ločene podmape za vsak programski jezik.  
V vsaki podmapi so pripravljeni trije testni primeri, ki predstavljajo tri glavne scenarije projekta:

1. SQL Injection
2. HQL / ORM Injection
3. Command Injection

### Struktura testnih primerov

```text
test/
│
├── python/
│   ├── scenario1_sql.py
│   ├── scenario2_hql.py
│   └── scenario3_cmd.py
│
├── javascript/
│   ├── scenario1_sql.js
│   ├── scenario2_hql.js
│   └── scenario3_cmd.js
│
└── php/
    ├── scenario1_sql.php
    ├── scenario2_hql.php
    └── scenario3_cmd.php


Primer zagona testov
Python
python -m app.main --file test/python/scenario1_sql.py --lang python --db mysql
python -m app.main --file test/python/scenario2_hql.py --lang python --db mysql
python -m app.main --file test/python/scenario3_cmd.py --lang python --db mysql
JavaScript
python -m app.main --file test/javascript/scenario1_sql.js --lang javascript --db mysql
python -m app.main --file test/javascript/scenario2_hql.js --lang javascript --db mysql
python -m app.main --file test/javascript/scenario3_cmd.js --lang javascript --db mysql
PHP
python -m app.main --file test/php/scenario1_sql.php --lang php --db mysql
python -m app.main --file test/php/scenario2_hql.php --lang php --db mysql
python -m app.main --file test/php/scenario3_cmd.php --lang php --db mysql
Pričakovani rezultati

Vsak posamezen testni primer mora vrniti eno glavno zaznano ranljivost.

Primer za SQL Injection:

=== SECURITY REPORT ===

Total findings: 1
Overall risk: HIGH
Score: 50/100

Detected scenarios:
- Scenario #1: SQL Injection

Če bi analizirali datoteko, ki vsebuje vse tri scenarije, bi bil pričakovan rezultat
Total findings: 3
Overall risk: CRITICAL
Score: 100/100

Detected scenarios:
- Scenario #1: SQL Injection
- Scenario #2: HQL Injection
- Scenario #3: Command Injection