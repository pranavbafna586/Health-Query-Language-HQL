from flask import Flask, render_template, request, jsonify
from hql import HQLEngine
import pandas as pd
import os
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'health-query-language-secret-key'

# Initialize the HQL engine
data_path = Path(__file__).parent / "data" / "patients.csv"
engine = HQLEngine(data_path)

@app.route('/')
def index():
    """Render the main HQL web interface"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_query():
    """Execute an HQL query and return results as JSON"""
    query = request.form.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'})
    
    # Execute the query
    result = engine.execute_query(query)
    
    # Handle errors
    if 'error' in result:
        return jsonify({'error': result['error']})
    
    # Format results based on command type
    if result.get('command') == 'find':
        # Convert DataFrame records to JSON-compatible format
        patient_data = result.get('data', [])
        return jsonify({
            'command': 'find',
            'count': result.get('count', 0),
            'data': patient_data
        })
    elif result.get('command') == 'show':
        return jsonify({
            'command': 'show',
            'function': result.get('function', ''),
            'attribute': result.get('attribute', ''),
            'result': str(result.get('result', '')),
            'count': result.get('count', 0)
        })
    elif result.get('command') == 'alert':
        return jsonify({
            'command': 'alert',
            'alert_triggered': result.get('alert_triggered', False),
            'matching_patients': result.get('matching_patients', 0)
        })
    else:
        return jsonify({'error': 'Unknown command type'})

@app.route('/examples')
def examples():
    """Return a list of example HQL queries"""
    examples = [
        {
            'title': 'Find elderly patients with high blood pressure',
            'query': 'FIND patients WHERE age > 60 AND blood_pressure > 140',
            'description': 'Locate patients over 60 years old with high blood pressure (systolic > 140)'
        },
        {
            'title': 'Show average heart rate for diabetic patients',
            'query': 'SHOW average heart_rate FOR patients WITH diabetes = yes',
            'description': 'Calculate the average heart rate among all patients with diabetes'
        },
        {
            'title': 'Alert for low oxygen levels',
            'query': 'ALERT IF oxygen_level < 95',
            'description': 'Identify patients with potentially concerning oxygen levels below 95%'
        },
        {
            'title': 'Find young asthmatic patients',
            'query': 'FIND patients WHERE age < 50 AND asthma = yes',
            'description': 'Locate patients under 50 years old who have asthma'
        },
        {
            'title': 'Show maximum heart rate by gender',
            'query': 'SHOW max heart_rate FOR patients WITH gender = F',
            'description': 'Find the maximum heart rate recorded among female patients'
        }
    ]
    return jsonify(examples)

@app.route('/patient-stats')
def patient_stats():
    """Return basic statistics about the patient dataset"""
    data = pd.read_csv(data_path)
    stats = {
        'total_patients': len(data),
        'age_distribution': {
            'min': int(data['age'].min()),
            'max': int(data['age'].max()),
            'avg': round(data['age'].mean(), 1)
        },
        'gender_distribution': data['gender'].value_counts().to_dict(),
        'conditions': {
            'diabetes': int(data['diabetes'].value_counts().get('yes', 0)),
            'hypertension': int(data['hypertension'].value_counts().get('yes', 0)),
            'asthma': int(data['asthma'].value_counts().get('yes', 0))
        }
    }
    return jsonify(stats)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / "templates"
    static_dir = Path(__file__).parent / "static"
    if not templates_dir.exists():
        templates_dir.mkdir()
    if not static_dir.exists():
        static_dir.mkdir()
        (static_dir / "css").mkdir()
        (static_dir / "js").mkdir()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)