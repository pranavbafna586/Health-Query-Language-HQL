# Health Query Language (HQL): Bridging Healthcare and Data Analysis

## Project Overview

Health Query Language (HQL) is a specialized domain-specific language designed to bridge the gap between healthcare professionals and patient data analysis. This project addresses the critical need for healthcare workers to access, query, and analyze patient data without requiring extensive technical knowledge or programming experience.

## The Problem HQL Solves

Healthcare professionals face several challenges when working with patient data:

1. **Technical Barrier**: Most healthcare workers lack programming skills but need to analyze patient data.
2. **Complex Query Requirements**: Medical queries often involve complex conditions and specialized healthcare metrics.
3. **Time Constraints**: Medical staff need quick answers without writing complex SQL or programming code.
4. **Data Accessibility**: Important insights remain locked in data that requires technical expertise to access.
5. **Alert Automation**: Need for automated monitoring of critical patient parameters.

## How HQL Helps the Healthcare Industry

The Health Query Language addresses these challenges by:

1. **Intuitive, English-Like Syntax**: HQL uses commands that mirror how healthcare professionals think and speak about patient data.
2. **Domain-Specific Focus**: Built specifically for healthcare data patterns and use cases.
3. **Multiple Interfaces**: Offers both a web-based interface and command-line tools to suit different user preferences.
4. **Real-Time Alerting**: Enables setting up automated monitoring of patient vital signs and health indicators.
5. **Data Visualization**: Presents results in easy-to-understand formats appropriate for clinical settings.

## Technical Implementation

HQL is implemented as a complete language processing system, consisting of:

1. **Lexical Analysis (Lexer)**: Breaks down HQL queries into meaningful tokens.
2. **Syntax Analysis (Parser)**: Validates query structure and builds an Abstract Syntax Tree (AST).
3. **Semantic Processing (Interpreter)**: Executes the query against patient data.
4. **Execution Engine**: Orchestrates the entire process and formats results for display.
5. **Web & CLI Interfaces**: Provides multiple ways to interact with the system.

### Dry Run Example: Processing an HQL Query

Let's trace how HQL processes the following query:

```
FIND patients WHERE age > 60 AND blood_pressure > 140
```

#### Step 1: Lexical Analysis (Lexer)

The lexer breaks down the query into tokens:

```
[('FIND', 'FIND'),
 ('PATIENTS', 'patients'),
 ('WHERE', 'WHERE'),
 ('IDENTIFIER', 'age'),
 ('GT', '>'),
 ('NUMBER', '60'),
 ('AND', 'AND'),
 ('IDENTIFIER', 'blood_pressure'),
 ('GT', '>'),
 ('NUMBER', '140')]
```

Each token consists of a token type and value, allowing the parser to understand the structure.

#### Step 2: Syntax Analysis (Parser)

The parser validates the query structure and builds an Abstract Syntax Tree (AST):

```
{
  "command": "FIND",
  "target": "patients",
  "condition": {
    "type": "binary_operation",
    "operator": "AND",
    "left": {
      "type": "comparison",
      "operator": ">",
      "left": "age",
      "right": 60
    },
    "right": {
      "type": "comparison",
      "operator": ">",
      "left": "blood_pressure",
      "right": 140
    }
  }
}
```

This tree represents the logical structure of the query, making it easier for the interpreter to process.

#### Step 3: Semantic Processing (Interpreter)

The interpreter executes the query against patient data:

1. Loads the patient data into a pandas DataFrame
2. Translates the AST into a pandas filter expression: `(df['age'] > 60) & (df['blood_pressure'] > 140)`
3. Applies the filter to retrieve matching patients
4. Returns the filtered dataset containing patients who are over 60 with blood pressure above 140

#### Step 4: Result Presentation

The execution engine formats and presents the results based on the interface being used:

- Command-line: Tabular display of matching patients
- Web interface: Interactive table with visualization options
- API mode: Structured JSON response

This pipeline ensures that healthcare professionals can write intuitive queries that are properly processed and return meaningful results.

## Features of the project

1. **Natural Language-Like Syntax**: Queries written in HQL closely resemble English sentences, making them intuitive for healthcare professionals.
2. **Specialized Healthcare Commands**: Purpose-built commands for medical data analysis and patient monitoring.
3. **Robust Data Filtering**: Complex conditional expressions to identify specific patient cohorts.
4. **Statistical Analysis**: Built-in aggregations (average, count, max, min) for healthcare metrics.
5. **Multi-platform Support**: Works through web browsers, command line, or integrated into other systems.
6. **Visualization Capabilities**: Presents query results as charts and graphs for better interpretation.
7. **Real-time Monitoring**: Continuous evaluation of patient data against alert conditions.
8. **Extensible Framework**: Modular architecture that allows for adding new commands and capabilities.
9. **CSV Data Support**: Works with standard CSV files containing patient records.
10. **Error Handling**: User-friendly error messages specific to healthcare query contexts.

