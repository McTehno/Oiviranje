import type { Finding, Severity } from '../types/analysis';

export const severityColors: Record<Severity, string> = {
  CRITICAL: '#EF4444',
  HIGH: '#F97316',
  MEDIUM: '#FACC15',
  LOW: '#22C55E',
  SAFE: '#22C55E',
  UNKNOWN: '#9CA3AF',
};

export const vulnerabilityTypeColors = [
  '#4F46E5',
  '#14B8A6',
  '#8B5CF6',
  '#EC4899',
  '#06B6D4',
  '#F59E0B',
  '#10B981',
  '#EF4444',
];

const severityRank: Record<Severity, number> = {
  CRITICAL: 5,
  HIGH: 4,
  MEDIUM: 3,
  LOW: 2,
  SAFE: 1,
  UNKNOWN: 0,
};

export interface VulnerabilityTypePoint {
  name: string;
  count: number;
}

export interface SeverityBreakdownPoint {
  name: Severity;
  value: number;
}


export const normalizeSeverity = (value: string): Severity => {
  if (
    value === 'CRITICAL' ||
    value === 'HIGH' ||
    value === 'MEDIUM' ||
    value === 'LOW' ||
    value === 'SAFE' ||
    value === 'UNKNOWN'
  ) {
    return value;
  }

  return 'UNKNOWN';
};

export const summarizeFindingsByAttackType = (
  findings: Finding[]
): VulnerabilityTypePoint[] => {
  const counts = findings.reduce<Record<string, number>>((accumulator, finding) => {
    accumulator[finding.attack_type] = (accumulator[finding.attack_type] ?? 0) + 1;
    return accumulator;
  }, {});

  return Object.entries(counts)
    .map(([name, count]) => ({
      name,
      count,
    }))
    .sort((left, right) => right.count - left.count || left.name.localeCompare(right.name));
};

export const summarizeFindingsBySeverity = (
  findings: Finding[]
): SeverityBreakdownPoint[] => {
  const counts = findings.reduce<Record<Severity, number>>(
    (accumulator, finding) => {
      const severity = normalizeSeverity(finding.risk);
      accumulator[severity] += 1;
      return accumulator;
    },
    {
      CRITICAL: 0,
      HIGH: 0,
      MEDIUM: 0,
      LOW: 0,
      SAFE: 0,
      UNKNOWN: 0,
    }
  );

  return Object.entries(counts)
    .map(([name, value]) => ({
      name: normalizeSeverity(name),
      value,
    }))
    .filter((entry) => entry.value > 0)
    .sort(
      (left, right) => severityRank[right.name] - severityRank[left.name]
    );
};


