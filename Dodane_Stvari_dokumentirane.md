zveden je bil refactoring parserjev


Dodana je bila datoteka languages/base_parser.py.


Parserji so bili premaknjeni oziroma preusmerjeni v strukturo languages/.


Analyzer zdaj uporablja parserje iz:


languages/python/parser.py


languages/php/parser.py


languages/javascript/parser.py






Urejena je bila nova arhitektura za jezike


Ciljna struktura je zdaj:
languages/├── base_parser.py├── base_taint_tracker.py├── python/│   ├── parser.py│   └── taint_tracker.py├── php/│   ├── parser.py│   └── taint_tracker.py└── javascript/    ├── parser.py    └── taint_tracker.py




Urejeni so bili importi parserjev


Namesto starega importa:
from parsers.base import BaseParser


se zdaj uporablja:
from languages.base_parser import BaseParser




Urejeni so bili taint trackerji


Taint trackerji so zdaj ločeni po jezikih:


PythonTaintTracker


PHPTaintTracker


JavaScriptTaintTracker




V detectors/injection_detector.py se ustrezen taint tracker izbere glede na jezik kode.




Poenoteno je bilo poimenovanje Python trackerja


Python tracker je bil preimenovan iz splošnega TaintTracker v:
PythonTaintTracker


S tem so imena trackerjev konsistentna.




Testirano je bilo, da refactoring ni pokvaril obstoječih scenarijev


Python test z vsemi tremi osnovnimi scenariji še vedno vrne:


SQL Injection


HQL Injection


Command Injection




Rezultat:
Total findings: 3Overall risk: CRITICALScore: 100/100




Testiran je bil Python taint chain


Primer:
user_id = request.GET["id"]copied_id = user_idquery = "SELECT * FROM users WHERE id='" + copied_id + "'"


Analizator pravilno zazna SQL Injection.


To pomeni, da taint tracking pravilno sledi vmesnim spremenljivkam.




Testiran je bil varen Python primer


Primer statične SQL poizvedbe:
query = "SELECT * FROM users WHERE active=1"


Rezultat:
Total findings: 0Overall risk: SAFEScore: 0/100


To pomeni, da refactoring ni povzročil false positive rezultatov.




Testiran je bil PHP SQL primer


PHP SQL Injection primer še vedno deluje.


Analizator pravilno zazna:
Scenario #1: SQL Injection




Dodana je bila podpora za MongoDB Injection


Projekt zdaj podpira nov scenarij:
Scenario #4: MongoDB Injection




V rules/injection_rules.py so bila dodana MongoDB pravila


Dodani so bili vzorci za MongoDB operacije:


.find(


.find_one(


.findOne(


.aggregate(


.update_one(


.updateOne(


->find(


->findOne(




Dodani so bili vzorci za MongoDB operatorje:


$ne


$gt


$gte


$lt


$lte


$regex


$where


$or


$and


$in


$nin


$exists






V detectors/pattern_utils.py sta bili dodani novi funkciji


Funkcija za zaznavo MongoDB operacij:
contains_mongodb_operation(line, language)


Funkcija za zaznavo MongoDB operatorjev:
contains_mongodb_operator(line)




Dodan je bil nov detector


Ustvarjena je bila datoteka:
detectors/mongodb_detector.py


V njej je razred:
MongoDBDetector




MongoDBDetector zazna ranljivost, kadar vrstica vsebuje


MongoDB operacijo


in direct user input ali tainted variable




MongoDBDetector ima tudi poseben opis za MongoDB operatorje


Če so operatorji, kot je $ne, v isti vrstici kot MongoDB operacija, se izpiše:
MongoDB query uses untrusted input with MongoDB operators.




V models/enums.py je bil dodan nov AttackType
MONGODB_INJECTION = "MongoDB Injection"


V models/enums.py je bil dodan nov FindingType
MONGODB_INJECTION = "MongoDB Injection"


MongoDBDetector je bil priklopljen v detectors/injection_detector.py


Dodan je bil import:
from detectors.mongodb_detector import MongoDBDetector


Dodana je bila inicializacija:
self.mongodb_detector = MongoDBDetector()




Vrstni red detekcije je zdaj


HQL Injection


MongoDB Injection


SQL Injection


Command Injection




V pipeline/analyzer.py je bil dodan četrti scenarij
Scenario #4: MongoDB Injection


Scoring zdaj podpira tudi štiri scenarije


0 scenarijev → SAFE, score 0


1 scenarij → HIGH, score 50


2 scenarija → HIGH, score 75


3 ali več scenarijev → CRITICAL, score 100




Testiran je bil Python MongoDB multiline primer


Primer:
username = request.args["username"]filter_query = {"username": username}return users.find_one(filter_query)


Rezultat:
Scenario #4: MongoDB Injection




Testiran je bil PHP MongoDB multiline primer


Primer:
$username = $_GET["username"];$filter = ["username" => $username];return $collection->findOne($filter);


Rezultat:
Scenario #4: MongoDB Injection




Testiran je bil Python test z vsemi štirimi scenariji


Rezultat:
Total findings: 4Overall risk: CRITICALScore: 100/100


Zaznani scenariji:


Scenario #1: SQL Injection


Scenario #2: HQL Injection


Scenario #3: Command Injection


Scenario #4: MongoDB Injection






Testiran je bil varen MongoDB primer


Primer:
filter_query = {"active": True}return users.find_one(filter_query)


Rezultat:
Total findings: 0Overall risk: SAFEScore: 0/100




Testiran je bil direct MongoDB operator primer


Primer:
return users.find_one({"username": {"$ne": username}})


Analizator pravilno vrne poseben opis:
MongoDB query uses untrusted input with MongoDB operators.




Trenutna omejitev


MongoDB operator-specific opis deluje samo, če je operator v isti vrstici kot MongoDB operacija.


Primer, ki deluje s posebnim opisom:
return users.find_one({"username": {"$ne": username}})


Primer, kjer se MongoDB Injection zazna, ampak opis ostane splošen:
filter_query = {"username": {"$ne": username}}return users.find_one(filter_query)




Kaj bi bilo treba dodati pozneje za multiline MongoDB operator tracking


Dodati ločeno sledenje spremenljivkam, ki vsebujejo MongoDB operatorje.


Ne mešati tega z obstoječim tainted_variables.


Dodati nov tracking, na primer:
mongodb_operator_variables




Za prihodnjo nadgradnjo bi bilo treba spremeniti


languages/base_taint_tracker.py


detectors/injection_detector.py


detectors/mongodb_detector.py




Prihodnja logika bi morala slediti temu


Če vrstica vsebuje:
filter_query = {"username": {"$ne": username}}
potem se filter_query označi kot spremenljivka, ki vsebuje MongoDB operator.


Če se pozneje uporabi:
return users.find_one(filter_query)
potem se uporabi poseben opis za MongoDB operatorje.




Trenutno stanje projekta


Python podpira:


SQL Injection


HQL Injection


Command Injection


MongoDB Injection




PHP podpira:


SQL Injection


MongoDB Injection




JavaScript ima pripravljena pravila in detectorje, multiline delovanje pa je odvisno od prihodnje implementacije JavaScriptTaintTracker.







