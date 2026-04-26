from app.cli import parse_args
from pipeline.analyzer import Analyzer
from reporting.report import generate_report


def read_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def main():
    #1. klicem cli.py da dobim argumente iz ukazne vrstice (ime datoteke, jezik, baza podatkov)
    args = parse_args()

    #2.pridobim ime datoteke iz argumentov, in preberem vsebino (kod) datoteke
    code = read_file(args.file)  

    #3. ustvarim instanco Analyzerja, ki bo vodil celoten proces analize
    analyzer = Analyzer() 

    #4.Zaženem analizo s kodo, jezikom in bazo podatkov, ki sem jih dobil iz argumentov iz cli
    result = analyzer.analyze(
        code=code,
        language=args.lang,
        database=args.db
    )

    #pridobim poročilo iz rezultata analize in ga izpišem na konzolo
    report = generate_report(result)
    print(report)


if __name__ == "__main__":
    main()