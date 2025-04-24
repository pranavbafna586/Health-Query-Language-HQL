#!/usr/bin/env python
"""
Health Query Language (HQL) Demo
-------------------------------
This script demonstrates how to use HQL as a library within other Python applications.
It shows common use cases for healthcare applications integrating HQL.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from hql import HQLEngine

def main():
    # Initialize the HQL engine with our sample data
    data_path = Path(__file__).parent / "data" / "patients.csv"
    engine = HQLEngine(data_path)
    
    print("=" * 60)
    print("HEALTH QUERY LANGUAGE (HQL) DEMONSTRATION")
    print("=" * 60)
    print("\nThis demo shows how HQL can be used as a library in healthcare applications.\n")
    
    # Example 1: Finding elderly patients with high blood pressure
    print("\n[EXAMPLE 1] Finding elderly patients with high blood pressure")
    print("-" * 60)
    
    query = "FIND patients WHERE age > 60 AND blood_pressure > 140"
    print(f"Query: {query}")
    
    result = engine.execute_query(query)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Found {result['count']} patients.")
        
        # Convert to DataFrame for easy manipulation
        df = pd.DataFrame(result['data'])
        print("\nPatient details:")
        print(df[['patient_id', 'name', 'age', 'blood_pressure']].to_string(index=False))
        
        # Calculate risk score (simplified example)
        df['risk_score'] = df['age'] / 10 + (df['systolic'] - 120) / 10
        print("\nCalculated risk scores based on age and blood pressure:")
        print(df[['name', 'age', 'systolic', 'risk_score']].sort_values(by='risk_score', ascending=False).to_string(index=False))
    
    # Example 2: Analyzing heart rate statistics for diabetic vs non-diabetic patients
    print("\n\n[EXAMPLE 2] Comparing heart rate statistics for patients with and without diabetes")
    print("-" * 60)
    
    # Query for diabetic patients
    diabetic_query = "SHOW average heart_rate FOR patients WITH diabetes = yes"
    print(f"Query 1: {diabetic_query}")
    
    diabetic_result = engine.execute_query(diabetic_query)
    if "error" in diabetic_result:
        print(f"Error: {diabetic_result['error']}")
    else:
        diabetic_avg = float(diabetic_result['result'])
        diabetic_count = diabetic_result['count']
        print(f"Average heart rate for diabetic patients: {diabetic_avg:.1f} BPM ({diabetic_count} patients)")
    
    # Query for non-diabetic patients
    non_diabetic_query = "SHOW average heart_rate FOR patients WITH diabetes = no"
    print(f"Query 2: {non_diabetic_query}")
    
    non_diabetic_result = engine.execute_query(non_diabetic_query)
    if "error" in non_diabetic_result:
        print(f"Error: {non_diabetic_result['error']}")
    else:
        non_diabetic_avg = float(non_diabetic_result['result'])
        non_diabetic_count = non_diabetic_result['count']
        print(f"Average heart rate for non-diabetic patients: {non_diabetic_avg:.1f} BPM ({non_diabetic_count} patients)")
    
    print("\nClinical Insight: A difference in average heart rates between diabetic and non-diabetic")
    print(f"patients of {abs(diabetic_avg - non_diabetic_avg):.1f} BPM may indicate cardiovascular effects of diabetes.")
    
    # Example 3: Setting up an alert system for patient monitoring
    print("\n\n[EXAMPLE 3] Setting up an oxygen level alert system")
    print("-" * 60)
    
    alert_thresholds = [95, 90, 85]
    
    for threshold in alert_thresholds:
        query = f"ALERT IF oxygen_level < {threshold}"
        print(f"\nQuery: {query}")
        
        result = engine.execute_query(query)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            if result['alert_triggered']:
                print(f"⚠️  ALERT: {result['matching_patients']} patient(s) have oxygen levels below {threshold}%")
                
                # Get details of patients with low oxygen
                low_oxygen_query = f"FIND patients WHERE oxygen_level < {threshold}"
                detail_result = engine.execute_query(low_oxygen_query)
                
                if "error" not in detail_result:
                    df = pd.DataFrame(detail_result['data'])
                    print("\nPatients requiring attention:")
                    print(df[['patient_id', 'name', 'oxygen_level']].to_string(index=False))
                    
                    if threshold < 90:
                        print(f"\nUrgent clinical action recommended for patients with O₂ < {threshold}%")
            else:
                print(f"✓ No patients have oxygen levels below {threshold}%")
    
    print("\n\n[DEMO COMPLETE] HQL library integration demonstrated successfully")
    print("=" * 60)
    print("This demo showed how HQL can be used to:")
    print("1. Find patients matching specific clinical criteria")
    print("2. Calculate and compare aggregate health metrics")
    print("3. Set up monitoring alerts with different thresholds")
    print("=" * 60)

if __name__ == "__main__":
    main()