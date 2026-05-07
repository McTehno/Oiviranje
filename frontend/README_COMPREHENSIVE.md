# SAST Analyzer - Frontend Application

A modern, interactive Static Application Security Testing (SAST) analyzer web application built with React, TypeScript, and Vite. The application provides a visual interface for exploring file systems, viewing code with syntax highlighting, and analyzing security vulnerabilities with detailed remediation guidance.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Getting Started](#getting-started)
- [Available Scripts](#available-scripts)
- [Component Architecture](#component-architecture)
- [Styling & Design](#styling--design)
- [Key Features](#key-features)

## 🎯 Project Overview

SAST Analyzer is a demonstration web stub that showcases a professional security analysis interface. It allows users to:

- Browse file systems using an interactive tree view
- View code with syntax highlighting
- Identify vulnerabilities embedded within code
- Analyze security statistics and vulnerability distributions
- Understand remediation strategies for identified issues

The application uses mock data to simulate a real SAST tool's functionality, making it ideal for UI/UX prototyping and demonstration purposes.

## 🛠 Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.2.5 | UI library for building interactive components |
| **TypeScript** | 6.0.2 | Static typing for JavaScript |
| **Vite** | 8.0.10 | Build tool and dev server with HMR |
| **TailwindCSS** | 3.4.19 | Utility-first CSS framework |
| **Framer Motion** | 12.38.0 | Animation and motion library |
| **React Syntax Highlighter** | 16.1.1 | Code syntax highlighting |
| **Recharts** | 3.8.1 | Charting library for data visualization |
| **Lucide React** | 1.14.0 | Icon library |
| **PostCSS** | 8.5.14 | CSS processing and transformation |
| **ESLint** | 10.2.1 | Code linting and quality checks |

## 📁 Project Structure

```
ninafrontend/
├── src/                           # Source code directory
│   ├── components/                # React components
│   │   ├── CodeViewer.tsx         # Code display with vulnerability highlighting
│   │   ├── Dashboard.tsx          # Security analytics dashboard
│   │   ├── FileTree.tsx           # File system tree navigation
│   │   └── VulnerabilityWidget.tsx # Vulnerability detail widget
│   ├── assets/                    # Static assets
│   ├── App.tsx                    # Root application component
│   ├── App.css                    # Application-wide styles
│   ├── main.tsx                   # React application entry point
│   ├── index.css                  # Global CSS styles
│   └── mockData.ts                # Mock data for demonstration
├── public/                        # Static public files
├── index.html                     # HTML entry point
├── package.json                   # Project dependencies and scripts
├── vite.config.ts                 # Vite build configuration
├── tailwind.config.js             # TailwindCSS configuration
├── tsconfig.json                  # TypeScript base configuration
├── tsconfig.app.json              # TypeScript application-specific config
├── tsconfig.node.json             # TypeScript Node.js config (for build tools)
├── eslint.config.js               # ESLint configuration
├── postcss.config.js              # PostCSS configuration
└── README.md                      # Original template README
```

## 📄 File Descriptions

### Configuration Files

#### `package.json`
Defines the project's metadata, dependencies, and npm scripts. Contains all required production and development dependencies, along with build and development commands.

**Key Scripts:**
- `npm run dev` - Start development server with HMR
- `npm run build` - TypeScript type checking + Vite production build
- `npm run lint` - Run ESLint to check code quality
- `npm run preview` - Preview production build

#### `vite.config.ts`
Vite build configuration file that sets up the React plugin for optimized development experience with fast HMR and efficient production builds.

#### `tailwind.config.js`
TailwindCSS configuration extending the default theme with custom colors:
- `background` - Main background white color
- `sidebar` - Left panel light gray
- `accent` - Highlight color for selections
- `danger` - Red color scheme for vulnerability severity

#### `tsconfig.json` / `tsconfig.app.json` / `tsconfig.node.json`
TypeScript configuration files:
- `tsconfig.json` - Base TypeScript settings
- `tsconfig.app.json` - Application-specific TypeScript rules
- `tsconfig.node.json` - Configuration for Node.js tools (Vite, ESLint)

#### `eslint.config.js`
ESLint configuration for enforcing code quality and style standards across the React TypeScript codebase.

#### `postcss.config.js`
PostCSS configuration for CSS processing, includes Autoprefixer for browser compatibility.

### Source Files

#### `src/index.css`
Global CSS styles applied to the entire application, including any CSS reset, base styles, and utility classes.

#### `src/App.css`
Application-specific CSS styles for the main App component and layout-related styling.

#### `src/main.tsx`
**Entry point for the React application.** This file:
- Imports React and ReactDOM
- Imports the main App component
- Renders the App component into the DOM root element
- Wraps the app in `<StrictMode>` for development warnings

#### `src/App.tsx`
**Root application component** that orchestrates the entire layout:
- Implements a three-section layout: header, main content, and footer
- Manages the selected file state using `useState`
- Renders the top navbar with branding
- Manages layout with Flexbox for the file tree, code viewer, and dashboard
- Connects all major components together

**Layout Structure:**
```
┌─ Header (Navbar) ─────────────────────┐
├─ FileTree │ CodeViewer ───────────────┤
├─ Dashboard ──────────────────────────┤
└──────────────────────────────────────┘
```

#### `src/mockData.ts`
**Mock data provider** containing:
- `Vulnerability` interface - Defines vulnerability data structure with line number, type, severity, description, and remediation
- `FileData` interface - Defines file/folder structure with hierarchical nesting support
- `mockFileSystem` - Sample file tree data simulating a code repository
- `statisticsData` - Aggregate security statistics for dashboard visualization

### Components

#### `src/components/FileTree.tsx`
**File system tree navigation component**

**Features:**
- Interactive tree view with expand/collapse functionality
- Displays folders and files with appropriate icons (from Lucide React)
- Supports hierarchical nesting with indentation based on tree depth
- Animated expand/collapse transitions using Framer Motion
- "Import Folder" button for UI completeness
- Click handler to select files for viewing
- Visual feedback for currently selected file
- Auto-expanded folders on initial load

**Props:**
- `data: FileData[]` - Array of files and folders to display
- `onSelectFile: (file: FileData) => void` - Callback when a file is selected
- `selectedFileId: string | null` - Currently selected file ID for highlighting

#### `src/components/CodeViewer.tsx`
**Code display component with syntax highlighting and vulnerability visualization**

**Features:**
- Displays code with syntax highlighting using React Syntax Highlighter
- Supports multiple programming languages
- Line numbering for easy reference
- Inline vulnerability widgets displayed below affected code lines
- Visual highlighting of vulnerable lines with red background and left border
- Responsive scrolling for large code files
- Empty state when no file is selected
- Uses the "coy" syntax highlighting theme for clarity

**Key Functionality:**
- Maps vulnerabilities to line numbers for efficient lookup
- Renders custom line properties for highlighting vulnerable lines
- Integrates VulnerabilityWidget components inline with code

**Props:**
- `file: FileData | null` - Selected file to display

#### `src/components/VulnerabilityWidget.tsx`
**Detailed vulnerability information display component**

**Features:**
- Displays vulnerability type, severity, description, and remediation
- Color-coded severity levels with appropriate icons:
  - **Critical** - Red with shield alert icon
  - **High** - Orange with alert triangle
  - **Medium** - Yellow with alert triangle
  - **Low** - Green with info icon
- Animated appearance using Framer Motion
- Organized layout with distinct sections for different information types
- Remediation code displayed in a formatted code block

**Props:**
- `vulnerability: Vulnerability` - Vulnerability data to display

#### `src/components/Dashboard.tsx`
**Security analytics and statistics dashboard**

**Features:**
- Expandable/collapsible dashboard section for space efficiency
- Three-column analytics view:
  1. **Vulnerabilities by Type** - Bar chart showing count of each vulnerability type
  2. **Severity Breakdown** - Donut/pie chart showing severity distribution
  3. **Top Exploitable Files** - List of files with most issues, displayed with progress bars
- Uses Recharts for data visualization
- Animated expand/collapse transitions
- Color-coded severity indicators in the exploitable files list
- Responsive tooltips on chart hover

**Features:**
- Smooth animations using Framer Motion for expand/collapse
- Accessibility considerations with proper contrast and icon usage
- Mobile-responsive layout adaptable to different screen sizes

## 🚀 Getting Started

### Prerequisites
- Node.js (v18 or higher recommended)
- npm or yarn package manager

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd ninafrontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   Navigate to `http://localhost:5173` (Vite's default port)

### Development Workflow

1. **Edit source files** in `src/` directory
2. **Changes automatically reload** thanks to Vite's HMR (Hot Module Replacement)
3. **Run linting** to catch code quality issues:
   ```bash
   npm run lint
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

## 📜 Available Scripts

### `npm run dev`
Starts the Vite development server with HMR. The application will automatically reload on code changes.

**Command:** `vite`

### `npm run build`
Builds the application for production. First runs TypeScript type checking, then creates an optimized production build.

**Command:** `tsc -b && vite build`

### `npm run lint`
Runs ESLint to check for code quality issues and style violations.

**Command:** `eslint .`

### `npm run preview`
Locally preview the production build before deployment. Useful for testing the optimized version.

**Command:** `vite preview`

## 🏗 Component Architecture

### Data Flow Diagram

```
App (Root)
├── FileTree
│   └── FileTreeNode (Recursive)
│       └── onSelectFile callback
├── CodeViewer
│   └── VulnerabilityWidget
│       └── Displays vulnerability details
└── Dashboard
    └── Statistical charts and exploitable files
```

### State Management

- **App Component** manages the selected file state
- Child components receive props and don't maintain global state
- Simple and straightforward prop-drilling pattern (suitable for this application size)

### Type Safety

All components use TypeScript interfaces and types:
- `FileData` - Defines file/folder structure
- `Vulnerability` - Defines vulnerability information
- Component-specific prop interfaces ensure type safety

## 🎨 Styling & Design

### Design System

The application uses a clean, professional design with:

**Color Palette:**
- **White** - Primary background
- **Light Gray (#F3F4F6)** - Sidebar and secondary backgrounds
- **Blue (#6366F1)** - Primary accent and interactive elements
- **Red (#EF4444)** - Critical vulnerabilities and errors
- **Orange (#F97316)** - High-severity vulnerabilities
- **Yellow (#FACC15)** - Medium-severity vulnerabilities
- **Green (#22C55E)** - Low-severity vulnerabilities

**Typography:**
- Font Family: Inter, Roboto, sans-serif
- Monospace: JetBrains Mono, Fira Code (for code display)

**Components:**
- Rounded corners (4-6px border radius)
- Subtle shadows for depth
- Smooth transitions and animations

### Responsive Design

The application uses Tailwind CSS for responsive layout:
- Flexbox for flexible layouts
- Grid for dashboard analytics
- Responsive padding and margins
- Mobile-friendly navigation

## ✨ Key Features

### 1. File Tree Navigation
- Browse hierarchical file structures
- Expand/collapse folders with visual feedback
- Select files to view
- Icon-based file type indication

### 2. Code Viewer
- Syntax highlighting for multiple languages
- Line numbering
- Responsive scrolling
- Inline vulnerability indicators

### 3. Vulnerability Analysis
- Inline vulnerability display
- Detailed severity classification
- Actionable remediation guidance
- Color-coded highlighting

### 4. Security Dashboard
- Visual analytics with charts
- Vulnerability type distribution
- Severity breakdown overview
- File risk assessment
- Collapsible interface for space efficiency

### 5. User Experience
- Smooth animations and transitions
- Clear visual hierarchy
- Intuitive navigation
- Professional branding

## 📝 Notes

- This application uses **mock data** for demonstration purposes
- The component structure is designed to be easily extendable
- All components are functional components with hooks
- TypeScript provides strong type safety throughout
- The application follows React best practices and modern patterns

## 🔧 Future Enhancement Possibilities

- Real backend API integration
- File upload functionality
- Additional vulnerability analysis types
- Export reports functionality
- Dark mode support
- Advanced filtering and search
- User authentication
- Multi-project management
- Custom remediation workflows

---

**Built with ❤️ using React, TypeScript, and Vite**
