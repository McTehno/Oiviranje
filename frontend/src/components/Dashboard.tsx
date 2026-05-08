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
                  {/* ResponsiveContainer poskrbi, da graf zapolni razpolozljiv prostor in ostane odziven. */}
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={vulnerabilitiesByType}
                      layout="vertical"
                      margin={{ top: 10, right: 20, left: 0, bottom: 10 }}
                    >
                      {/* CartesianGrid doda subtilno mrezo, da je primerjanje dolzin lazje. */}
                      <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E5E7EB" />
                      {/* XAxis prikazuje stevilo findingov, YAxis pa tip napada. */}
                      <XAxis type="number" tick={{ fontSize: 11 }} tickLine={false} axisLine={false} />
                      <YAxis
                        type="category"
                        dataKey="name"
                        width={140}
                        tick={{ fontSize: 11 }}
                        tickLine={false}
                        axisLine={false}
                      />
                      {/* Tooltip pokaze natancno vrednost ob hoverju nad posameznim vodoravnim stolpcem. */}
                      <Tooltip
                        cursor={{ fill: '#F9FAFB' }}
                        contentStyle={{
                          borderRadius: '12px',
                          border: 'none',
                          boxShadow: '0 12px 24px -12px rgba(15, 23, 42, 0.25)',
                        }}
                      />
                      {/* Bar vsebuje serijo stolpcev, Cell pa vsakemu stolpcu dodeli svojo barvo. */}
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
                  {/* ResponsiveContainer omogoce, da se pie chart prilagaja prostoru kartice. */}
                  <ResponsiveContainer width="100%" height="100%">
                    {/* PieChart vizualno prikaze razporeditev po severity nivojih. */}
                    <PieChart>
                      {/* Pie pobere pripravljene podatke, Cell pa vsakemu izseku nastavi barvo iz skupnega severity mapa. */}
                      <Pie
                        data={severityBreakdown}
                        innerRadius={48}
                        outerRadius={78}
                        paddingAngle={4}
                        dataKey="value"
                      >
                        {severityBreakdown.map((entry) => (
                          <Cell key={entry.name} fill={severityColors[entry.name]} />
                        ))}
                      </Pie>
                      {/* Tooltip prikaze stevilo findingov za trenutno izbran severity segment. */}
                      <Tooltip
                        contentStyle={{
                          borderRadius: '12px',
                          border: 'none',
                          boxShadow: '0 12px 24px -12px rgba(15, 23, 42, 0.25)',
                        }}
                      />
                      {/* Legend razlozi, katera barva pripada posameznemu severity nivoju. */}
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