## Key Features

### 1. Three Core Command Types

- **FIND**: Retrieves patients matching specific clinical criteria

  ```
  FIND patients WHERE age > 60 AND blood_pressure > 140
  ```

- **SHOW**: Calculates and displays aggregate health metrics

  ```
  SHOW average heart_rate FOR patients WITH diabetes = yes
  ```

- **ALERT**: Sets up automatic monitoring for critical health parameters
  ```
  ALERT IF oxygen_level < 90
  ```

### 2. Multiple User Interfaces

- **Web Interface**: Browser-based UI with sample queries, visualization, and statistics dashboard
- **Interactive CLI**: Command-line shell for direct query input
- **Script Integration**: API for embedding HQL in other healthcare applications

### 3. Healthcare-Specific Analytics

- Support for vital signs monitoring (blood pressure, heart rate, oxygen levels)
- Medical condition filtering (diabetes, hypertension, asthma)
- Age and demographic-based analysis

## Real-World Applications

HQL can be deployed in various healthcare settings to:

1. **Clinical Decision Support**: Help physicians identify patients matching specific clinical profiles.
2. **Patient Monitoring**: Set up automated alerts for patients with concerning vital signs.
3. **Population Health Management**: Analyze trends across patient populations with specific conditions.
4. **Research Studies**: Quickly identify cohorts of patients matching study criteria.
5. **Resource Allocation**: Determine how many patients require specific interventions or treatments.

## Technical Architecture

HQL's architecture follows the classic compiler/interpreter design pattern:

1. **Lexer (`lexer.py`)**: Uses PLY (Python Lex-Yacc) to tokenize HQL queries
2. **Parser (`parser.py`)**: Transforms tokens into an Abstract Syntax Tree (AST)
3. **Interpreter (`interpreter.py`)**: Executes the AST against patient data (pandas DataFrame)
4. **Engine (`hql.py`)**: Coordinates the overall execution process
5. **Web App (`web_app.py`)**: Flask-based web interface
6. **CLI (`run_hql.py`)**: Command-line interface
7. **Launcher (`launch_hql.py`)**: Entry point to select interface mode

## Installation and Setup

1. Clone the repository or download the source code
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the application:
   ```bash
   python launch_hql.py --web
   ```

## Use Cases with Examples

### Case Study 1: Cardiovascular Risk Assessment

A cardiologist needs to identify elderly patients with high blood pressure:

```
FIND patients WHERE age > 60 AND blood_pressure > 140
```

HQL returns a list of at-risk patients for follow-up.

### Case Study 2: Diabetes Management

A diabetes educator wants to analyze the average heart rate for diabetic patients:

```
SHOW average heart_rate FOR patients WITH diabetes = yes
```

The result provides insight into potential cardiovascular effects of diabetes.

### Case Study 3: Respiratory Monitoring

A respiratory therapist needs to be alerted when any patient's oxygen level drops below a critical threshold:

```
ALERT IF oxygen_level < 90
```

This creates an automatic monitoring system for at-risk patients.

## Why HQL Matters for Healthcare

HQL represents a significant advancement in healthcare informatics by:

1. **Democratizing Data Access**: Enabling non-technical staff to gain insights from patient data
2. **Improving Clinical Workflows**: Reducing the time between having a question and getting an answer
3. **Enhancing Patient Care**: Facilitating data-driven clinical decision making
4. **Supporting Evidence-Based Practice**: Making it easier to analyze outcomes across patient populations

## Future Potential

The HQL project could expand to include:

1. **EMR Integration**: Direct connection to Electronic Medical Record systems
2. **Advanced Visualization**: More sophisticated charting and data visualization
3. **Machine Learning**: Integration with predictive analytics and AI models
4. **Mobile Interface**: Smartphone access for on-the-go healthcare professionals
5. **Natural Language Processing**: Ability to ask questions in completely natural language

## Extending HQL

The HQL system is modular and extensible:

1. **Lexer** (`lexer.py`): Tokenizes the input commands
2. **Parser** (`parser.py`): Transforms tokens into an abstract syntax tree (AST)
3. **Interpreter** (`interpreter.py`): Executes the AST on the patient data
4. **Engine** (`hql.py`): Orchestrates the overall process and formats results
5. **Web Frontend** (`web_app.py`): Provides a browser-based user interface

You can extend the language by modifying these components.

## Technical Requirements

- Python 3.6+
- Dependencies:
  - pandas: Data processing and manipulation
  - ply: Lexical analysis and parsing
  - flask: Web interface
  - matplotlib: Data visualization

## Conclusion

Health Query Language (HQL) represents an innovative approach to solving a critical challenge in healthcare informatics. By creating a domain-specific language that speaks the language of healthcare professionals, HQL removes technical barriers to data access and enables more efficient, data-driven healthcare delivery and research.
