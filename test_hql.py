import sys
import os
from pathlib import Path
import unittest

# Add the parent directory to sys.path to import the HQL modules
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from lexer import HQLLexer
from parser import HQLParser
from interpreter import HQLInterpreter
from hql import HQLEngine

class TestHQLSystem(unittest.TestCase):
    def setUp(self):
        # Set up the data path for testing
        self.data_path = parent_dir / "data" / "patients.csv"
        self.engine = HQLEngine(self.data_path)
    
    def test_find_command(self):
        # Test a simple FIND command
        query = "FIND patients WHERE age > 60"
        result = self.engine.execute_query(query)
        
        self.assertEqual(result["command"], "find")
        self.assertEqual(result["target"], "patients")
        # Should find 4 patients with age > 60 in our sample data
        self.assertEqual(result["count"], 4)
    
    def test_find_with_and(self):
        # Test a FIND command with AND condition
        query = "FIND patients WHERE age > 60 AND diabetes = yes"
        result = self.engine.execute_query(query)
        
        self.assertEqual(result["command"], "find")
        # Should find 3 patients with age > 60 AND diabetes = yes
        self.assertEqual(result["count"], 3)
    
    def test_show_command(self):
        # Test a SHOW command
        query = "SHOW average heart_rate FOR patients WITH diabetes"
        result = self.engine.execute_query(query)
        
        self.assertEqual(result["command"], "show")
        self.assertEqual(result["function"], "average")
        self.assertEqual(result["attribute"], "heart_rate")
        # Should be around 78.0 based on our sample data
        self.assertAlmostEqual(result["result"], 78.0, delta=1.0)
    
    def test_alert_command(self):
        # Test an ALERT command with no matches
        query = "ALERT IF oxygen_level < 90"
        result = self.engine.execute_query(query)
        
        self.assertEqual(result["command"], "alert")
        self.assertEqual(result["alert_triggered"], False)
        self.assertEqual(result["matching_patients"], 0)
        
        # Test an ALERT command with matches
        query = "ALERT IF oxygen_level < 95"
        result = self.engine.execute_query(query)
        
        self.assertEqual(result["command"], "alert")
        self.assertEqual(result["alert_triggered"], True)
        self.assertGreater(result["matching_patients"], 0)
    
    def test_lexer(self):
        # Test the lexer directly
        lexer = HQLLexer()
        lexer.build()
        tokens = lexer.tokenize("FIND patients WHERE age > 60")
        
        token_types = [t.type for t in tokens]
        expected_types = ['FIND', 'ID', 'WHERE', 'ID', 'GT', 'NUMBER']
        self.assertEqual(token_types, expected_types)
    
    def test_parser(self):
        # Test the parser directly
        parser = HQLParser()
        ast = parser.parse("FIND patients WHERE age > 60")
        
        self.assertEqual(ast["command_type"], "find")
        self.assertEqual(ast["target"], "patients")
        self.assertEqual(ast["condition"]["field"], "age")
        self.assertEqual(ast["condition"]["operator"], ">")
        self.assertEqual(ast["condition"]["value"], 60)

if __name__ == "__main__":
    unittest.main()