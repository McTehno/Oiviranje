from detectors.pattern_utils import (
    contains_user_input,
    contains_tainted_variable,
    contains_mongodb_operation,
    contains_mongodb_operator
)

from models.finding import Finding
from models.enums import RiskLevel, AttackType, FindingType


class MongoDBDetector:
    def detect_line(self, code_line, tainted_variables, operator_variables):
        line = code_line.content
        language = code_line.language

        has_mongodb_operation = contains_mongodb_operation(line, language)
        has_user_input = contains_user_input(line, language)
        has_tainted_variable = contains_tainted_variable(line, tainted_variables)
        
        # Preverimo, če se MongoDB operatorji pojavljajo direktno v vrstici, 
        # ali če uporabljamo spremenljivko, ki vsebuje MongoDB operatorje
        has_direct_mongodb_operator = contains_mongodb_operator(line)
        has_operator_variable = contains_tainted_variable(line, operator_variables)
        uses_mongodb_operator = has_direct_mongodb_operator or has_operator_variable

        if not has_mongodb_operation:
            return None

        if not has_user_input and not has_tainted_variable:
            return None

        description = "MongoDB query is constructed using untrusted user input."
        recommendation = "Validate input and build MongoDB filters using allowed fields and safe operators only."

        if uses_mongodb_operator:
            description = "MongoDB query uses untrusted input with MongoDB operators."
            recommendation = "Do not allow user-controlled MongoDB operators such as $ne, $where, $regex, or $or."

        return Finding(
            line=code_line.number,
            type=FindingType.MONGODB_INJECTION,
            code=line,
            language=language,
            risk=RiskLevel.HIGH,
            attack_type=AttackType.MONGODB_INJECTION,
            description=description,
            recommendation=recommendation
        )