from enum import Enum
#Tukaj hranimo standardne vrednosti, 
# da ne pišemo ročno "HIGH", "SQL Injection" itd.

class RiskLevel(Enum):
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AttackType(Enum):
    NONE = "None"
    SQL_INJECTION = "SQL Injection"
    HQL_INJECTION = "HQL Injection"
    COMMAND_INJECTION = "Command Injection"
    MONGODB_INJECTION = "MongoDB Injection"


class FindingType(Enum):
    UNKNOWN = "Unknown"
    CONCAT = "String Concatenation"
    EXEC = "Command Execution"
    RAW_QUERY = "Raw Query"
    MONGODB_INJECTION = "MongoDB Injection"