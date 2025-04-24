#!/usr/bin/env python
"""
Health Query Language (HQL) Launcher
-----------------------------------
This script provides a simple way to launch either the web interface
or the command-line interface for the HQL system.
"""

import os
import sys
import webbrowser
import time
import threading
import argparse
from pathlib import Path

def launch_web_interface():
    """Launch the HQL web interface"""
    print("Starting the HQL Web Interface...")
    print("This will open a web browser automatically when ready.")
    
    # Define a function to open the web browser after a short delay
    def open_browser():
        time.sleep(1.5)  # Wait for Flask to start
        webbrowser.open('http://localhost:5000')
        
    # Start the browser opening in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Import and run the web app
    try:
        from web_app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError:
        print("Error: Could not import the web application.")
        print("Please make sure Flask is installed: pip install flask")
        return 1
    except Exception as e:
        print(f"Error starting the web interface: {str(e)}")
        return 1
        
    return 0

def launch_cli_interface(args=None):
    """Launch the HQL command-line interface"""
    print("Starting the HQL Command-Line Interface...")
    
    # Import and run the CLI
    try:
        from run_hql import main
        if args is None:
            return main()
        else:
            sys.argv = [sys.argv[0]] + args
            return main()
    except ImportError:
        print("Error: Could not import the HQL command-line interface.")
        return 1
    except Exception as e:
        print(f"Error starting the command-line interface: {str(e)}")
        return 1
        
    return 0

def main():
    parser = argparse.ArgumentParser(
        description='Health Query Language (HQL) Launcher',
        epilog='Run without arguments to launch the interface selection menu'
    )
    parser.add_argument('--web', action='store_true', help='Launch the web interface directly')
    parser.add_argument('--cli', action='store_true', help='Launch the command-line interface directly')
    parser.add_argument('--query', '-q', help='Execute a query in the command-line interface and exit')
    parser.add_argument('--data', '-d', help='Specify a data file to use')
    
    args = parser.parse_args()
    
    # If direct mode options are provided, launch the specified interface
    if args.web:
        return launch_web_interface()
    elif args.cli or args.query:
        cli_args = []
        if args.query:
            cli_args.extend(['-q', args.query])
        if args.data:
            cli_args.extend(['-d', args.data])
        return launch_cli_interface(cli_args)
    
    # If no direct mode is specified, show the menu
    while True:
        print("\n====================================")
        print("Health Query Language (HQL) Launcher")
        print("====================================")
        print("1. Launch Web Interface (Recommended)")
        print("2. Launch Command-Line Interface")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            return launch_web_interface()
        elif choice == '2':
            return launch_cli_interface()
        elif choice == '3':
            print("Exiting HQL Launcher...")
            return 0
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    sys.exit(main())