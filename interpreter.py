import pandas as pd
import numpy as np

class HQLInterpreter:
    def __init__(self, data_path):
        """Initialize the interpreter with the path to the patient data"""
        self.data = pd.read_csv(data_path)
        # Convert yes/no values to boolean
        for col in ['diabetes', 'hypertension', 'asthma']:
            if col in self.data.columns:
                self.data[col] = self.data[col].map({'yes': True, 'no': False})
        
        # Parse blood pressure values (e.g., "140/90" -> systolic=140, diastolic=90)
        if 'blood_pressure' in self.data.columns:
            self.data['systolic'] = self.data['blood_pressure'].apply(lambda x: int(x.split('/')[0]))
            self.data['diastolic'] = self.data['blood_pressure'].apply(lambda x: int(x.split('/')[1]))

    def execute(self, ast):
        """Execute a parsed HQL command"""
        command_type = ast.get('command_type')
        
        if command_type == 'find':
            return self._execute_find(ast)
        elif command_type == 'show':
            return self._execute_show(ast)
        elif command_type == 'alert':
            return self._execute_alert(ast)
        else:
            raise ValueError(f"Unknown command type: {command_type}")

    def _execute_find(self, ast):
        """Execute a FIND command"""
        target = ast.get('target')
        condition = ast.get('condition')
        
        # Ensure target refers to a valid collection
        if target != 'patients':
            raise ValueError(f"Unknown collection: {target}")
            
        # Apply filters based on conditions
        filtered_data = self._apply_condition(self.data, condition)
        
        return filtered_data
    
    def _execute_show(self, ast):
        """Execute a SHOW command"""
        function = ast.get('function')
        attribute = ast.get('attribute')
        target = ast.get('target')
        condition = ast.get('condition')
        
        # Ensure target refers to a valid collection
        if target != 'patients':
            raise ValueError(f"Unknown collection: {target}")
            
        # Special case for blood_pressure
        if attribute == 'blood_pressure':
            # Use systolic by default
            attribute = 'systolic'
            
        # Apply filters based on conditions
        filtered_data = self._apply_condition(self.data, condition)
        
        # Apply the aggregation function
        if function == 'average':
            result = filtered_data[attribute].mean()
        elif function == 'count':
            result = len(filtered_data)
        elif function == 'max':
            result = filtered_data[attribute].max()
        elif function == 'min':
            result = filtered_data[attribute].min()
        else:
            raise ValueError(f"Unknown function: {function}")
            
        return {
            'function': function,
            'attribute': attribute,
            'result': result,
            'count': len(filtered_data)
        }
        
    def _execute_alert(self, ast):
        """Execute an ALERT command"""
        condition = ast.get('condition')
        
        # Apply the condition to identify matching patients
        matching_patients = self._apply_condition(self.data, condition)
        
        # Determine if an alert should be triggered
        alert_triggered = len(matching_patients) > 0
        
        return {
            'alert_triggered': alert_triggered,
            'matching_patients': len(matching_patients),
            'condition': condition
        }
    
    def _apply_condition(self, data, condition):
        """Apply a condition to filter data"""
        if isinstance(condition, dict) and 'left' in condition and 'right' in condition:
            # Complex condition with AND/OR
            operator = condition.get('operator')
            left_result = self._apply_condition(data, condition.get('left'))
            right_result = self._apply_condition(data, condition.get('right'))
            
            if operator == 'and':
                return pd.merge(left_result, right_result, how='inner')
            elif operator == 'or':
                return pd.concat([left_result, right_result]).drop_duplicates()
        else:
            # Simple condition
            field = condition.get('field')
            operator = condition.get('operator')
            value = condition.get('value')
            
            # Convert string values for boolean fields
            if field in ['diabetes', 'hypertension', 'asthma'] and isinstance(value, str):
                val_lower = value.lower()
                if val_lower in ['yes', 'true']:
                    value = True
                elif val_lower in ['no', 'false']:
                    value = False

            # Handle special fields
            if field == 'blood_pressure':
                # Default to systolic
                field = 'systolic'
            
            # Handle the various comparison operators
            if operator == '>':
                return data[data[field] > value]
            elif operator == '<':
                return data[data[field] < value]
            elif operator == '=':
                return data[data[field] == value]
            elif operator == '>=':
                return data[data[field] >= value]
            elif operator == '<=':
                return data[data[field] <= value]
            elif operator == '!=':
                return data[data[field] != value]
            else:
                raise ValueError(f"Unknown operator: {operator}")