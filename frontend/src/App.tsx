import React, { useMemo, useState } from 'react';
import { FileTree } from './components/FileTree';
import { CodeViewer } from './components/CodeViewer';
import { Dashboard } from './components/Dashboard';
import { UploadPanel } from './components/UploadPanel';
import { ShieldCheck, RotateCcw } from 'lucide-react';

import type { AnalysisResult, FileData } from './types/analysis';
import { buildFileTree } from './utils/buildFileTree';

const App: React.FC = () => {
  /*
    analysisResult hrani celoten rezultat analize, ki ga vrne backend.
    Dokler je vrednost null, uporabnik še ni zagnal analize in prikaže se UploadPanel.
    Ko backend vrne rezultat, se prikaže glavni pogled z datotekami, kodo in dashboardom.
  */
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  /*
    selectedFile hrani trenutno izbrano datoteko iz FileTree komponente.
    CodeViewer uporablja to datoteko za prikaz kode.
  */
  const [selectedFile, setSelectedFile] = useState<FileData | null>(null);

  /*
    Backend vrne datoteke kot navaden seznam.
    Primer:
      src/app.py
      src/database/query.py

    FileTree pa potrebuje drevesno strukturo map in datotek.
    Zato se seznam datotek pretvori v drevo s funkcijo buildFileTree.
  */
  const fileTree = useMemo(() => {
    if (!analysisResult) {
      return [];
    }

    return buildFileTree(analysisResult.files);
  }, [analysisResult]);

  /*
    Iz vseh findingov izberemo samo tiste, ki pripadajo trenutno izbrani datoteki.
    Tako CodeViewer označi ranljive vrstice samo v odprti datoteki.
  */
  const selectedFileFindings = useMemo(() => {
    if (!analysisResult || !selectedFile) {
      return [];
    }

    return analysisResult.findings.filter(
      (finding) => finding.file_path === selectedFile.path
    );
  }, [analysisResult, selectedFile]);

  /*
    Ko uporabnik klikne datoteko v FileTree, jo shranimo kot selectedFile.
    Mape se tukaj ne izbirajo za preview, samo datoteke.
  */
  const handleSelectFile = (file: FileData) => {
    if (file.type === 'file') {
      setSelectedFile(file);
    }
  };

  /*
    Resetira trenutno analizo in uporabnika vrne nazaj na začetni upload zaslon.
  */
  const handleReset = () => {
    setAnalysisResult(null);
    setSelectedFile(null);
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-background text-gray-800">
      {/* Zgornja navigacijska vrstica z imenom aplikacije in osnovnim povzetkom analize */}
      <header className="h-12 border-b border-gray-200 bg-white flex items-center px-4 shrink-0 shadow-sm z-20">
        <ShieldCheck className="text-indigo-600 mr-2" size={20} />

        <h1 className="font-bold text-gray-800 tracking-tight text-sm">
          SAST<span className="font-light text-gray-500">Analyzer</span>
        </h1>

        {/* Po analizi se v headerju prikaže kratek povzetek rezultata */}
        {analysisResult && (
          <div className="ml-4 text-xs text-gray-500">
            Score: {analysisResult.project_score}/100 · Risk: {analysisResult.overall_risk} · Findings: {analysisResult.total_findings}
          </div>
        )}

        {/* Gumb za začetek nove analize */}
        {analysisResult && (
          <button
            onClick={handleReset}
            className="ml-auto text-xs text-gray-600 hover:text-indigo-600 flex items-center"
          >
            <RotateCcw size={14} className="mr-1" />
            New scan
          </button>
        )}
      </header>

      {!analysisResult ? (
        /*
          Začetni zaslon.
          UploadPanel naloži ZIP projekt in po uspešni analizi nastavi analysisResult.
        */
        <UploadPanel onAnalyzeComplete={setAnalysisResult} />
      ) : (
        /*
          Glavni zaslon po analizi:
          levo je drevo datotek, na sredini je preview kode,
          spodaj pa dashboard s statistiko.
        */
        <>
          <div className="flex-1 flex overflow-hidden">
            <FileTree
              data={fileTree}
              onSelectFile={handleSelectFile}
              selectedFileId={selectedFile?.id || null}
            />

            <CodeViewer
              file={selectedFile}
              findings={selectedFileFindings}
            />
          </div>

          <Dashboard result={analysisResult} />
        </>
      )}
    </div>
  );
};

export default App;