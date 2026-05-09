import React from 'react';
import { FileDown } from 'lucide-react';
import jsPDF from 'jspdf';
import type { AnalysisResult, Severity } from '../types/analysis';

interface PdfExportButtonProps {
  result: AnalysisResult;
}

const riskColors: Record<Severity, [number, number, number]> = {
  SAFE: [34, 197, 94],
  LOW: [34, 197, 94],
  MEDIUM: [250, 204, 21],
  HIGH: [249, 115, 22],
  CRITICAL: [239, 68, 68],
  UNKNOWN: [156, 163, 175],
};

const formatDate = () => {
  return new Date().toLocaleString('en-GB', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const addFooter = (doc: jsPDF, pageNumber: number) => {
  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();

  doc.setFontSize(8);
  doc.setTextColor(120, 120, 120);
  doc.text('SAST Analyzer Security Report', 14, pageHeight - 10);
  doc.text(`Page ${pageNumber}`, pageWidth - 28, pageHeight - 10);
};

const addSectionTitle = (doc: jsPDF, title: string, y: number) => {
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(30, 41, 59);
  doc.text(title, 14, y);

  doc.setDrawColor(226, 232, 240);
  doc.line(14, y + 4, 196, y + 4);

  return y + 12;
};

const addMetricCard = (
  doc: jsPDF,
  title: string,
  value: string,
  x: number,
  y: number,
  width: number,
  color: [number, number, number]
) => {
  doc.setFillColor(248, 250, 252);
  doc.setDrawColor(226, 232, 240);
  doc.roundedRect(x, y, width, 28, 4, 4, 'FD');

  doc.setFontSize(8);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(100, 116, 139);
  doc.text(title.toUpperCase(), x + 4, y + 8);

  doc.setFontSize(16);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(color[0], color[1], color[2]);
  doc.text(value, x + 4, y + 21);
};

export const PdfExportButton: React.FC<PdfExportButtonProps> = ({ result }) => {
  const handleExportPdf = () => {
    const doc = new jsPDF('p', 'mm', 'a4');

    const pageWidth = doc.internal.pageSize.getWidth();
    let y = 18;
    let pageNumber = 1;

    const riskColor = riskColors[result.overall_risk] || riskColors.UNKNOWN;

    // Header
    doc.setFillColor(79, 70, 229);
    doc.rect(0, 0, pageWidth, 34, 'F');

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(22);
    doc.setTextColor(255, 255, 255);
    doc.text('SAST Analyzer', 14, 16);

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    doc.text('Static Application Security Testing Report', 14, 24);

    doc.setFontSize(9);
    doc.text(`Generated: ${formatDate()}`, pageWidth - 62, 16);

    y = 48;

    // Executive summary
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(18);
    doc.setTextColor(15, 23, 42);
    doc.text('Executive Summary', 14, y);

    y += 10;

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    doc.setTextColor(71, 85, 105);

    const summaryText =
      result.total_findings === 0
        ? 'No obvious injection vulnerabilities were found in the analyzed project.'
        : `The analyzer found ${result.total_findings} potential security finding(s) across ${result.files_analyzed} analyzed file(s). The overall project risk is ${result.overall_risk}.`;

    const wrappedSummary = doc.splitTextToSize(summaryText, 180);
    doc.text(wrappedSummary, 14, y);
    y += wrappedSummary.length * 5 + 8;

    // Metrics
    addMetricCard(doc, 'Project Score', `${result.project_score}/100`, 14, y, 42, riskColor);
    addMetricCard(doc, 'Overall Risk', result.overall_risk, 61, y, 42, riskColor);
    addMetricCard(doc, 'Findings', String(result.total_findings), 108, y, 42, riskColor);
    addMetricCard(doc, 'Files Analyzed', String(result.files_analyzed), 155, y, 42, [79, 70, 229]);

    y += 42;

    // Findings by type
    y = addSectionTitle(doc, 'Findings by Attack Type', y);

    const typeEntries = Object.entries(result.summary.findings_by_type);

    if (typeEntries.length === 0) {
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(10);
      doc.setTextColor(71, 85, 105);
      doc.text('No attack types detected.', 14, y);
      y += 10;
    } else {
      typeEntries.forEach(([type, count]) => {
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(10);
        doc.setTextColor(30, 41, 59);
        doc.text(`- ${type}: ${count}`, 18, y);
        y += 7;
      });
    }

    y += 6;

    // Findings by risk
    y = addSectionTitle(doc, 'Findings by Risk Level', y);

    const riskEntries = Object.entries(result.summary.findings_by_risk);

    if (riskEntries.length === 0) {
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(10);
      doc.setTextColor(71, 85, 105);
      doc.text('No risk levels detected.', 14, y);
      y += 10;
    } else {
      riskEntries.forEach(([risk, count]) => {
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(10);
        doc.setTextColor(30, 41, 59);
        doc.text(`- ${risk}: ${count}`, 18, y);
        y += 7;
      });
    }

    y += 6;

    // Recommendations
    y = addSectionTitle(doc, 'Recommendations', y);

    result.recommendations.forEach((recommendation, index) => {
      const text = `${index + 1}. ${recommendation}`;
      const wrapped = doc.splitTextToSize(text, 175);

      if (y + wrapped.length * 5 > 275) {
        addFooter(doc, pageNumber);
        doc.addPage();
        pageNumber += 1;
        y = 20;
      }

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(10);
      doc.setTextColor(30, 41, 59);
      doc.text(wrapped, 18, y);
      y += wrapped.length * 5 + 4;
    });

    y += 4;

    // Detailed findings
    if (result.findings.length > 0) {
      if (y > 230) {
        addFooter(doc, pageNumber);
        doc.addPage();
        pageNumber += 1;
        y = 20;
      }

      y = addSectionTitle(doc, 'Detailed Findings', y);

      result.findings.forEach((finding, index) => {
        if (y > 245) {
          addFooter(doc, pageNumber);
          doc.addPage();
          pageNumber += 1;
          y = 20;
        }

        const findingColor = riskColors[finding.risk] || riskColors.UNKNOWN;

        doc.setFillColor(255, 255, 255);
        doc.setDrawColor(226, 232, 240);
        doc.roundedRect(14, y, 182, 38, 3, 3, 'D');

        doc.setFont('helvetica', 'bold');
        doc.setFontSize(10);
        doc.setTextColor(findingColor[0], findingColor[1], findingColor[2]);
        doc.text(`${index + 1}. ${finding.attack_type} - ${finding.risk}`, 18, y + 7);

        doc.setFont('helvetica', 'normal');
        doc.setFontSize(8);
        doc.setTextColor(100, 116, 139);
        doc.text(`${finding.file_path} · Line ${finding.line} · ${finding.language} · ${finding.database}`, 18, y + 13);

        doc.setFontSize(8);
        doc.setTextColor(30, 41, 59);

        const code = doc.splitTextToSize(`Code: ${finding.code}`, 170);
        doc.text(code.slice(0, 2), 18, y + 20);

        const recommendation = doc.splitTextToSize(`Recommendation: ${finding.recommendation}`, 170);
        doc.text(recommendation.slice(0, 2), 18, y + 30);

        y += 44;
      });
    }

    addFooter(doc, pageNumber);

    doc.save(`sast-security-report-${Date.now()}.pdf`);
  };

  return (
    <button
      type="button"
      onClick={handleExportPdf}
      className="inline-flex items-center rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700 transition-colors hover:bg-emerald-100 hover:text-emerald-800"
    >
      <FileDown size={14} className="mr-1.5" />
      Export PDF
    </button>
  );
};