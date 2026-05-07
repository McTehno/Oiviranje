# Testni primer za Command Injection detektor
# Multiline primer: user input se najprej shrani v spremenljivko
#python -m app.main --file examples/scenario3_cmd_multiline.py --lang python --db mysql
def lookup(request, os):
    domain = request.GET["domain"]
    cmd = "nslookup " + domain
    os.system(cmd)