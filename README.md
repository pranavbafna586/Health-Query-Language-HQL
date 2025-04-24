# Health Query Language (HQL)

A domain-specific language (DSL) for healthcare workers and researchers to query patient data using simple, human-readable commands.

## Overview

HQL is designed to make it easy for healthcare professionals with limited technical skills to query and analyze patient data. The language provides simple, intuitive syntax for common healthcare data operations.

## Features

- Simple, English-like syntax
- Three main command types:
  - **FIND**: Retrieve patients matching specific criteria
  - **SHOW**: Calculate aggregated metrics (averages, counts, etc.)
  - **ALERT**: Identify patients that require attention
- Support for compound conditions with AND/OR
- Interactive shell for exploratory data analysis
- Web-based user interface for easy interaction

## Installation

1. Clone this repository or download the source code.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Sample Data

The project includes a sample dataset of patient records in `data/patients.csv`. The data schema includes:

- patient_id
- name
- age
- gender
- blood_pressure (format: "120/80")
- heart_rate
- oxygen_level
- diabetes (yes/no)
- hypertension (yes/no)
- asthma (yes/no)

You can replace this with your own dataset, following the same schema.

## Usage

### Web Interface

Start the web interface for the most user-friendly experience:

```bash
python web_app.py
```

This will launch a web server at http://localhost:5000 where you can:
- Execute HQL queries through a visual interface
- View patient statistics
- Browse example queries
- See query results in a formatted display

### Interactive Command Line Mode

Run the HQL interactive shell:

```bash
python run_hql.py -i
```

Or simply:

```bash
python launch_hql.py --web
```

This will launch a web server at http://localhost:5000 where you can:
- Execute HQL queries through a visual interface
- View patient statistics
- Browse example queries
- See query results in a formatted display
- Start the interactive command line mode for direct query input

### Single Query Mode

Execute a single HQL query:

```bash
python run_hql.py -q "FIND patients WHERE age > 60"
```

### Using a Custom Dataset

You can specify a custom dataset:

```bash
python run_hql.py -d path/to/your/data.csv
```

## HQL Syntax and Examples

### FIND Command

Retrieves patients matching specific criteria.

```
FIND patients WHERE age > 60
FIND patients WHERE blood_pressure > 140
FIND patients WHERE diabetes = yes AND age > 50
```

### SHOW Command

Calculates aggregated metrics on patient data.

```
SHOW average heart_rate FOR patients WITH diabetes = yes
SHOW count patient_id FOR patients WITH age > 70
SHOW max blood_pressure FOR patients WITH hypertension = yes
```

### ALERT Command

Identifies patients requiring attention based on specific criteria.

```
ALERT IF oxygen_level < 90
ALERT IF heart_rate > 100
```

## Extending HQL

The HQL system is modular and extensible:

1. **Lexer** (`lexer.py`): Tokenizes the input commands
2. **Parser** (`parser.py`): Transforms tokens into an abstract syntax tree (AST)
3. **Interpreter** (`interpreter.py`): Executes the AST on the patient data
4. **Engine** (`hql.py`): Orchestrates the overall process and formats results
5. **Web Frontend** (`web_app.py`): Provides a browser-based user interface

You can extend the language by modifying these components.

## Technical Implementation

This project demonstrates key compiler/interpreter concepts:
- Lexical analysis (tokenization)
- Parsing and grammar definition
- Abstract syntax tree (AST) generation
- Interpretation and execution

The implementation uses Python with the following libraries:
- PLY (Python Lex-Yacc) for lexing and parsing
- Pandas for data operations
- NumPy for numerical operations
- Flask for the web interface

## License

This project is released under the MIT License.
