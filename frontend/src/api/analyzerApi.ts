import type { AnalysisResult } from '../types/analysis';
const API_URL = 'http://localhost:8000';

export interface DatabaseConfig {
  mode: 'single' | 'per_folder';
  default_database: string;
  folder_databases: Record<string, string>;
}

export async function analyzeProject(
  projectFile: File,
  databaseConfig: DatabaseConfig
): Promise<AnalysisResult> {
  const formData = new FormData();

  formData.append('project', projectFile);
  formData.append('database_config', JSON.stringify(databaseConfig));

  const response = await fetch(`${API_URL}/analyze-project`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Project analysis failed.');
  }

  const data = await response.json();

  if (data.error) {
    throw new Error(data.error);
  }

  return data;
}

export async function analyzeFolder(
  files: File[],
  databaseConfig: DatabaseConfig
): Promise<AnalysisResult> {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append('files', file, file.webkitRelativePath || file.name);
  });

  formData.append('database_config', JSON.stringify(databaseConfig));

  const response = await fetch(`${API_URL}/analyze-folder`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Folder analysis failed.');
  }

  const data = await response.json();

  if (data.error) {
    throw new Error(data.error);
  }

  return data;
}

export async function analyzeGitHubProject(
  repoUrl: string,
  databaseConfig: DatabaseConfig
): Promise<AnalysisResult> {
  const response = await fetch(`${API_URL}/analyze-github`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      repo_url: repoUrl,
      database_config: databaseConfig,
    }),
  });

  if (!response.ok) {
    throw new Error('GitHub project analysis failed.');
  }

  const data = await response.json();

  if (data.error) {
    throw new Error(data.error);
  }

  return data;
}