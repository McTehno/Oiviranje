export interface Vulnerability {
  line: number;
  type: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  description: string;
  remediation: string;
}

export interface FileData {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'folder';
  language?: string;
  content?: string;
  children?: FileData[];
  vulnerabilities?: Vulnerability[];
}

export const mockFileSystem: FileData[] = [
  {
    id: '1',
    name: 'app',
    path: '/app',
    type: 'folder',
    children: [
      {
        id: '2',
        name: 'api',
        path: '/app/api',
        type: 'folder',
        children: [
          {
            id: '3',
            name: 'upload.php',
            path: '/app/api/upload.php',
            type: 'file',
            language: 'php',
            content: `<?php
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
    echo "The file ". htmlspecialchars( basename( $_FILES["fileToUpload"]["name"])). " has been uploaded.";
    
    // Process image
    $cmd = "convert " . $target_file . " -resize 100x100 " . $target_file . "_thumb.jpg";
    shell_exec($cmd);
} else {
    echo "Sorry, there was an error uploading your file.";
}
?>`,
            vulnerabilities: [
              {
                line: 10,
                type: 'Command Injection',
                severity: 'Critical',
                description: 'Unsanitized user input ($target_file derived from filename) passed directly to shell_exec().',
                remediation: 'Use escapeshellarg() or escapeshellcmd() to sanitize input before passing to shell_exec. Alternatively, use a built-in image processing library like GD or Imagick.'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: '4',
    name: 'src',
    path: '/src',
    type: 'folder',
    children: [
      {
        id: '5',
        name: 'database',
        path: '/src/database',
        type: 'folder',
        children: [
          {
            id: '6',
            name: 'db.py',
            path: '/src/database/db.py',
            type: 'file',
            language: 'python',
            content: `import sqlite3
import os

def get_user_by_name(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Insecure query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    
    result = cursor.fetchall()
    conn.close()
    return result
`,
            vulnerabilities: [
              {
                line: 9,
                type: 'SQL Injection',
                severity: 'High',
                description: 'Direct string concatenation in a SQL query allows attackers to inject malicious SQL statements.',
                remediation: 'Use parameterized queries / prepared statements provided by the database driver. Ex: cursor.execute("SELECT * FROM users WHERE username = ?", (username,))'
              }
            ]
          },
          {
            id: '7',
            name: 'server.js',
            path: '/src/database/server.js',
            type: 'file',
            language: 'javascript',
            content: `const express = require('express');
const MongoClient = require('mongodb').MongoClient;
const app = express();

app.use(express.json());

app.post('/api/search', async (req, res) => {
    const client = await MongoClient.connect('mongodb://localhost:27017');
    const db = client.db('myapp');
    
    const userRole = req.body.role;
    
    // Insecure NoSQL query
    const results = await db.collection('users').find({
        $where: "this.role == '" + userRole + "'"
    }).toArray();
    
    res.json(results);
    client.close();
});

app.listen(3000);`,
            vulnerabilities: [
              {
                line: 15,
                type: 'MongoDB NoSQL Injection',
                severity: 'Critical',
                description: 'Usage of the $where operator with unescaped string concatenation allows execution of arbitrary JavaScript on the database server.',
                remediation: 'Avoid using $where operator. If necessary, use proper query operators like db.collection("users").find({ role: userRole }).'
              }
            ]
          }
        ]
      }
    ]
  },
  {
    id: '8',
    name: 'config',
    path: '/config',
    type: 'folder',
    children: [
      {
        id: '9',
        name: 'settings.yml',
        path: '/config/settings.yml',
        type: 'file',
        language: 'yaml',
        content: `server:
  port: 8080
  debug: false
database:
  user: admin
  password: "supersecretpassword123"
`
      }
    ]
  }
];

export const statisticsData = {
  vulnerabilitiesByType: [
    { name: 'SQL Injection', count: 12 },
    { name: 'Command Injection', count: 5 },
    { name: 'MongoDB Injection', count: 8 },
    { name: 'XSS', count: 15 },
  ],
  severityBreakdown: [
    { name: 'Critical', value: 8, color: '#DC2626' },
    { name: 'High', value: 14, color: '#F97316' },
    { name: 'Medium', value: 10, color: '#FCD34D' },
    { name: 'Low', value: 18, color: '#34D399' },
  ],
  topExploitableFiles: [
    { name: 'api/upload.php', count: 4, severity: 'Critical' },
    { name: 'src/database/server.js', count: 3, severity: 'High' },
    { name: 'src/database/db.py', count: 2, severity: 'High' },
    { name: 'auth/login.js', count: 2, severity: 'Medium' },
  ]
};
