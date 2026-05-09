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
import {
  Activity,
  BarChart3,
  ChevronDown,
  ChevronUp,
  PieChart as PieChartIcon,
  ShieldCheck,
} from 'lucide-react';
import type { FileData, Finding } from '../types/analysis';
import {
  severityColors,
  summarizeFindingsByAttackType,
  summarizeFindingsBySeverity,
  vulnerabilityTypeColors,
} from '../utils/severity';

interface DashboardProps {
  selectedFile: FileData;
  findings: Finding[];
}

export const Dashboard: React.FC<DashboardProps> = ({ selectedFile, findings }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  // `vulnerabilitiesByType` vzame vse findinge iz odprte datoteke,
  // jih zdruzi po `attack_type` in pripravi podatke za vodoravni bar chart.
  // UI ga uporablja za prikaz napadalnih vzorcev kot jasen seznam od zgoraj navzdol.
  const vulnerabilitiesByType = useMemo(
    () => summarizeFindingsByAttackType(findings),
    [findings]
  );

  // `severityBreakdown` iz seznama findingov izracuna razporeditev po severity nivojih.
  // Ta podatek napaja pie chart in prikazuje samo rezultate za trenutno odprto datoteko.
  const severityBreakdown = useMemo(
    () => summarizeFindingsBySeverity(findings),
    [findings]
  );

  return (
    <div className="z-10 border-t border-gray-200 bg-white shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
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

        <div className="text-gray-400">
          {isExpanded ? <ChevronDown size={18} /> : <ChevronUp size={18} />}
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: 320 }}
            exit={{ height: 0 }}
            className="overflow-hidden"
          >
            {findings.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center bg-[radial-gradient(ellipse_at_center,_rgba(16,185,129,0.08),_transparent_70%)] p-6 text-center">
                <div className="flex h-20 w-20 items-center justify-center rounded-full bg-emerald-50 text-emerald-500 shadow-inner shadow-emerald-100">
                  <ShieldCheck size={48} strokeWidth={1.5} />
                </div>
                <h3 className="mt-4 text-xl font-bold tracking-tight text-slate-800">
                  File is safe
                </h3>
                <p className="mt-2 max-w-sm text-sm text-slate-500">
                  No security vulnerabilities or risky patterns were detected in <span className="font-mono text-xs text-slate-600">{selectedFile.name}</span>.
                </p>
              </div>
            ) : (
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
                      <BarChart
                        data={vulnerabilitiesByType}
                        layout="vertical"
                        margin={{ top: 10, right: 20, left: 0, bottom: 10 }}
                      >
                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E5E7EB" />
                        <XAxis type="number" tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
                        <YAxis
                          type="category"
                          dataKey="name"
                          width={140}
                          tick={{ fontSize: 11 }}
                          tickLine={false}
                          axisLine={false}
                        />
                        <Tooltip
                          cursor={{ fill: '#F9FAFB' }}
                          contentStyle={{
                            borderRadius: '12px',
                            border: 'none',
                            boxShadow: '0 12px 24px -12px rgba(15, 23, 42, 0.25)',
                          }}
                        />
                        <Bar dataKey="count" radius={[0, 6, 6, 0]} barSize={18}>
                          {vulnerabilitiesByType.map((entry, index) => (
                            <Cell
                              key={`${entry.name}-${index}`}
                              fill={vulnerabilityTypeColors[index % vulnerabilityTypeColors.length]}
                            />
                          ))}
                        </Bar>
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
                        <Pie
                          data={severityBreakdown}
                          innerRadius={48}
                          outerRadius={78}
                          paddingAngle={4}
                          dataKey="value"
                        >
                          {severityBreakdown.map((entry) => (
                            <Cell key={entry.name} fill={severityColors[entry.name as keyof typeof severityColors]} />
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
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
