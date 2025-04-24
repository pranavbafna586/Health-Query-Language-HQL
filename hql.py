from parser import HQLParser
from interpreter import HQLInterpreter
import os
import sys
from pathlib import Path

class HQLEngine:
    def __init__(self, data_path=None):
        """Initialize the HQL Engine with optional data path"""
        if data_path is None:
            # Default to patients.csv in the data directory
            current_dir = Path(__file__).parent
            data_path = current_dir / "data" / "patients.csv"
            
        self.parser = HQLParser()
        self.interpreter = HQLInterpreter(data_path)
        
    def execute_query(self, query):
        """Parse and execute a HQL query"""
        # Parse the query
        try:
            print(f"Parsing query: {query}")
            ast = self.parser.parse(query)
            print(f"Generated AST: {ast}")
            if ast is None:
                print("Parser returned None")
                return {"error": "Failed to parse query"}
        except Exception as e:
            print(f"Parser exception: {str(e)}")
            return {"error": f"Parser error: {str(e)}"}
        
        # Execute the parsed query
        try:
            result = self.interpreter.execute(ast)
            return self._format_result(ast, result)
        except Exception as e:
            print(f"Execution exception: {str(e)}")
            return {"error": f"Execution error: {str(e)}"}
    
    def _format_result(self, ast, result):
        """Format the result based on the command type"""
        command_type = ast.get('command_type')
        
        if command_type == 'find':
            return {
                "command": "find",
                "target": ast.get('target'),
                "count": len(result),
                "data": result.to_dict('records')
            }
        elif command_type == 'show':
            return {
                "command": "show",
                "function": ast.get('function'),
                "attribute": result.get('attribute'),
                "result": result.get('result'),
                "count": result.get('count')
            }
        elif command_type == 'alert':
            return {
                "command": "alert",
                "alert_triggered": result.get('alert_triggered'),
                "matching_patients": result.get('matching_patients')
            }
        else:
            return {"error": f"Unknown command type: {command_type}"}


def run_interactive():
    """Run HQL in interactive mode"""
    print("Health Query Language (HQL) Interactive Shell")
    print("Type 'exit' or 'quit' to exit, 'help' for help")
    
    # Initialize the HQL engine
    engine = HQLEngine()
    
    while True:
        try:
            query = input("HQL> ")
            if query.lower() in ('exit', 'quit'):
                break
            elif query.lower() == 'help':
                show_help()
                continue
            elif not query.strip():
                continue
                
            # Execute the query
            result = engine.execute_query(query)
            
            # Handle errors
            if "error" in result:
                print(f"Error: {result['error']}")
                continue
                
            # Display results based on command type
            if result.get("command") == "find":
                print(f"Found {result['count']} patient(s)")
                if result['count'] > 0:
                    import pandas as pd
                    df = pd.DataFrame(result['data'])
                    print(df)
            elif result.get("command") == "show":
                print(f"{result['function'].capitalize()} of {result['attribute']} for {result['count']} patient(s): {result['result']}")
            elif result.get("command") == "alert":
                if result['alert_triggered']:
                    print(f"⚠️ ALERT: {result['matching_patients']} patient(s) match alert condition!")
                else:
                    print("No alerts triggered.")
                    
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


def show_help():
    """Display help information"""
    help_text = """
Health Query Language (HQL) Help:

Commands:
---------
1. FIND patients WHERE <condition>
   Example: FIND patients WHERE age > 60 AND blood_pressure > 140

2. SHOW <aggregate> <attribute> FOR patients WITH <condition>
   Example: SHOW average heart_rate FOR patients WITH diabetes

3. ALERT IF <condition>
   Example: ALERT IF oxygen_level < 90

Conditions:
-----------
- Simple condition: <field> <operator> <value>
  Example: age > 60

- Compound condition: <condition> AND/OR <condition>
  Example: age > 60 AND blood_pressure > 140

Operators:
----------
>, <, =, >=, <=, !=

Aggregates:
-----------
average, count, max, min

Fields:
-------
patient_id, name, age, gender, blood_pressure, 
heart_rate, oxygen_level, diabetes, hypertension, asthma
"""
    print(help_text)


if __name__ == "__main__":
    # If script is run directly, start interactive mode
    run_interactive()