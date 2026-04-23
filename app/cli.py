import argparse

def parse_args():
    """
    Namen:
        Sprejme argumente iz terminala (CLI)

    Input:
        --file (pot do kode)
        --lang (programski jezik)

    Output:
        namespace objekt z argumenti

    Primer:
        python main.py --file test.py --lang python
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--file", required=True)  # pot do kode
    parser.add_argument("--lang", required=True)  # jezik

    return parser.parse_args()