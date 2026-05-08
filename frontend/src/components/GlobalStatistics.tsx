import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
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
  BarChart3,
  FileText,
  FileWarning,
  Lightbulb,
  PieChart as PieChartIcon,
  ShieldAlert,
  ShieldCheck,
  Target,
} from 'lucide-react';
import type { AnalysisResult } from '../types/analysis';
import {
  severityColors,
  summarizeFindingsByAttackType,
  summarizeFindingsByFile,
  summarizeFindingsBySeverity,
  type FileSeveritySummary,
  vulnerabilityTypeColors,
} from '../utils/severity';

interface GlobalStatisticsProps {
  result: AnalysisResult;
}

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle: string;
  icon: React.ReactNode;
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtitle, icon }) => (
  <div className="rounded-3xl border border-white/70 bg-white/90 p-5 shadow-[0_10px_30px_-15px_rgba(15,23,42,0.25)] backdrop-blur">
    <div className="flex items-start justify-between gap-4">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">{title}</p>
        <div className="mt-3 text-3xl font-black text-slate-900">{value}</div>
        <p className="mt-2 text-sm text-slate-500">{subtitle}</p>
      </div>

      <div className="rounded-2xl bg-slate-900/5 p-3 text-slate-700">{icon}</div>
    </div>
  </div>
);

