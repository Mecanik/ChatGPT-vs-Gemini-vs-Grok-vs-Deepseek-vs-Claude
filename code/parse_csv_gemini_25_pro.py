#!/usr/bin/env python3
"""
A Python script to parse CSV files from scratch without any external libraries.
This script provides a function to read a CSV file and convert it into a
list of dictionaries.
"""
import os

def parse_csv(filepath, delimiter=','):
    """
    Parses a CSV file and returns its content as a list of dictionaries.

    This parser handles:
    - Custom delimiters.
    - Quoted fields containing delimiters.
    - Escaped quotes (e.g., "a ""quoted"" field").

    Args:
        filepath (str): The path to the CSV file.
        delimiter (str, optional): The field delimiter. Defaults to ','.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row.
              Returns an empty list if the file is not found or is empty.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'")
        return []

    parsed_data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if not lines:
        return []

    # Extract header and strip any whitespace from column names
    header = [h.strip() for h in lines[0].strip().split(delimiter)]
    
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue # Skip empty lines

        values = []
        field = ""
        in_quotes = False
        i = 0
        while i < len(line):
            char = line[i]

            if in_quotes:
                # If the current char is a quote
                if char == '"':
                    # Check if it's an escaped quote ("")
                    if i + 1 < len(line) and line[i+1] == '"':
                        field += '"'
                        i += 1  # Skip next character
                    else:
                        in_quotes = False
                else:
                    field += char
            else: # Not in quotes
                if char == '"':
                    in_quotes = True
                elif char == delimiter:
                    values.append(field)
                    field = ""
                else:
                    field += char
            i += 1
        
        values.append(field) # Add the last field from the line

        # Ensure row length matches header length before creating dict
        if len(values) == len(header):
            parsed_data.append(dict(zip(header, values)))
        else:
            print(f"Warning: Skipping malformed row. Expected {len(header)} fields, found {len(values)}: {line}")

    return parsed_data

if __name__ == "__main__":
    # --- Demonstration ---
    
    # 1. Define sample CSV content and create a temporary file
    csv_content = (
        'Year,Make,Model,Description,Price\n'
        '1997,Ford,E350,"ac, abs, moon",3000.00\n'
        '1999,Chevy,"Venture ""Extended Edition""",4900.00\n'
        '1996,Jeep,Grand Cherokee,"MUST SELL! air, moon roof, loaded",4799.00\n'
        '2005,Honda,Accord,"excellent condition, one owner",7500.00\n'
        ',,,,\n' # An empty line to test skipping
        '2010,Toyota,Camry,,"5500.00"'
    )
    temp_file_name = "sample_data.csv"
    with open(temp_file_name, "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    print(f"✅ Created a sample CSV file: '{temp_file_name}'")
    print("-" * 25)

    # 2. Parse the CSV file using the function
    data = parse_csv(temp_file_name)

    # 3. Print the results in a readable format
    print("Parsing complete. Result:\n")
    if data:
        for index, row in enumerate(data):
            print(f"Row {index + 1}: {row}")
    
    # 4. Clean up the temporary file
    os.remove(temp_file_name)
    print("-" * 25)
    print(f"✅ Cleaned up temporary file: '{temp_file_name}'")