import React, { useState } from 'react';
import { Upload, ShieldCheck } from 'lucide-react';
import { analyzeFolder, analyzeGitHubProject, analyzeProject } from '../api/analyzerApi';
import type { AnalysisResult } from '../types/analysis';

interface UploadPanelProps {
  onAnalyzeComplete: (result: AnalysisResult) => void;
}

type UploadMode = 'zip' | 'folder' | 'github';

export const UploadPanel: React.FC<UploadPanelProps> = ({ onAnalyzeComplete }) => {
  // Uporabnik lahko naloži ZIP, mapo projekta ali GitHub repozitorij
  const [uploadMode, setUploadMode] = useState<UploadMode>('zip');

  // Izbrana ZIP datoteka
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // Datoteke iz izbrane mape
  const [selectedFolderFiles, setSelectedFolderFiles] = useState<File[]>([]);

  // URL repozitorija, če uporabnik izbere GitHub upload
  const [repoUrl, setRepoUrl] = useState('');

  // Privzeta baza, ki jo pošljemo backendu kot database context
  const [database, setDatabase] = useState('mysql');

  // Stanje med izvajanjem analize
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Sporočilo o napaki, če upload ali analiza ne uspe
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (uploadMode === 'zip' && !selectedFile) {
      setError('Please select a ZIP project file.');
      return;
    }

    if (uploadMode === 'folder' && selectedFolderFiles.length === 0) {
      setError('Please select a project folder.');
      return;
    }

    if (uploadMode === 'github' && !repoUrl.trim()) {
      setError('Please enter a GitHub repository URL.');
      return;
    }

    try {
      setError(null);
      setIsAnalyzing(true);

      const databaseConfig = {
        mode: 'single' as const,
        default_database: database,
        folder_databases: {},
      };

      /*
        Glede na izbrani način nalaganja pokličemo ustrezen API endpoint.
        Vsi trije načini vrnejo isti AnalysisResult za prikaz v App.tsx.
      */
      let result: AnalysisResult;

      if (uploadMode === 'zip') {
        result = await analyzeProject(selectedFile!, databaseConfig);
      } else if (uploadMode === 'folder') {
        result = await analyzeFolder(selectedFolderFiles, databaseConfig);
      } else {
        result = await analyzeGitHubProject(repoUrl.trim(), databaseConfig);
      }

      onAnalyzeComplete(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="flex-1 flex items-center justify-center bg-gray-50">
      <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-8 w-full max-w-xl">
        <div className="flex items-center mb-6">
          <ShieldCheck className="text-indigo-600 mr-3" size={28} />

          <div>
            <h2 className="text-xl font-bold text-gray-900">Analyze Project</h2>
            <p className="text-sm text-gray-500">
              Upload a ZIP file, choose a project folder, or import a public GitHub repository.
            </p>
          </div>
        </div>

        <div className="space-y-5">
          {/* Izbira načina nalaganja projekta */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Type
            </label>

            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => {
                  setUploadMode('zip');
                  setSelectedFolderFiles([]);
                  setRepoUrl('');
                  setError(null);
                }}
                className={`border rounded-md py-2 text-sm font-medium ${
                  uploadMode === 'zip'
                    ? 'bg-indigo-50 border-indigo-500 text-indigo-700'
                    : 'bg-white border-gray-300 text-gray-700'
                }`}
              >
                ZIP file
              </button>

              <button
                type="button"
                onClick={() => {
                  setUploadMode('folder');
                  setSelectedFile(null);
                  setRepoUrl('');
                  setError(null);
                }}
                className={`border rounded-md py-2 text-sm font-medium ${
                  uploadMode === 'folder'
                    ? 'bg-indigo-50 border-indigo-500 text-indigo-700'
                    : 'bg-white border-gray-300 text-gray-700'
                }`}
              >
                Folder
              </button>

              <button
                type="button"
                onClick={() => {
                  setUploadMode('github');
                  setSelectedFile(null);
                  setSelectedFolderFiles([]);
                  setError(null);
                }}
                className={`border rounded-md py-2 text-sm font-medium ${
                  uploadMode === 'github'
                    ? 'bg-indigo-50 border-indigo-500 text-indigo-700'
                    : 'bg-white border-gray-300 text-gray-700'
                }`}
              >
                GitHub
              </button>
            </div>
          </div>

          {/* ZIP upload */}
          {uploadMode === 'zip' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project ZIP
              </label>

              <input
                type="file"
                accept=".zip"
                onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
                className="block w-full text-sm text-gray-700 border border-gray-300 rounded-md p-2"
              />
            </div>
          )}

          {/* Folder upload */}
          {uploadMode === 'folder' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Project Folder
              </label>

              <input
                type="file"
                multiple
                {...({ webkitdirectory: 'true' } as React.InputHTMLAttributes<HTMLInputElement>)}
                onChange={(event) => {
                  const files = Array.from(event.target.files || []);
                  setSelectedFolderFiles(files);
                }}
                className="block w-full text-sm text-gray-700 border border-gray-300 rounded-md p-2"
              />

              {selectedFolderFiles.length > 0 && (
                <p className="text-xs text-gray-500 mt-2">
                  Selected {selectedFolderFiles.length} files.
                </p>
              )}
            </div>
          )}

          {/* GitHub import */}
          {uploadMode === 'github' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                GitHub Repository URL
              </label>

              <input
                type="text"
                value={repoUrl}
                onChange={(event) => setRepoUrl(event.target.value)}
                placeholder="https://github.com/user/repository"
                className="block w-full text-sm text-gray-700 border border-gray-300 rounded-md p-2"
              />

              <p className="text-xs text-gray-500 mt-2">
                Public GitHub repositories are supported.
              </p>
            </div>
          )}

          {/* Izbira privzete podatkovne baze */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Default Database
            </label>

            <select
              value={database}
              onChange={(event) => setDatabase(event.target.value)}
              className="block w-full border border-gray-300 rounded-md p-2 text-sm"
            >
              <option value="mysql">MySQL</option>
              <option value="mongodb">MongoDB</option>
            </select>
          </div>

          {/* Prikaz napake pri uploadu ali analizi */}
          {error && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-3">
              {error}
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className="w-full bg-indigo-600 text-white rounded-md py-2.5 text-sm font-semibold flex items-center justify-center disabled:opacity-60"
          >
            <Upload size={16} className="mr-2" />
            {isAnalyzing ? 'Analyzing...' : 'Analyze Project'}
          </button>
        </div>
      </div>
    </div>
  );
};