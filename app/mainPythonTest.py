import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.analyzer import Analyzer

"""
TEST FILE ZA PYTHON SCENARIO

Namen:
- testiranje Python parserja + detectorja
- brez CLI
"""

code_nepravilna = """
user = input()
query = "SELECT * FROM users WHERE id='" + user + "'"
"""
code_pravilna = """
user = input()
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user,))
"""

code_cdi ="""
import os

domain = input()
cmd = "nslookup " + domain
os.system(cmd)
"""

analyzer = Analyzer()
result = analyzer.run(code_cdi, "python")

print(result)