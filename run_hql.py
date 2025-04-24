#!/usr/bin/env python
"""
Health Query Language (HQL) Command-line Interface
-------------------------------------------------
This script provides a command-line interface for executing HQL commands
on healthcare data.
"""

import sys
import argparse
import pandas as pd
import os.path
from hql import HQLEngine, show_help

def main():
    parser = argparse.ArgumentParser(description='Health Query Language (HQL) CLI')
    
    # Add arguments
    parser.add_argument('-d', '--data', help='Path to the CSV file with patient data')
    parser.add_argument('-q', '--query', help='HQL query to execute')
    parser.add_argument('-i', '--interactive', action='store_true', 
                        help='Run in interactive mode')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if data file exists if specified
    if args.data and not os.path.isfile(args.data):
        print(f"Error: Data file '{args.data}' not found")
        return 1
        
    # Create HQL engine
    engine = HQLEngine(args.data)
    
    # Handle interactive mode
    if args.interactive or (not args.query and sys.stdin.isatty()):
        print("Health Query Language (HQL) Interactive Shell")
        print("Type 'exit' or 'quit' to exit, 'help' for help")
        
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
                
    # Execute a single query
    elif args.query:
        result = engine.execute_query(args.query)
        
        # Handle errors
        if "error" in result:
            print(f"Error: {result['error']}")
            return 1
            
        # Display results based on command type
        if result.get("command") == "find":
            print(f"Found {result['count']} patient(s)")
            if result['count'] > 0:
                df = pd.DataFrame(result['data'])
                print(df)
        elif result.get("command") == "show":
            print(f"{result['function'].capitalize()} of {result['attribute']} for {result['count']} patient(s): {result['result']}")
        elif result.get("command") == "alert":
            if result['alert_triggered']:
                print(f"⚠️ ALERT: {result['matching_patients']} patient(s) match alert condition!")
            else:
                print("No alerts triggered.")
    
    # No arguments, show help
    else:
        parser.print_help()
        
    return 0

if __name__ == "__main__":
    sys.exit(main())