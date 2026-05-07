import React from 'react';
import { Prism as SyntaxHighlighter, createElement } from 'react-syntax-highlighter';
import { coy } from 'react-syntax-highlighter/dist/esm/styles/prism';
import type { FileData, Finding } from '../types/analysis';
import { VulnerabilityWidget } from './VulnerabilityWidget';

interface CodeViewerProps {
  file: FileData | null;
  findings: Finding[];
}

export const CodeViewer: React.FC<CodeViewerProps> = ({ file, findings }) => {
  // Če uporabnik še ni izbral datoteke, prikažemo prazen začetni prikaz
  if (!file) {
    return (
      <div className="flex-1 flex items-center justify-center bg-white text-gray-400">
        <div className="text-center">
          <div className="text-4xl mb-2 text-gray-200">{"</>"}</div>
          <p>Select a file to view code</p>
        </div>
      </div>
    );
  }

  const { content, language } = file;

  /*
    Findinge uredimo po številki vrstice.
    Tako lahko hitro preverimo, ali ima določena vrstica ranljivost.
  */
  const findingsByLine = new Map<number, Finding[]>();

  findings.forEach((finding) => {
    if (!findingsByLine.has(finding.line)) {
      findingsByLine.set(finding.line, []);
    }

    findingsByLine.get(finding.line)!.push(finding);
  });

  return (
    <div className="flex-1 flex flex-col h-full bg-white overflow-hidden relative">
      {/* Zgornja vrstica z imenom datoteke in osnovnimi informacijami */}
      <div className="h-10 flex items-center justify-between px-4 border-b border-gray-200 bg-gray-50/50 text-sm font-medium text-gray-600">
        <span>{file.path}</span>

        <span className="text-xs text-gray-400">
          {file.language} · {file.database} · {findings.length} finding{findings.length === 1 ? '' : 's'}
        </span>
      </div>

      {/* Prikaz kode s syntax highlightingom in številkami vrstic */}
      <div className="flex-1 overflow-auto bg-[#fafafa]">
        <SyntaxHighlighter
          language={language || 'text'}
          style={coy}
          customStyle={{
            margin: 0,
            padding: '16px 0',
            background: 'transparent',
            fontSize: '14px',
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
          }}
          showLineNumbers={true}
          wrapLines={true}
          lineProps={(lineNumber) => {
            const lineFindings = findingsByLine.get(lineNumber);

            // Če ima vrstica finding, jo vizualno označimo
            if (lineFindings && lineFindings.length > 0) {
              return {
                style: {
                  display: 'block',
                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                  borderLeft: '4px solid #EF4444',
                  boxShadow: 'inset 0 0 0 1px rgba(239, 68, 68, 0.2)',
                },
              };
            }

            return {
              style: { display: 'block', paddingLeft: '4px' },
            };
          }}
          renderer={({ rows, stylesheet, useInlineStyles }) => {
            return (
              <code style={{ display: 'block' }}>
                {rows.map((row, i) => {
                  const lineNumber = i + 1;
                  const lineFindings = findingsByLine.get(lineNumber) || [];

                  return (
                    <React.Fragment key={i}>
                      {/* Dejanska vrstica kode */}
                      {createElement({
                        node: row,
                        stylesheet,
                        useInlineStyles,
                        key: `code-line-${i}`,
                      })}

                      {/* Pod ranljivo vrstico prikažemo opis findinga */}
                      {lineFindings.map((finding, index) => (
                        <div
                          key={`${finding.file_path}-${finding.line}-${finding.attack_type}-${index}`}
                          className="my-2 px-8"
                        >
                          <VulnerabilityWidget finding={finding} />
                        </div>
                      ))}
                    </React.Fragment>
                  );
                })}
              </code>
            );
          }}
        >
          {content || ''}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};