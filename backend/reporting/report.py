def generate_report(result):
    """
    Pretvori AnalysisResult v berljiv tekstovni report.
    """

    lines = []

    lines.append("=== SECURITY REPORT ===")
    lines.append("")
    lines.append(f"Total findings: {result.total_findings}")
    lines.append(f"Overall risk: {result.overall_risk.value}")
    lines.append(f"Score: {result.score}/100")
    lines.append("")

    lines.append("Detected scenarios:")

    if result.detected_scenarios:
        for scenario in result.detected_scenarios:
            lines.append(f"- {scenario}")
    else:
        lines.append("- None")

    lines.append("")

    if not result.findings:
        lines.append("No obvious injection vulnerabilities were found.")
        return "\n".join(lines)

    for finding in result.findings:
        lines.append(f"[{finding.risk.value}] {finding.attack_type.value}")
        lines.append(f"Line: {finding.line}")
        lines.append(f"Language: {finding.language}")
        lines.append(f"Code: {finding.code}")
        lines.append(f"Description: {finding.description}")
        lines.append(f"Recommendation: {finding.recommendation}")
        lines.append("")

    return "\n".join(lines)