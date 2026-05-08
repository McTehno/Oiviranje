import React, { useMemo, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Activity, BarChart3, ChevronDown, ChevronUp, PieChart as PieChartIcon } from 'lucide-react';
import type { FileData, Finding, Severity } from '../types/analysis';

interface DashboardProps {
  selectedFile: FileData;
  findings: Finding[];
}

const severityPalette: Record<Severity, string> = {
  CRITICAL: '#EF4444',
  HIGH: '#F97316',
  MEDIUM: '#FACC15',
  LOW: '#22C55E',
  SAFE: '#22C55E',
  UNKNOWN: '#9CA3AF',
};

const severityOrder: Severity[] = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'SAFE', 'UNKNOWN'];

const toSeverity = (value: string): Severity => {
  return (severityOrder.includes(value as Severity) ? value : 'UNKNOWN') as Severity;
};

export const Dashboard: React.FC<DashboardProps> = ({ selectedFile, findings }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const vulnerabilitiesByType = useMemo(() => {
    const counts = findings.reduce<Record<string, number>>((accumulator, finding) => {
      accumulator[finding.attack_type] = (accumulator[finding.attack_type] ?? 0) + 1;
      return accumulator;
    }, {});

    return Object.entries(counts)
      .map(([name, count]) => ({ name, count }))
      .sort((left, right) => right.count - left.count || left.name.localeCompare(right.name));
  }, [findings]);

  const severityBreakdown = useMemo(() => {
    const counts = findings.reduce<Record<Severity, number>>(
      (accumulator, finding) => {
        accumulator[finding.risk] += 1;
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
        name: toSeverity(name),
        value,
        color: severityPalette[toSeverity(name)],
      }))
      .filter((entry) => entry.value > 0)
      .sort((left, right) => severityOrder.indexOf(left.name) - severityOrder.indexOf(right.name));
  }, [findings]);

  return (
    <div className="border-t border-gray-200 bg-white shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-10">
      <div
        className="flex h-10 cursor-pointer items-center justify-between border-b border-gray-100 bg-gray-50 px-4 hover:bg-gray-100"
        onClick={() => setIsExpanded((current) => !current)}
      >
        <div className="flex items-center text-sm font-semibold uppercase tracking-wide text-gray-700">
          <Activity size={16} className="mr-2 text-indigo-500" />
          File Security Analytics
          <span className="ml-3 text-xs font-normal normal-case text-gray-500">
            {selectedFile.path} · {findings.length} finding{findings.length === 1 ? '' : 's'}
          </span>
        </div>

        <div className="text-gray-400">{isExpanded ? <ChevronDown size={18} /> : <ChevronUp size={18} />}</div>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: 320 }}
            exit={{ height: 0 }}
            className="overflow-hidden"
          >
            <div className="grid h-full grid-cols-1 gap-4 p-4 xl:grid-cols-2">
              <section className="flex min-h-0 flex-col rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
                <div className="mb-3 flex items-center gap-2">
                  <div className="rounded-xl bg-indigo-50 p-2 text-indigo-600">
                    <BarChart3 size={18} />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-gray-800">Vulnerabilities by Type</h3>
                    <p className="text-xs text-gray-500">Counts for the open file only.</p>
                  </div>
                </div>

                <div className="min-h-0 flex-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={vulnerabilitiesByType} margin={{ top: 10, right: 10, left: -12, bottom: 16 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                      <XAxis
                        dataKey="name"
                        tick={{ fontSize: 11 }}
                        tickLine={false}
                        axisLine={false}
                        interval={0}
                        angle={-25}
                        textAnchor="end"
                      />
                      <YAxis tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
                      <Tooltip
                        cursor={{ fill: '#F9FAFB' }}
                        contentStyle={{
                          borderRadius: '12px',
                          border: 'none',
                          boxShadow: '0 12px 24px -12px rgba(15, 23, 42, 0.25)',
                        }}
                      />
                      <Bar dataKey="count" fill="#6366F1" radius={[6, 6, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </section>

              <section className="flex min-h-0 flex-col rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
                <div className="mb-3 flex items-center gap-2">
                  <div className="rounded-xl bg-rose-50 p-2 text-rose-600">
                    <PieChartIcon size={18} />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-gray-800">Severity Breakdown</h3>
                    <p className="text-xs text-gray-500">Severity distribution for the open file.</p>
                  </div>
                </div>

                <div className="min-h-0 flex-1">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={severityBreakdown} innerRadius={48} outerRadius={78} paddingAngle={4} dataKey="value">
                        {severityBreakdown.map((entry) => (
                          <Cell key={entry.name} fill={entry.color} />
                        ))}
                      </Pie>

                      <Tooltip
                        contentStyle={{
                          borderRadius: '12px',
                          border: 'none',
                          boxShadow: '0 12px 24px -12px rgba(15, 23, 42, 0.25)',
                        }}
                      />

                      <Legend
                        verticalAlign="middle"
                        align="right"
                        layout="vertical"
                        iconType="circle"
                        wrapperStyle={{ fontSize: '12px' }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </section>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
