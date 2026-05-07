import React, { useMemo, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronUp, ChevronDown, Activity } from 'lucide-react';
import type { AnalysisResult } from '../types/analysis';

interface DashboardProps {
  result: AnalysisResult;
}

// Barve za prikaz resnosti ranljivosti v grafih
const severityColors: Record<string, string> = {
  CRITICAL: '#EF4444',
  HIGH: '#F97316',
  MEDIUM: '#FACC15',
  LOW: '#22C55E',
  SAFE: '#22C55E',
  UNKNOWN: '#9CA3AF',
};

// Za posamezno datoteko poiščemo njen risk level
const getFileSeverity = (
  fileName: string,
  files: AnalysisResult['files']
): string => {
  const file = files.find((item) => item.path === fileName);
  return file?.risk || 'UNKNOWN';
};

export const Dashboard: React.FC<DashboardProps> = ({ result }) => {
  const [isExpanded, setIsExpanded] = useState(true);

  // Podatki za graf: ranljivosti po tipu napada
  const vulnerabilitiesByType = useMemo(() => {
    return Object.entries(result.summary.findings_by_type).map(([name, count]) => ({
      name,
      count,
    }));
  }, [result]);

  // Podatki za graf: ranljivosti po resnosti
  const severityBreakdown = useMemo(() => {
    return Object.entries(result.summary.findings_by_risk).map(([name, value]) => ({
      name,
      value,
      color: severityColors[name] || severityColors.UNKNOWN,
    }));
  }, [result]);

  // Najbolj problematične datoteke po številu findingov
  const topExploitableFiles = useMemo(() => {
    return Object.entries(result.summary.findings_by_file)
      .map(([name, count]) => ({
        name,
        count,
        severity: getFileSeverity(name, result.files),
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);
  }, [result]);

  // Uporablja se za izračun širine progress bara pri datotekah
  const maxFileIssues = Math.max(
    1,
    ...topExploitableFiles.map((file) => file.count)
  );

  return (
    <div className="border-t border-gray-200 bg-white flex flex-col shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] z-10 transition-all duration-300">
      {/* Glava dashboarda, klik jo razširi ali skrije */}
      <div
        className="h-10 border-b border-gray-100 bg-gray-50 flex items-center justify-between px-4 cursor-pointer hover:bg-gray-100"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center text-sm font-semibold text-gray-700 uppercase tracking-wide">
          <Activity size={16} className="mr-2 text-indigo-500" />
          Security Analytics

          <span className="ml-3 text-xs normal-case font-normal text-gray-500">
            Score: {result.project_score}/100 · Risk: {result.overall_risk} · Findings: {result.total_findings}
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
            animate={{ height: 280 }}
            exit={{ height: 0 }}
            className="overflow-hidden"
          >
            <div className="p-4 h-full grid grid-cols-3 gap-6">
              {/* Graf: ranljivosti po tipu */}
              <div className="flex flex-col">
                <h3 className="text-xs font-semibold text-gray-500 mb-2 uppercase text-center">
                  Vulnerabilities by Type
                </h3>

                <div className="flex-1 min-h-0">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={vulnerabilitiesByType}
                      margin={{ top: 10, right: 10, left: -20, bottom: 20 }}
                    >
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
                        cursor={{ fill: '#F3F4F6' }}
                        contentStyle={{
                          borderRadius: '6px',
                          border: 'none',
                          boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                        }}
                      />
                      <Bar dataKey="count" fill="#6366F1" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Graf: razporeditev po resnosti */}
              <div className="flex flex-col border-l border-gray-100 pl-6">
                <h3 className="text-xs font-semibold text-gray-500 mb-2 uppercase text-center">
                  Severity Breakdown
                </h3>

                <div className="flex-1 min-h-0">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={severityBreakdown}
                        innerRadius={45}
                        outerRadius={75}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {severityBreakdown.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>

                      <Tooltip
                        contentStyle={{
                          borderRadius: '6px',
                          border: 'none',
                          boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)',
                        }}
                      />

                      <Legend
                        verticalAlign="middle"
                        align="right"
                        layout="vertical"
                        iconType="circle"
                        wrapperStyle={{ fontSize: '11px' }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Seznam najbolj ranljivih datotek */}
              <div className="flex flex-col border-l border-gray-100 pl-6">
                <h3 className="text-xs font-semibold text-gray-500 mb-4 uppercase">
                  Top Exploitable Files
                </h3>

                <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                  {topExploitableFiles.length === 0 ? (
                    <div className="text-sm text-gray-500">
                      No vulnerable files found.
                    </div>
                  ) : (
                    topExploitableFiles.map((file, i) => (
                      <div key={i} className="flex flex-col gap-1">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-700 truncate font-mono text-xs">
                            {file.name}
                          </span>

                          <span className="font-medium text-gray-900 text-xs bg-gray-100 px-2 py-0.5 rounded">
                            {file.count} issues
                          </span>
                        </div>

                        <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                          <div
                            className={`h-1.5 rounded-full ${
                              file.severity === 'CRITICAL'
                                ? 'bg-red-500'
                                : file.severity === 'HIGH'
                                  ? 'bg-orange-500'
                                  : file.severity === 'MEDIUM'
                                    ? 'bg-yellow-400'
                                    : 'bg-green-500'
                            }`}
                            style={{ width: `${(file.count / maxFileIssues) * 100}%` }}
                          />
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};