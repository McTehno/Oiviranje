import React from 'react';
import { Filter, Search } from 'lucide-react';
import type { Severity } from '../types/analysis';
import { severityOptions } from '../utils/severity';

export type FindingSortOption =
  | 'severity-desc'
  | 'severity-asc'
  | 'file-asc'
  | 'line-asc'
  | 'type-asc';

export interface FindingFilterState {
  severity: 'ALL' | Severity;
  attackType: 'ALL' | string;
  language: 'ALL' | string;
  pathQuery: string;
  sortBy: FindingSortOption;
}

interface FindingFiltersProps {
  filters: FindingFilterState;
  attackTypes: string[];
  languages: string[];
  totalCount: number;
  visibleCount: number;
  onChange: (filters: FindingFilterState) => void;
  onReset: () => void;
}

export const FindingFilters: React.FC<FindingFiltersProps> = ({
  filters,
  attackTypes,
  languages,
  totalCount,
  visibleCount,
  onChange,
  onReset,
}) => {
  const hasFilters =
    filters.severity !== 'ALL' ||
    filters.attackType !== 'ALL' ||
    filters.language !== 'ALL' ||
    filters.pathQuery.trim().length > 0;

  return (
    <div className="border-b border-gray-200 bg-white px-4 py-3 shadow-sm">
      <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">
        <div className="flex items-center gap-2 text-sm font-semibold text-gray-700">
          <Filter size={16} className="text-indigo-500" />
          Findings triage
          <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-500">
            {visibleCount} of {totalCount} shown
          </span>
        </div>

        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-5 xl:flex xl:items-center">
          <label className="relative min-w-[190px]">
            <Search size={14} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="search"
              value={filters.pathQuery}
              onChange={(event) => onChange({ ...filters, pathQuery: event.target.value })}
              placeholder="Search file path"
              className="h-9 w-full rounded-lg border border-gray-200 bg-white pl-9 pr-3 text-xs text-gray-700 outline-none transition focus:border-indigo-300 focus:ring-2 focus:ring-indigo-100"
            />
          </label>

          <select
            value={filters.severity}
            onChange={(event) => onChange({ ...filters, severity: event.target.value as FindingFilterState['severity'] })}
            className="h-9 rounded-lg border border-gray-200 bg-white px-3 text-xs text-gray-700 outline-none transition focus:border-indigo-300 focus:ring-2 focus:ring-indigo-100"
            aria-label="Filter by severity"
          >
            <option value="ALL">All severities</option>
            {severityOptions.map((severity) => (
              <option key={severity} value={severity}>{severity}</option>
            ))}
          </select>

          <button
            type="button"
            onClick={onReset}
            disabled={!hasFilters && filters.sortBy === 'severity-desc'}
            className="h-9 rounded-lg border border-gray-200 px-3 text-xs font-medium text-gray-600 transition hover:border-gray-300 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  );
};