#zagon: python -m app.main --file examples/scenario3_cmd.py --lang python --db mysql--db mysql

def lookup(request, os):
    os.system("nslookup " + request.GET["domain"])