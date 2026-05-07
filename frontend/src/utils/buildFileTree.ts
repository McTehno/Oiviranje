import type { FileData } from '../types/analysis';

/*
  Backend vrne datoteke kot seznam poti.
  Ta funkcija jih pretvori v drevesno strukturo za FileTree.
*/
export function buildFileTree(files: FileData[]): FileData[] {
  const root: FileData[] = [];

  files.forEach((file) => {
    // Pot razdelimo na dele, npr. "src/db/test.py" -> ["src", "db", "test.py"]
    const parts = file.path.split(/[\\/]/);
    let currentLevel = root;

    parts.forEach((part, index) => {
      const currentPath = parts.slice(0, index + 1).join('/');
      const isFile = index === parts.length - 1;

      // Preverimo, ali mapa/datoteka na tem nivoju že obstaja
      let existing = currentLevel.find((item) => item.path === currentPath);

      // Če ne obstaja, ustvarimo nov node
      if (!existing) {
        existing = {
          id: currentPath,
          name: part,
          path: currentPath,
          type: isFile ? 'file' : 'folder',
          children: isFile ? undefined : [],
        };

        currentLevel.push(existing);
      }

      if (isFile) {
        // Pri datoteki ohranimo tudi content, language, risk, findings_count itd.
        Object.assign(existing, file);
      } else {
        // Pri mapi se premaknemo en nivo globlje
        currentLevel = existing.children!;
      }
    });
  });

  return root;
}