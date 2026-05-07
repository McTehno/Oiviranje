import React, { useState } from 'react';
import type { FileData } from '../types/analysis';
import { ChevronRight, ChevronDown, Folder, File } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface FileTreeProps {
  data: FileData[];
  onSelectFile: (file: FileData) => void;
  selectedFileId: string | null;
}

const FileTreeNode: React.FC<{
  node: FileData;
  level: number;
  onSelectFile: (file: FileData) => void;
  selectedFileId: string | null;
}> = ({ node, level, onSelectFile, selectedFileId }) => {
  const [isOpen, setIsOpen] = useState(true);

  const isFolder = node.type === 'folder';
  const isSelected = node.id === selectedFileId;

  /*
    Če uporabnik klikne mapo, jo odpremo/zapremo.
    Če klikne datoteko, jo pošljemo v App.tsx kot izbrano datoteko.
  */
  const handleToggle = (event: React.MouseEvent) => {
    event.stopPropagation();

    if (isFolder) {
      setIsOpen(!isOpen);
      return;
    }

    onSelectFile(node);
  };

  // Pri datotekah z ranljivostmi prikažemo majhno oznako s številom findingov
  const riskBadge =
    !isFolder && node.findings_count && node.findings_count > 0 ? (
      <span className="ml-auto text-[10px] bg-red-100 text-red-700 px-1.5 py-0.5 rounded-full">
        {node.findings_count}
      </span>
    ) : null;

  return (
    <div>
      <div
        className={`flex items-center py-1.5 px-2 cursor-pointer hover:bg-accent/50 transition-colors ${
          isSelected ? 'bg-accent text-blue-600 font-medium' : 'text-gray-700'
        }`}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
        onClick={handleToggle}
      >
        {/* Ikona za odpiranje/zapiranje map */}
        {isFolder ? (
          <span className="mr-1.5 text-gray-500">
            {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </span>
        ) : (
          <span className="mr-1.5 ml-4" />
        )}

        {/* Različna ikona za mapo in datoteko */}
        {isFolder ? (
          <Folder size={16} className="mr-2 text-blue-400 shrink-0" />
        ) : (
          <File size={16} className="mr-2 text-gray-400 shrink-0" />
        )}

        <span className="text-sm truncate select-none">{node.name}</span>

        {riskBadge}
      </div>

      {/* Rekurzivni prikaz podmap in datotek */}
      <AnimatePresence>
        {isFolder && isOpen && node.children && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            {node.children.map((child) => (
              <FileTreeNode
                key={child.id}
                node={child}
                level={level + 1}
                onSelectFile={onSelectFile}
                selectedFileId={selectedFileId}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export const FileTree: React.FC<FileTreeProps> = ({
  data,
  onSelectFile,
  selectedFileId,
}) => {
  return (
    <div className="w-64 h-full bg-sidebar border-r border-gray-200 flex flex-col shrink-0">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
          Project Files
        </h2>
      </div>

      {/* Glavni seznam map in datotek */}
      <div className="flex-1 overflow-y-auto py-2">
        {data.length > 0 ? (
          data.map((node) => (
            <FileTreeNode
              key={node.id}
              node={node}
              level={0}
              onSelectFile={onSelectFile}
              selectedFileId={selectedFileId}
            />
          ))
        ) : (
          <div className="h-full flex items-center justify-center text-gray-400 text-sm px-6 text-center">
            No project files found.
          </div>
        )}
      </div>
    </div>
  );
};