export const GlobalStatistics: React.FC<GlobalStatisticsProps> = ({ result }) => {
  const isSafeProject = result.total_findings === 0 || result.overall_risk === 'SAFE';

  // `vulnerabilitiesByType` vzame vse findinge na nivoju celotnega repozitorija,
  // jih zdruzi po `attack_type` in pripravi podatke za globalni vodoravni bar chart.
  // UI ga uporablja za primerjavo najpogostejših napadalnih vzorcev v projektu.
  const vulnerabilitiesByType = useMemo(
    () => summarizeFindingsByAttackType(result.findings),
    [result.findings]
  );

  // `severityBreakdown` iz vseh findingov izdela globalno porazdelitev po resnosti.
  // Ta rezultat napaja pie chart in pokaže, koliko CRITICAL/HIGH/MEDIUM/LOW/SAFE primerov je v projektu.
  const severityBreakdown = useMemo(
    () => summarizeFindingsBySeverity(result.findings),
    [result.findings]
  );

  // `topExploitableFiles` zdruzi findinge po datotekah, za vsako datoteko izracuna
  // skupno stevilo findingov in najvisjo resnost ter pripravi seznam za globalni pregled.
  // UI iz tega izriše najbolj izpostavljene datoteke z barvnim progress barom.
  const topExploitableFiles = useMemo<FileSeveritySummary[]>(
    () => summarizeFindingsByFile(result.findings).slice(0, 5),
    [result.findings]
  );

  const maxFileIssues = Math.max(1, ...topExploitableFiles.map((file) => file.count));

  if (isSafeProject) {
    return (
      <div className="flex-1 min-h-0 overflow-y-auto bg-[radial-gradient(circle_at_top,_rgba(16,185,129,0.16),_transparent_45%),linear-gradient(180deg,_rgba(236,253,245,0.9),_rgba(255,255,255,1))]">
        <div className="flex min-h-full items-center justify-center p-6 md:p-10">
          <motion.div
            initial={{ opacity: 0, y: 14, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            transition={{ duration: 0.35 }}
            className="w-full max-w-3xl rounded-[2rem] border border-emerald-200 bg-white/95 p-8 text-center shadow-[0_20px_60px_-20px_rgba(16,185,129,0.35)] backdrop-blur"
          >
            <div className="mx-auto flex h-36 w-36 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 shadow-inner shadow-emerald-200/60">
              <ShieldCheck size={104} strokeWidth={1.6} />
            </div>

            <h2 className="mt-8 text-4xl font-black tracking-tight text-slate-900 md:text-5xl">
              Project is safe
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-600 md:text-xl">
              No vulnerabilities were found in this repository.
            </p>

            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              <MetricCard
                title="Project score"
                value={`${result.project_score}/100`}
                subtitle="The overall security score is in the safe range."
                icon={<Target size={22} />}
              />
              <MetricCard
                title="Files analyzed"
                value={result.files_analyzed}
                subtitle="All scanned files were checked successfully."
                icon={<FileText size={22} />}
              />
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 min-h-0 overflow-y-auto bg-[radial-gradient(circle_at_top,_rgba(99,102,241,0.12),_transparent_40%),linear-gradient(180deg,_rgba(248,250,252,1),_rgba(244,247,255,0.92))]">
      <div className="space-y-6 p-6 md:p-8">
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-[0_16px_40px_-24px_rgba(15,23,42,0.4)] backdrop-blur"
        >
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.35em] text-slate-500">
                Global statistics
              </p>
              <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-900 md:text-4xl">
                Repository-wide security overview
              </h2>
              <p className="mt-3 max-w-3xl text-sm text-slate-600 md:text-base">
                This view aggregates all findings across the project and highlights the most exposed files,
                the dominant attack patterns, and the next remediation steps.
              </p>
            </div>

            <div className="inline-flex items-center gap-3 self-start rounded-full border border-slate-200 bg-slate-950 px-4 py-2 text-sm font-semibold text-white shadow-sm">
              <ShieldAlert size={16} className="text-amber-300" />
              {result.overall_risk} risk · {result.total_findings} findings
            </div>
          </div>
        </motion.div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard
            title="Project score"
            value={`${result.project_score}/100`}
            subtitle="Higher is better."
            icon={<Target size={22} />}
          />
          <MetricCard
            title="Overall risk"
            value={result.overall_risk}
            subtitle="Repository-level severity summary."
            icon={<ShieldAlert size={22} />}
          />
          <MetricCard
            title="Total findings"
            value={result.total_findings}
            subtitle="All detected issues across the scan."
            icon={<FileWarning size={22} />}
          />
          <MetricCard
            title="Files analyzed"
            value={result.files_analyzed}
            subtitle="Files included in the completed scan."
            icon={<FileText size={22} />}
          />
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: 0.05 }}
            className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-[0_16px_40px_-24px_rgba(15,23,42,0.4)]"
          >
            <div className="mb-4 flex items-center gap-3">
              <div className="rounded-2xl bg-indigo-50 p-2 text-indigo-600">
                <BarChart3 size={18} />
              </div>
              <div>
                <h3 className="text-base font-semibold text-slate-900">Vulnerabilities by Type</h3>
                <p className="text-sm text-slate-500">Global distribution across the repository.</p>
              </div>
            </div>

            <div className="h-[320px]">
              {/* ResponsiveContainer zagotovi, da graf zapolni celotno kartico in ostane odziven. */}
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={vulnerabilitiesByType}
                  layout="vertical"
                  margin={{ top: 10, right: 20, left: 0, bottom: 10 }}
                >
                  {/* CartesianGrid doda ozadje z mrezo, ki pomaga pri branju dolzin stolpcev. */}
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E2E8F0" />
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
                  {/* Tooltip prikaze natančne podatke ob hoverju nad posameznim vodoravnim stolpcem. */}
                  <Tooltip
                    cursor={{ fill: '#F8FAFC' }}
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
          </motion.section>

          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: 0.1 }}
            className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-[0_16px_40px_-24px_rgba(15,23,42,0.4)]"
          >
            <div className="mb-4 flex items-center gap-3">
              <div className="rounded-2xl bg-rose-50 p-2 text-rose-600">
                <PieChartIcon size={18} />
              </div>
              <div>
                <h3 className="text-base font-semibold text-slate-900">Severity Breakdown</h3>
                <p className="text-sm text-slate-500">Repository-level risk distribution.</p>
              </div>
            </div>

            <div className="h-[320px]">
              {/* ResponsiveContainer prilagodi krozni graf velikosti vsebovane kartice. */}
              <ResponsiveContainer width="100%" height="100%">
                {/* PieChart prikazuje razporeditev severity nivojev v krogu. */}
                <PieChart>
                  {/* Pie porabi agregirane podatke, Cell pa vsakemu izseku dodeli skupno severity barvo. */}
                  <Pie data={severityBreakdown} innerRadius={50} outerRadius={82} paddingAngle={4} dataKey="value">
                    {severityBreakdown.map((entry) => (
                      <Cell key={entry.name} fill={severityColors[entry.name]} />
                    ))}
                  </Pie>
                  {/* Tooltip po hoverju pokaže dejansko vrednost posameznega izseka. */}
                  <Tooltip
                    contentStyle={{
                      borderRadius: '12px',
                      border: 'none',
                      boxShadow: '0 12px 24px -12px rgba(15, 23, 42, 0.25)',
                    }}
                  />
                  {/* Legend pojasni, kateri severity nivo predstavlja posamezna barva. */}
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
          </motion.section>
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: 0.15 }}
            className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-[0_16px_40px_-24px_rgba(15,23,42,0.4)]"
          >
            <div className="mb-4 flex items-center gap-3">
              <div className="rounded-2xl bg-amber-50 p-2 text-amber-600">
                <FileWarning size={18} />
              </div>
              <div>
                <h3 className="text-base font-semibold text-slate-900">Top Exploitable Files</h3>
                <p className="text-sm text-slate-500">Files with the highest number of findings.</p>
              </div>
            </div>

            {topExploitableFiles.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50/70 p-6 text-sm text-slate-500">
                No vulnerable files were found in the current scan.
              </div>
            ) : (
              <div className="space-y-4">
                {topExploitableFiles.map((file, index) => (
                  <div key={file.path} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                    <div className="flex items-start justify-between gap-4">
                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-bold text-slate-600">
                            {index + 1}
                          </span>
                          <p className="truncate font-mono text-sm font-medium text-slate-800" title={file.path}>
                            {file.path}
                          </p>
                        </div>
                        <p className="mt-2 text-xs text-slate-500">{file.count} findings</p>
                      </div>

                      <span
                        className="inline-flex shrink-0 items-center rounded-full border px-2.5 py-1 text-[11px] font-semibold"
                        style={{
                          borderColor: severityColors[file.risk],
                          color: severityColors[file.risk],
                        }}
                      >
                        {file.risk}
                      </span>
                    </div>

                    <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${(file.count / maxFileIssues) * 100}%`,
                          backgroundColor: severityColors[file.risk],
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.section>

          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, delay: 0.2 }}
            className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-[0_16px_40px_-24px_rgba(15,23,42,0.4)]"
          >
            <div className="mb-4 flex items-center gap-3">
              <div className="rounded-2xl bg-emerald-50 p-2 text-emerald-600">
                <Lightbulb size={18} />
              </div>
              <div>
                <h3 className="text-base font-semibold text-slate-900">Recommendations</h3>
                <p className="text-sm text-slate-500">Suggested next steps from the analyzer.</p>
              </div>
            </div>

            {result.recommendations.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50/70 p-6 text-sm text-slate-500">
                No additional recommendations were generated.
              </div>
            ) : (
              <div className="space-y-3">
                {result.recommendations.map((recommendation, index) => (
                  <div
                    key={`${index}-${recommendation}`}
                    className="rounded-2xl border border-emerald-100 bg-emerald-50/60 p-4 shadow-sm"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-sm font-bold text-emerald-700">
                        {index + 1}
                      </div>
                      <p className="text-sm leading-6 text-slate-700">{recommendation}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.section>
        </div>
      </div>
    </div>
  );
};
