from dataclasses import dataclass, field
from typing import List
from models.finding import Finding
from models.enums import RiskLevel


@dataclass
class AnalysisResult:
    """
    Predstavlja končni rezultat analize.
        Ta objekt bo vseboval 
        findings - seznam vseh najdenih ranljivosti (Finding objektov), 
        total_findings - skupno število najdenih ranljivosti, 
        overall_risk oceno tveganja in 
        skuoni score
        
        lahko dodamo tudi - priporočila za izboljšanje varnosti kode.
    """

    findings: List[Finding] = field(default_factory=list)
    total_findings: int = 0
    overall_risk: RiskLevel = RiskLevel.LOW
    score: int = 0
    detected_scenarios: list = field(default_factory=list)


    