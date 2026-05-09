import React, { useState, useMemo } from 'react';
import type { FileData } from '../types/analysis';
import { ChevronRight, ChevronDown, Folder, File, Search, Filter } from 'lucide-react';
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

  const handleToggle = (event: React.MouseEvent) => {
    event.stopPropagation();
    if (isFolder) {
      setIsOpen(!isOpen);
      return;
    }
    onSelectFile(node);
  };

  const riskBadge =
    !isFolder ? (
      <span
        className={`ml-auto text-[10px] px-1.5 py-0.5 rounded-full ${
          node.risk === 'SAFE'
            ? 'bg-green-100 text-green-700'
            : node.risk === 'HIGH'
              ? 'bg-orange-100 text-orange-700'
              : node.risk === 'CRITICAL'
                ? 'bg-red-100 text-red-700'
                : node.risk === 'MEDIUM'
                  ? 'bg-yellow-100 text-yellow-700'
                  : 'bg-gray-100 text-gray-700'
        }`}
      >
        {node.risk === 'SAFE' ? 'SAFE' : node.findings_count || 0}
      </span>
    ) : null;

  return (
    <div>
      <div
        className={`flex items-center py-1.5 px-2 cursor-pointer hover:bg-slate-100 transition-colors ${
          isSelected ? 'bg-indigo-50 text-indigo-700 font-medium' : 'text-slate-700'
        }`}
        style={{ paddingLeft: `${level * 12 + 8}px` }}
        onClick={handleToggle}
      >
        {isFolder ? (
          <span className="mr-1.5 text-slate-400">
            {isOpen ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </span>
        ) : (
          <span className="mr-1.5 ml-4" />
        )}

        {isFolder ? (
          <Folder size={16} className="mr-2 text-blue-400 shrink-0" />
        ) : (
          <File size={16} className="mr-2 text-slate-400 shrink-0" />
        )}

        <span className="text-sm truncate select-none">{node.name}</span>
        {riskBadge}
      </div>

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
  // 1. STATE ZA FILTRIRANJE
  // Shranjujemo trenutni iskalni niz in izbran nivo tveganja
  const [searchQuery, setSearchQuery] = useState('');
  const [riskFilter, setRiskFilter] = useState<string>('ALL');

  // 2. REKURZIVNA FUNKCIJA ZA FILTRIRANJE
  // Uporabimo useMemo, da se drevo ne preračunava ob vsakem renderju,
  // ampak samo, ko se spremeni originalna `data`, `searchQuery` ali `riskFilter`.
  const filteredTree = useMemo(() => {
    // Pomožna rekurzivna funkcija
    const filterNodes = (nodes: FileData[]): FileData[] => {
      return nodes.reduce<FileData[]>((acc, node) => {
        
        // SCENARIJ A: Trenutni node je MAPA (folder)
        if (node.type === 'folder') {
          if (!node.children) return acc;
          
          // Najprej rekurzivno filtriramo njene otroke
          const filteredChildren = filterNodes(node.children);
          
          // Mapo obdržimo in prikažemo SAMO, če po filtriranju vsebuje vsaj eno datoteko.
          // S tem preprečimo, da bi uporabnik videl prazne mape.
          if (filteredChildren.length > 0) {
            // Naredimo kopijo mape in ji dodelimo prefiltrirane otroke
            acc.push({ ...node, children: filteredChildren });
          }
        } 
        
        // SCENARIJ B: Trenutni node je DATOTEKA (file)
        else {
          // Preverimo, če se ime datoteke ujema z iskanim nizom (case-insensitive)
          const matchesSearch = node.name.toLowerCase().includes(searchQuery.toLowerCase());
          
          // Privzeto obravnavamo datoteke brez nastavljenega riska kot 'SAFE'
          const fileRisk = node.risk || 'SAFE';
          
          // Preverimo, če se risk datoteke ujema z izbranim filtrom (ali če je izbran 'ALL')
          const matchesRisk = riskFilter === 'ALL' || fileRisk === riskFilter;

          // Če datoteka ustreza OBOJEMU, jo dodamo v končni seznam
          if (matchesSearch && matchesRisk) {
            acc.push(node);
          }
        }
        
        return acc;
      }, []);
    };

    // Zaženemo rekurzijo nad celotnim drevesom
    return filterNodes(data);
  }, [data, searchQuery, riskFilter]);

  return (
    <div className="w-72 h-full bg-slate-50/50 border-r border-slate-200 flex flex-col shrink-0">
      <div className="p-4 border-b border-slate-200 space-y-4 bg-white">
        <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">
          Project Explorer
        </h2>

        {/* 3. UI KONTROLE ZA FILTRIRANJE */}
        <div className="space-y-3">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-2.5 top-2 text-slate-400" size={14} />
            <input
              type="text"
              placeholder="Search files..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 text-sm bg-slate-100 border border-transparent focus:border-indigo-300 focus:bg-white focus:ring-2 focus:ring-indigo-100 rounded-lg transition-all outline-none text-slate-700 placeholder:text-slate-400"
            />
          </div>

          {/* Risk Level Filter */}
          <div className="relative">
            <Filter className="absolute left-2.5 top-2 text-slate-400" size={14} />
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 text-sm bg-slate-100 border border-transparent focus:border-indigo-300 focus:bg-white focus:ring-2 focus:ring-indigo-100 rounded-lg transition-all outline-none text-slate-700 appearance-none cursor-pointer"
            >
              <option value="ALL">All Risk Levels</option>
              <option value="CRITICAL">Critical Only</option>
              <option value="HIGH">High Only</option>
              <option value="MEDIUM">Medium Only</option>
              <option value="LOW">Low Only</option>
              <option value="SAFE">Safe Only</option>
            </select>
          </div>
        </div>
      </div>

      {/* Glavni seznam map in datotek - Uporablja prefiltrirano drevo! */}
      <div className="flex-1 overflow-y-auto py-3">
        {filteredTree.length > 0 ? (
          filteredTree.map((node) => (
            <FileTreeNode
              key={node.id}
              node={node}
              level={0}
              onSelectFile={onSelectFile}
              selectedFileId={selectedFileId}
            />
          ))
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-slate-400 p-6 text-center space-y-2">
            <Search size={24} className="opacity-20 mb-2" />
            <p className="text-sm font-medium">No files found</p>
            <p className="text-xs opacity-70">
              Try adjusting your search query or risk filter.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};