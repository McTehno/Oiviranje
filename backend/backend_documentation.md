# Backend Documentation

This document provides a comprehensive overview of the backend architecture and functionality of the SAST (Static Application Security Testing) Analyzer tool.

## Overview

The backend is a Python-based static code analysis tool designed to detect injection vulnerabilities in web applications. It supports multiple programming languages (Python, JavaScript, PHP) and can identify four types of injection attacks:

1. **SQL Injection** - Database query manipulation through user input
2. **HQL/ORM Injection** - Hibernate Query Language injection vulnerabilities
3. **Command Injection** - Operating system command execution through user input
4. **MongoDB Injection** - NoSQL database operator injection

The system uses taint tracking analysis to follow user input through the code and detect when it reaches dangerous operations without proper sanitization.

## Architecture Overview

The backend follows a modular architecture with clear separation of concerns:

```
backend/
├── app/                 # Application entry points and utilities
├── detectors/           # Vulnerability detection logic
├── languages/           # Language-specific parsing and analysis
├── models/              # Data models and enums
├── pipeline/            # Analysis orchestration
├── reporting/           # Report generation
├── rules/               # Detection rules
├── examples/            # Sample vulnerable code
└── test/                # Test cases
```

## Core Components

### 1. Application Layer (`app/`)

#### `main.py`
**Purpose**: Command-line interface entry point for single-file analysis.

**Functionality**:
- Parses command-line arguments using `cli.py`
- Reads target file content
- Initializes `Analyzer` from the pipeline
- Runs analysis with specified language and database
- Generates and displays security report

**Usage**: `python main.py --file <path> --lang <language> --db <database>`

#### `api.py`
**Purpose**: FastAPI-based REST API for web interface integration.

**Key Features**:
- Project analysis via ZIP file uploads
- GitHub repository analysis
- CORS middleware for frontend communication
- Temporary workspace management for analysis
- UUID-based scan identification

**Endpoints**:
- `GET /` - Health check
- `POST /analyze-project` - Analyze uploaded ZIP project
- `POST /analyze-github` - Analyze GitHub repository

#### `cli.py`
**Purpose**: Command-line argument parsing and validation.

**Supported Arguments**:
- `--file`: Path to file for analysis
- `--lang`: Programming language (python, javascript, php)
- `--db`: Database type (mysql, postgresql, mongodb, etc.)

#### `config.py`
**Purpose**: Application configuration settings.

#### `file_utils.py`
**Purpose**: File system utilities and language detection.

**Key Functions**:
- `detect_language_from_file()` - Detects language from file extension
- `is_supported_code_file()` - Checks if file type is supported for analysis
- Directory filtering logic

#### `github_utils.py`
**Purpose**: GitHub integration utilities.

**Functionality**:
- Repository ZIP download
- Archive extraction
- Repository URL parsing

#### `gui.py`
**Purpose**: Graphical user interface (if implemented).

### 2. Pipeline Layer (`pipeline/`)

#### `analyzer.py`
**Purpose**: Core analysis orchestration engine.

**Responsibilities**:
- Language-specific parser selection
- Code parsing into structured format
- Vulnerability detection coordination
- Risk assessment and scoring
- Result aggregation

**Supported Languages**: Python, JavaScript, PHP

#### `project_analyzer.py`
**Purpose**: Multi-file project analysis coordinator.

**Functionality**:
- Recursive directory traversal
- File filtering (ignores common directories like node_modules, .git)
- Individual file analysis aggregation
- Cross-file finding correlation
- Database configuration mapping per file

### 3. Detection Layer (`detectors/`)

#### `injection_detector.py`
**Purpose**: Main detector coordinator that orchestrates all injection detection types.

**Architecture**:
- Factory pattern for language-specific taint trackers
- Delegates to specialized detectors (SQL, HQL, Command, MongoDB)
- Coordinates taint analysis across the codebase

#### `sql_detector.py`
**Purpose**: SQL injection vulnerability detection.

**Detection Methods**:
- String concatenation in SQL queries
- Raw query execution patterns
- Parameterized query validation

#### `hql_detector.py`
**Purpose**: Hibernate Query Language (HQL) injection detection.

**Focus**: ORM query manipulation vulnerabilities

#### `command_detector.py`
**Purpose**: Operating system command injection detection.

**Detection Targets**:
- `os.system()` calls
- `subprocess` module usage
- Shell command execution patterns

#### `mongodb_detector.py`
**Purpose**: MongoDB/NoSQL injection detection.

**Detection Methods**:
- Operator injection in MongoDB queries
- `$where` clause vulnerabilities
- JavaScript execution in database context

#### `base.py`
**Purpose**: Base detector class with common functionality.

#### `common_rules.py`
**Purpose**: Shared detection rules and patterns.

#### `pattern_utils.py`
**Purpose**: Utility functions for pattern matching and analysis.

### 4. Language Support (`languages/`)

#### Base Components
- `base_parser.py`: Abstract base parser class
- `base_taint_tracker.py`: Abstract taint tracking implementation

