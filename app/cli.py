import argparse

from app.config import SUPPORTED_LANGUAGES, SUPPORTED_DATABASES

"""
    'argparse' je Python knjižnica za branje argumentov iz terminala.
    Parsa argumente ukazne vrstice za zagon analize.

    Input (CLI parametri):
        --file (str): Pot do datoteke z izvorno kodo.
        --lang (str): Programski jezik (podpira: {SUPPORTED_LANGUAGES}).
        --db   (str): Tip baze podatkov (privzeto: 'mysql').

    Output:
        argparse.Namespace: Objekt, ki vsebuje atribute .file, .lang in .db.
"""



def parse_args():
    parser = argparse.ArgumentParser(
        description="Static analyzer for SQL, HQL and Command Injection."
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Path to the source code file."
    )

    parser.add_argument(
        "--lang",
        required=True,
        choices=SUPPORTED_LANGUAGES,
        help="Programming language of the source code."
    )

    parser.add_argument(
        "--db",
        required=False,
        default="mysql",
        choices=SUPPORTED_DATABASES,
        help="Database type."
    )

    return parser.parse_args()