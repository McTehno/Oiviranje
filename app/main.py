from pipeline.analyzer import Analyzer
from app.cli import parse_args

"""
ENTRY POINT PROGRAMA

Input:
    CLI argumenti + datoteka kode

Output:
    print rezultat analize
"""

if __name__ == "__main__":
    args = parse_args()

    with open(args.file, "r") as f:
        code = f.read()

    analyzer = Analyzer()
    result = analyzer.run(code, args.lang)

    print(result)