import React, { useMemo, useState } from 'react';
import { Home, RotateCcw, ShieldCheck } from 'lucide-react';
import { FileTree } from './components/FileTree';
import { CodeViewer } from './components/CodeViewer';
import { Dashboard } from './components/Dashboard';
import { GlobalStatistics } from './components/GlobalStatistics';
import { UploadPanel } from './components/UploadPanel';
import type { AnalysisResult, FileData } from './types/analysis';
import { buildFileTree } from './utils/buildFileTree';

const App: React.FC = () => {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [selectedFile, setSelectedFile] = useState<FileData | null>(null);

  const fileTree = useMemo(() => {
    if (!analysisResult) {
      return [];
    }

    return buildFileTree(analysisResult.files);
  }, [analysisResult]);

  const selectedFileFindings = useMemo(() => {
    if (!analysisResult || !selectedFile) {
      return [];
    }

    return analysisResult.findings.filter(
      (finding) => finding.file_path === selectedFile.path
    );
  }, [analysisResult, selectedFile]);

  const handleSelectFile = (file: FileData) => {
    if (file.type === 'file') {
      setSelectedFile(file);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setSelectedFile(null);
  };

  const handleCloseFile = () => {
    setSelectedFile(null);
  };

  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-background text-gray-800">
      <header className="z-20 flex h-12 shrink-0 items-center border-b border-gray-200 bg-white px-4 shadow-sm">
        <ShieldCheck className="mr-2 text-indigo-600" size={20} />

        <h1 className="text-sm font-bold tracking-tight text-gray-800">
          SAST<span className="font-light text-gray-500">Analyzer</span>
        </h1>

        {analysisResult && (
          <div className="ml-4 hidden text-xs text-gray-500 md:block">
            Score: {analysisResult.project_score}/100 · Risk: {analysisResult.overall_risk} · Findings: {analysisResult.total_findings}
          </div>
        )}

        {analysisResult && (
          <div className="ml-auto flex items-center gap-2">
            {selectedFile && (
              <button
                type="button"
                onClick={handleCloseFile}
                className="inline-flex items-center rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-600 transition-colors hover:border-gray-300 hover:bg-gray-50 hover:text-gray-900"
              >
                <Home size={14} className="mr-1.5" />
                Back to overview
              </button>
            )}

            <button
              type="button"
              onClick={handleReset}
              className="inline-flex items-center rounded-lg border border-indigo-200 px-3 py-1.5 text-xs font-medium text-indigo-700 transition-colors hover:bg-indigo-50 hover:text-indigo-800"
            >
              <RotateCcw size={14} className="mr-1.5" />
              New scan
            </button>
          </div>
        )}
      </header>

      {!analysisResult ? (
        <UploadPanel onAnalyzeComplete={setAnalysisResult} />
      ) : (
        <div className="flex flex-1 overflow-hidden">
          <FileTree
            data={fileTree}
            onSelectFile={handleSelectFile}
            selectedFileId={selectedFile?.id || null}
          />

          <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
            {selectedFile ? (
              <>
                <CodeViewer file={selectedFile} findings={selectedFileFindings} />
                <Dashboard selectedFile={selectedFile} findings={selectedFileFindings} />
              </>
            ) : (
              <GlobalStatistics result={analysisResult} />
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;