#!/usr/bin/env python3
"""
CSV Parser - Pure Python implementation without external libraries
Handles common CSV formats including quoted fields, escaped quotes, and custom delimiters.
"""

class CSVParser:
    def __init__(self, delimiter=',', quote_char='"', escape_char=None):
        self.delimiter = delimiter
        self.quote_char = quote_char
        self.escape_char = escape_char or quote_char
    
    def parse_line(self, line):
        """Parse a single CSV line into fields."""
        fields = []
        current_field = ""
        in_quotes = False
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char == self.quote_char:
                if in_quotes:
                    # Check if this is an escaped quote
                    if i + 1 < len(line) and line[i + 1] == self.quote_char:
                        current_field += self.quote_char
                        i += 1  # Skip the next quote
                    else:
                        in_quotes = False
                else:
                    in_quotes = True
            elif char == self.delimiter and not in_quotes:
                fields.append(current_field)
                current_field = ""
            else:
                current_field += char
            
            i += 1
        
        # Add the last field
        fields.append(current_field)
        return fields
    
    def parse_file(self, filename, has_header=True):
        """Parse an entire CSV file."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = []
                header = None
                
                for line_num, line in enumerate(file, 1):
                    line = line.rstrip('\n\r')
                    if not line.strip():  # Skip empty lines
                        continue
                    
                    try:
                        parsed_line = self.parse_line(line)
                        
                        if has_header and header is None:
                            header = parsed_line
                        else:
                            lines.append(parsed_line)
                    
                    except Exception as e:
                        print(f"Error parsing line {line_num}: {e}")
                        continue
                
                return {'header': header, 'data': lines}
        
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def parse_string(self, csv_string, has_header=True):
        """Parse CSV data from a string."""
        lines = csv_string.strip().split('\n')
        parsed_lines = []
        header = None
        
        for line in lines:
            if not line.strip():
                continue
            
            parsed_line = self.parse_line(line)
            
            if has_header and header is None:
                header = parsed_line
            else:
                parsed_lines.append(parsed_line)
        
        return {'header': header, 'data': parsed_lines}


def display_csv_data(csv_data):
    """Display parsed CSV data in a formatted way."""
    if not csv_data:
        print("No data to display.")
        return
    
    header = csv_data.get('header')
    data = csv_data.get('data', [])
    
    if header:
        print("Header:", " | ".join(header))
        print("-" * (len(" | ".join(header))))
    
    for i, row in enumerate(data):
        if header and len(row) != len(header):
            print(f"Warning: Row {i+1} has {len(row)} fields, expected {len(header)}")
        
        print(" | ".join(str(field) for field in row))


def main():
    """Example usage of the CSV parser."""
    
    # Example 1: Parse CSV string
    print("=== Example 1: Parsing CSV string ===")
    csv_string = '''Name,Age,City,Description
John Doe,30,New York,"Software Engineer, Python Developer"
Jane Smith,25,San Francisco,"Data Scientist, ""Machine Learning"" Expert"
Bob Johnson,35,Chicago,Manager'''
    
    parser = CSVParser()
    result = parser.parse_string(csv_string)
    display_csv_data(result)
    
    print("\n=== Example 2: Parsing with different delimiter ===")
    csv_string_semicolon = '''Name;Age;City
Alice;28;Boston
Charlie;32;Seattle'''
    
    parser_semicolon = CSVParser(delimiter=';')
    result = parser_semicolon.parse_string(csv_string_semicolon)
    display_csv_data(result)
    
    print("\n=== Example 3: Creating a sample CSV file and parsing it ===")
    
    # Create a sample CSV file
    sample_filename = "sample_data.csv"
    sample_data = '''Product,Price,Stock,Notes
"Laptop Pro",1299.99,15,"High-performance laptop, ""Gaming Ready"""
"Mouse Wireless",29.99,50,"Ergonomic design"
"Keyboard Mechanical",89.99,25,"Cherry MX switches, RGB lighting"
"Monitor 4K",399.99,8,"32-inch display, ""Ultra HD"""'''
    
    try:
        with open(sample_filename, 'w', encoding='utf-8') as f:
            f.write(sample_data)
        
        print(f"Created sample file: {sample_filename}")
        
        # Parse the file
        file_result = parser.parse_file(sample_filename)
        display_csv_data(file_result)
        
        # Clean up
        import os
        os.remove(sample_filename)
        print(f"\nCleaned up: {sample_filename}")
        
    except Exception as e:
        print(f"Error creating/processing sample file: {e}")
    
    print("\n=== Example 4: Interactive CSV parsing ===")
    print("Enter CSV data (press Enter twice to finish):")
    
    user_input = []
    while True:
        line = input()
        if line == "" and user_input:
            break
        if line != "":
            user_input.append(line)
    
    if user_input:
        user_csv = '\n'.join(user_input)
        print("\nParsing your input:")
        user_result = parser.parse_string(user_csv)
        display_csv_data(user_result)


if __name__ == "__main__":
    main()