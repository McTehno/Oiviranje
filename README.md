# Oiviranje
SQL Injection Analyzer
Opis
Orodje za statično analizo kode, ki zazna:
SQL Injection
HQL Injection
Command Injection

Podprti jeziki:
Python
JavaScript
PHP

Kako deluje
Parser analizira kodo
Detector prepozna nevarne vzorce
Pipeline oceni tveganje
Report vrne rezultat

## Project Structure

```text
README.md
app/
	cli.py
	config.py
	main.py
detectors/
	base.py
	injection_detector.py
examples/
	scenario1_sql.py
	scenario2_hql.java
	scenario3_cmd.java
models/
	enums.py
	finding.py
	result.py
parsers/
	base.py
	js_parser.py
	php_parser.py
	python_parser.py
pipeline/
	analyzer.py
	pipeline.py
reporting/
	report.py
rules/
	injection_rules.py
scoring/
utils/
```

## Directory Overview

### `app/`
Application-level entry points and configuration live here.

- `cli.py` is intended for command-line interaction.
- `config.py` stores application settings and runtime configuration.
- `main.py` is the main startup module.

### `detectors/`
This folder contains detector implementations.

- `base.py` is the shared detector interface or abstraction.
- `injection_detector.py` is the detector focused on injection-related findings.

### `examples/`
Sample inputs for testing and demonstration.

- `scenario1_sql.py` represents a SQL-oriented scenario.
- `scenario2_hql.java` represents a Java/HQL-oriented scenario.
- `scenario3_cmd.java` represents a command-execution scenario.

### `models/`
Data structures used to represent analysis output.

- `enums.py` stores shared enumerations.
- `finding.py` defines the finding model.
- `result.py` defines the final analysis result model.

### `parsers/`
Language-specific parsing logic.

- `base.py` defines the parser interface.
- `js_parser.py` handles JavaScript source.
- `php_parser.py` handles PHP source.
- `python_parser.py` handles Python source.

### `pipeline/`
Core orchestration for analyzing input and moving data through the system.

- `analyzer.py` is the analysis stage.
- `pipeline.py` coordinates the end-to-end flow.

### `reporting/`
Output formatting and report generation.

- `report.py` is intended to turn analysis results into a human-readable report.

### `rules/`
Rule definitions used by detectors and analyzers.

- `injection_rules.py` contains the rules relevant to injection detection.

### `scoring/`
Placeholder for scoring or severity-ranking logic.

### `utils/`
Shared helper functions and small reusable utilities.

## Current State

Several modules in this repository are still empty placeholders. The structure is already in place, but the implementation is not yet complete. This README therefore describes the intended architecture rather than a fully working application flow.

## Suggested Next Step

When the implementation is added, this README can be expanded with installation instructions, usage examples, and a short explanation of the analysis pipeline.