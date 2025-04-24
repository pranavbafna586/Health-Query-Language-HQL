#!/usr/bin/env python
# Simple script to test and debug the HQL components

from lexer import HQLLexer
from parser import HQLParser
from interpreter import HQLInterpreter
from pathlib import Path
import pandas as pd

def test_lexer():
    print("\n=== Testing Lexer ===")
    test_query = "FIND patients WHERE age > 60"
    lexer = HQLLexer()
    lexer.build()
    tokens = lexer.tokenize(test_query)
    print(f"Query: {test_query}")
    print("Tokens:")
    for t in tokens:
        print(f"  {t.type}: {t.value}")

def test_parser():
    print("\n=== Testing Parser ===")
    test_queries = [
        "FIND patients WHERE age > 60",
        "SHOW average heart_rate FOR patients WITH diabetes = yes",
        "ALERT IF oxygen_level < 90"
    ]
    
    parser = HQLParser()
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            ast = parser.parse(query)
            print(f"AST: {ast}")
        except Exception as e:
            print(f"Error: {e}")

def test_interpreter():
    print("\n=== Testing Interpreter ===")
    # Get the current directory
    current_dir = Path(__file__).parent
    data_path = current_dir / "data" / "patients.csv"
    
    # Create the interpreter
    interpreter = HQLInterpreter(data_path)
    
    # Test data overview
    print(f"Loaded {len(interpreter.data)} patient records")
    print("Sample data:")
    print(interpreter.data.head(2))
    
    # Test a simple find command
    test_ast = {
        'command_type': 'find',
        'target': 'patients',
        'condition': {
            'field': 'age',
            'operator': '>',
            'value': 60
        }
    }
    
    print("\nExecuting: FIND patients WHERE age > 60")
    try:
        result = interpreter.execute(test_ast)
        print(f"Found {len(result)} patients")
        print(result[['name', 'age']])
    except Exception as e:
        print(f"Error: {e}")

def test_full_query():
    print("\n=== Testing Full Query Execution ===")
    from hql import HQLEngine
    
    # Create the HQL engine
    engine = HQLEngine()
    
    # Test queries
    test_queries = [
        "FIND patients WHERE age > 60",
        "SHOW average heart_rate FOR patients WITH diabetes = yes",
        "ALERT IF oxygen_level < 90"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            result = engine.execute_query(query)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_lexer()
    test_parser()
    test_interpreter()
    test_full_query()