#### Language-Specific Modules

Each language has three components:

**Parser** (`parser.py`):
- Splits code into individual lines
- Creates `CodeLine` objects with line numbers and content
- Language-specific syntax handling

**Taint Tracker** (`taint_tracker.py`):
- Implements data flow analysis
- Tracks user input propagation through variables
- Identifies dangerous sinks (database queries, command execution)

**Rules** (`rules.py`):
- Language-specific vulnerability patterns
- Syntax-aware detection rules
- Context-sensitive analysis

**Supported Languages**:
- **Python**: Full taint tracking, AST-based analysis
- **JavaScript**: DOM-based and Node.js patterns
- **PHP**: Web application security focus

### 5. Data Models (`models/`)

#### `finding.py`
**Purpose**: Represents a detected vulnerability.

**Attributes**:
- `line`: Line number where vulnerability occurs
- `type`: Type of finding (CONCAT, EXEC, RAW_QUERY, etc.)
- `code`: Code snippet containing the vulnerability
- `variables`: Variables involved in the vulnerability
- `language`: Programming language
- `file_path`: Relative path in project
- `database`: Target database type
- `risk`: Risk level (SAFE, LOW, MEDIUM, HIGH, CRITICAL)
- `attack_type`: Type of attack (SQL_INJECTION, HQL_INJECTION, etc.)
- `description`: Human-readable description
- `recommendation`: Suggested fix

#### `result.py`
**Purpose**: Analysis result container.

**Contains**:
- List of all findings
- Total count of findings
- Overall risk assessment
- Security score (0-100)
- Detected vulnerability scenarios

#### `code_line.py`
**Purpose**: Represents a single line of code.

**Attributes**:
- `number`: Line number
- `content`: Code content
- `language`: Programming language

#### `enums.py`
**Purpose**: Centralized enumeration definitions.

**Enums**:
- `RiskLevel`: SAFE, LOW, MEDIUM, HIGH, CRITICAL
- `AttackType`: NONE, SQL_INJECTION, HQL_INJECTION, COMMAND_INJECTION, MONGODB_INJECTION
- `FindingType`: UNKNOWN, CONCAT, EXEC, RAW_QUERY, MONGODB_INJECTION

### 6. Reporting (`reporting/`)

#### `report.py`
**Purpose**: Report generation and formatting.

**Features**:
- Text-based security reports
- Finding categorization by risk level
- Scenario-based summaries
- Statistical overview (total findings, risk score)

### 7. Rules (`rules/`)

#### `injection_rules.py`
**Purpose**: Centralized injection vulnerability patterns and rules.

**Contains**:
- Common injection patterns
- Language-agnostic detection rules
- Pattern matching logic

### 8. Examples (`examples/`)

Contains sample vulnerable code for testing and demonstration:

- `javascript/`: JavaScript injection examples
- `php/`: PHP web application vulnerabilities
- `python/`: Python injection scenarios

Each subdirectory contains:
- Individual scenario files
- Comprehensive test files with multiple vulnerabilities

### 9. Testing (`test/`)

Test suite with:
- Unit tests for detectors
- Integration tests for pipeline
- Sample vulnerable code for validation
- Test cases for each supported language

## Analysis Flow

1. **Input Processing**: Code is received via CLI, API, or file upload
2. **Language Detection**: File extension or explicit parameter determines language
3. **Parsing**: Code is split into lines and structured as `CodeLine` objects
4. **Taint Tracking**: User input sources are identified and tracked through variable assignments
5. **Detection**: Specialized detectors analyze code for injection patterns
6. **Risk Assessment**: Findings are categorized by risk level and attack type
7. **Reporting**: Results are formatted into human-readable security reports

## Supported File Types

- **Python**: `.py`
- **JavaScript**: `.js`, `.ts`, `.jsx`, `.tsx`
- **PHP**: `.php`

## Database Support

- MySQL
- PostgreSQL
- MongoDB
- SQLite
- Oracle
- Microsoft SQL Server

## Security Analysis Types

### Taint Tracking
- Follows user input from sources (request parameters, user input)
- Tracks data flow through variable assignments
- Identifies when tainted data reaches dangerous sinks

### Pattern Matching
- Recognizes common vulnerable patterns
- String concatenation in queries
- Direct command execution
- Raw database operations

### Context-Aware Analysis
- Language-specific syntax understanding
- Framework-aware detection (Django, Flask, Express, Laravel)
- Database-specific query patterns

## Output Formats

- **Console Reports**: Text-based summaries for CLI usage
- **JSON API Responses**: Structured data for web interfaces
- **Risk Scoring**: 0-100 security score based on findings
- **Scenario Detection**: Identifies which vulnerability types are present

## Integration Points

- **Frontend**: REST API integration with React/TypeScript dashboard
- **GitHub**: Direct repository analysis capability
- **CI/CD**: Command-line interface for automated security testing
- **IDE**: Potential VS Code extension integration

This modular architecture allows for easy extension to new languages, detection types, and output formats while maintaining clean separation of concerns.