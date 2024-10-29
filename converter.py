import pandas as pd
import os

# Use your specific path
input_file_path = r"your/file/path/input.txt"

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def convert_to_csv(input_text):
    # Splits the text into lines
    lines = input_text.strip().split('\n')
    
    # Finds where the data starts (after the header)
    data_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            if 'X' in line and 'Y' in line:  # This is the header line
                headers = line.strip('# ').split()
                data_start = i + 1
                break
    
    # Extracts the data rows
    data = []
    for line in lines[data_start:]:
        if not line.strip().startswith('#'):  # Skips any remaining comments
            # Splits the line and convert to appropriate types
            values = line.strip().split()
            if len(values) >= 8:  # Ensures we have at least the main data columns
                row = {
                    'X_MeV': float(values[0]) if is_float(values[0]) else None,
                    'dX_MeV': float(values[1]) if is_float(values[1]) else None,
                    'Y_barns': float(values[2]) if is_float(values[2]) else None,
                    'dY_barns': float(values[3]) if is_float(values[3]) else None,
                    'Reference': values[5].strip('#').strip(),
                    'EXFOR_ID': values[7].strip('#').strip(),
                    'Uncertainty': values[8].strip() if len(values) > 8 else ''
                }
                data.append(row)
    
    # Creates DataFrame
    df = pd.DataFrame(data)
    return df

try:
    # Reads the input file
    with open(input_file_path, 'r') as file:
        input_text = file.read()
        
    # Converts and saves to CSV
    df = convert_to_csv(input_text)
    # Saves the output CSV in the same folder as input
    output_path = r"your/file/path/output.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Conversion completed! Check {output_path}")
except FileNotFoundError:
    print(f"Error: Could not find the file at {input_file_path}")
    print("Please check if the file path is correct")
