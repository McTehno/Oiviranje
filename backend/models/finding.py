from dataclasses import dataclass, field
from models.enums import RiskLevel, AttackType, FindingType


@dataclass
class Finding:
    """
    Predstavlja eno najdeno ranljivost v kodi.
    Sprememba v logiki ki sem jo naredila je da
        Finding ustvari detector, ne parser.
    """

    line: int
    type: FindingType
    code: str
    variables: list = field(default_factory=list)
    language: str = "unknown"

    #dodala sem te atribute da lahko razlikujemo odgovore
    file_path: str = ""
    database: str = "unknown"

    risk: RiskLevel = RiskLevel.LOW
    attack_type: AttackType = AttackType.NONE

    description: str = ""
    recommendation: str = ""