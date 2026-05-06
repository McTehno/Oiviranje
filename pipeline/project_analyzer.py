import os
from collections import Counter

from app.file_utils import (
    detect_language_from_file,
    is_supported_code_file,
    IGNORED_DIRS,
)
from pipeline.analyzer import Analyzer
from models.enums import RiskLevel


class ProjectAnalyzer:
    def __init__(self):
        self.analyzer = Analyzer()

    def analyze_project(self, project_path: str, database_config: dict):
        all_findings = []
        analyzed_files = []

        for root, dirs, files in os.walk(project_path):
            dirs[:] = [directory for directory in dirs if directory not in IGNORED_DIRS]

            for filename in files:
                file_path = os.path.join(root, filename)

                if not is_supported_code_file(file_path):
                    continue

                relative_path = os.path.relpath(file_path, project_path)
                language = detect_language_from_file(file_path)
                database = self.get_database_for_file(relative_path, database_config)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                        code = file.read()

                    result = self.analyzer.analyze(
                        code=code,
                        language=language,
                        database=database
                    )

                    for finding in result.findings:
                        finding.file_path = relative_path
                        finding.database = database

                    all_findings.extend(result.findings)

                    analyzed_files.append({
                        "id": relative_path,
                        "name": filename,
                        "path": relative_path,
                        "type": "file",
                        "language": language,
                        "database": database,
                        "content": code,
                        "findings_count": len(result.findings),
                        "risk": self.calculate_file_risk(result.findings).value
                    })

                except Exception as error:
                    analyzed_files.append({
                        "id": relative_path,
                        "name": filename,
                        "path": relative_path,
                        "type": "file",
                        "language": language,
                        "database": database,
                        "content": "",
                        "findings_count": 0,
                        "risk": "UNKNOWN",
                        "error": str(error)
                    })

        return self.build_project_result(all_findings, analyzed_files)

    def get_database_for_file(self, file_path: str, database_config: dict):
        mode = database_config.get("mode", "single")
        default_database = database_config.get("default_database", "mysql")

        if mode == "single":
            return default_database

        folder_databases = database_config.get("folder_databases", {})
        best_match = None

        for folder_path in folder_databases:
            normalized_folder = folder_path.strip("/")

            if file_path.startswith(normalized_folder):
                if best_match is None or len(normalized_folder) > len(best_match):
                    best_match = normalized_folder

        if best_match:
            return folder_databases[best_match]

        return default_database

    def calculate_file_risk(self, findings):
        if not findings:
            return RiskLevel.SAFE

        risks = [finding.risk for finding in findings]

        if RiskLevel.CRITICAL in risks:
            return RiskLevel.CRITICAL

        if RiskLevel.HIGH in risks:
            return RiskLevel.HIGH

        if RiskLevel.MEDIUM in risks:
            return RiskLevel.MEDIUM

        if RiskLevel.LOW in risks:
            return RiskLevel.LOW

        return RiskLevel.SAFE

    def calculate_project_risk(self, findings):
        if not findings:
            return RiskLevel.SAFE

        high_count = sum(1 for finding in findings if finding.risk == RiskLevel.HIGH)
        critical_count = sum(1 for finding in findings if finding.risk == RiskLevel.CRITICAL)

        if critical_count > 0 or high_count >= 5:
            return RiskLevel.CRITICAL

        if high_count > 0:
            return RiskLevel.HIGH

        return RiskLevel.MEDIUM

    def calculate_project_score(self, findings):
        if not findings:
            return 0

        score = 0

        for finding in findings:
            if finding.risk == RiskLevel.LOW:
                score += 10
            elif finding.risk == RiskLevel.MEDIUM:
                score += 20
            elif finding.risk == RiskLevel.HIGH:
                score += 35
            elif finding.risk == RiskLevel.CRITICAL:
                score += 50

        return min(score, 100)

    def build_project_result(self, findings, files):
        findings_by_type = Counter(finding.attack_type.value for finding in findings)
        findings_by_risk = Counter(finding.risk.value for finding in findings)
        findings_by_file = Counter(finding.file_path for finding in findings)

        return {
            "project_score": self.calculate_project_score(findings),
            "overall_risk": self.calculate_project_risk(findings).value,
            "total_findings": len(findings),
            "files_analyzed": len(files),
            "summary": {
                "findings_by_type": dict(findings_by_type),
                "findings_by_risk": dict(findings_by_risk),
                "findings_by_file": dict(findings_by_file)
            },
            "files": files,
            "findings": [self.finding_to_dict(finding) for finding in findings],
            "recommendations": self.build_recommendations(findings)
        }

    def finding_to_dict(self, finding):
        return {
            "file_path": finding.file_path,
            "line": finding.line,
            "type": finding.type.value,
            "code": finding.code,
            "variables": finding.variables,
            "language": finding.language,
            "database": finding.database,
            "risk": finding.risk.value,
            "attack_type": finding.attack_type.value,
            "description": finding.description,
            "recommendation": finding.recommendation
        }

    def build_recommendations(self, findings):
        recommendations = []
        attack_types = set(finding.attack_type.value for finding in findings)

        if "SQL Injection" in attack_types:
            recommendations.append("Use parameterized queries or prepared statements for SQL queries.")

        if "HQL Injection" in attack_types:
            recommendations.append("Use safe ORM parameters instead of raw query construction.")

        if "Command Injection" in attack_types:
            recommendations.append("Avoid passing user input directly to operating system commands.")

        if "MongoDB Injection" in attack_types:
            recommendations.append("Validate MongoDB filters and block user-controlled operators such as $ne, $where and $regex.")

        if not recommendations:
            recommendations.append("No obvious injection vulnerabilities were found.")

        return recommendations