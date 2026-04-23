from detectors.base import BaseDetector
from rules.injection_rules import RULES

class InjectionDetector(BaseDetector):
    """
    DETEKTOR ZA SQL / HQL / COMMAND INJECTION

    Input:
        findings iz parserja

    Output:
        findings z:
        - risk (LOW/HIGH/CRITICAL)
        - attack_type
    """

    def detect(self, findings):

        for f in findings:

            for rule in RULES:

                # preveri keyword match
                if any(k in f.code for k in rule["keywords"]):

                    # preveri concat + user input
                    if f.type == "concat" and f.variables:

                        f.risk = rule["risk"]
                        f.attack_type = rule["name"]

        return findings