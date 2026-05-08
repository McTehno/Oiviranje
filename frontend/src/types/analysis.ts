export type Severity =
  | 'SAFE'
  | 'LOW'
  | 'MEDIUM'
  | 'HIGH'
  | 'CRITICAL'
  | 'UNKNOWN';

// Backend sedaj eksplicitno oznaci, od kod izvira sken.
// To nam omogoca, da ob vrnitvi na UploadPanel odstranimo samo GitHub ZIP artefakt,
// medtem ko drugih vrst skenov ne tisimo skozi nepotrebno cleanup pot.
export type ScanSource = 'zip' | 'folder' | 'github';

export interface Finding {
  file_path: string;
  line: number;
  type: string;
  code: string;
  variables: string[];
  language: string;
  database: string;
  risk: Severity;
  attack_type: string;
  description: string;
  recommendation: string;
}

export interface FileData {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'folder';
  language?: string;
  database?: string;
  content?: string;
  findings_count?: number;
  risk?: Severity;
  error?: string;
  children?: FileData[];
}

export interface AnalysisResult {
  scan_id?: string;
  source?: ScanSource;
  repo_url?: string;
  project_score: number;
  overall_risk: Severity;
  total_findings: number;
  files_analyzed: number;
  files: FileData[];
  findings: Finding[];
  summary: {
    findings_by_type: Record<string, number>;
    findings_by_risk: Record<string, number>;
    findings_by_file: Record<string, number>;
  };
  recommendations: string[];
}