#!/usr/bin/env python3
"""
A CSV parser that doesn't rely on external libraries.
Handles quoted fields, escaped quotes, and various CSV edge cases.
"""

class CSVParser:
    def __init__(self, delimiter=',', quote_char='"'):
        self.delimiter = delimiter
        self.quote_char = quote_char
    
    def parse_line(self, line):
        """Parse a single CSV line into fields."""
        fields = []
        current_field = ''
        in_quotes = False
        i = 0
        
        while i < len(line):
            char = line[i]
            
            if char == self.quote_char:
                if in_quotes:
                    # Check if this is an escaped quote (double quote)
                    if i + 1 < len(line) and line[i + 1] == self.quote_char:
                        current_field += self.quote_char
                        i += 1  # Skip the next quote
                    else:
                        # End of quoted field
                        in_quotes = False
                else:
                    # Start of quoted field
                    in_quotes = True
            elif char == self.delimiter and not in_quotes:
                # Field separator found outside quotes
                fields.append(current_field.strip())
                current_field = ''
            else:
                # Regular character
                current_field += char
            
            i += 1
        
        # Add the last field
        fields.append(current_field.strip())
        return fields
    
    def parse_file(self, filename, has_header=True):
        """Parse an entire CSV file."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
        
        if not lines:
            print("Error: File is empty.")
            return None
        
        # Remove newline characters and filter out empty lines
        lines = [line.rstrip('\n\r') for line in lines if line.strip()]
        
        if not lines:
            print("Error: No valid data found in file.")
            return None
        
        result = {
            'headers': [],
            'data': [],
            'raw_data': []
        }
        
        # Parse header if present
        if has_header:
            result['headers'] = self.parse_line(lines[0])
            data_lines = lines[1:]
        else:
            data_lines = lines
        
        # Parse data lines
        for line_num, line in enumerate(data_lines, start=2 if has_header else 1):
            try:
                parsed_line = self.parse_line(line)
                result['data'].append(parsed_line)
                result['raw_data'].append(line)
            except Exception as e:
                print(f"Warning: Error parsing line {line_num}: {e}")
                continue
        
        return result
    
    def parse_string(self, csv_string, has_header=True):
        """Parse CSV data from a string."""
        lines = csv_string.strip().split('\n')
        lines = [line.rstrip('\r') for line in lines if line.strip()]
        
        if not lines:
            return None
        
        result = {
            'headers': [],
            'data': [],
            'raw_data': []
        }
        
        # Parse header if present
        if has_header:
            result['headers'] = self.parse_line(lines[0])
            data_lines = lines[1:]
        else:
            data_lines = lines
        
        # Parse data lines
        for line in data_lines:
            parsed_line = self.parse_line(line)
            result['data'].append(parsed_line)
            result['raw_data'].append(line)
        
        return result


def display_csv_data(parsed_data, max_rows=10):
    """Display parsed CSV data in a readable format."""
    if not parsed_data:
        print("No data to display.")
        return
    
    headers = parsed_data['headers']
    data = parsed_data['data']
    
    print(f"\nParsed CSV Data ({len(data)} rows):")
    print("-" * 50)
    
    if headers:
        print("Headers:", " | ".join(headers))
        print("-" * 50)
    
    # Display first few rows
    rows_to_show = min(max_rows, len(data))
    for i in range(rows_to_show):
        row = data[i]
        print(f"Row {i+1}: {' | '.join(row)}")
    
    if len(data) > max_rows:
        print(f"... and {len(data) - max_rows} more rows")


def main():
    """Main function with usage examples."""
    print("CSV Parser - No External Libraries")
    print("=" * 40)
    
    # Example 1: Parse from string
    print("\nExample 1: Parsing CSV string")
    csv_string = '''Name,Age,City,"Quote Example"
John Doe,30,New York,"He said, ""Hello World"""
Jane Smith,25,Los Angeles,"Simple value"
Bob Johnson,35,"San Francisco","Value with, comma"'''
    
    parser = CSVParser()
    result = parser.parse_string(csv_string)
    display_csv_data(result)
    
    # Example 2: Different delimiter
    print("\n\nExample 2: Parsing with semicolon delimiter")
    csv_semicolon = '''Name;Age;Department
Alice;28;Engineering
Bob;32;"Human Resources"
Carol;29;Marketing'''
    
    parser_semicolon = CSVParser(delimiter=';')
    result2 = parser_semicolon.parse_string(csv_semicolon)
    display_csv_data(result2)
    
    # Example 3: File parsing (interactive)
    print("\n\nExample 3: File parsing")
    filename = input("Enter CSV filename to parse (or press Enter to skip): ").strip()
    
    if filename:
        file_result = parser.parse_file(filename)
        if file_result:
            display_csv_data(file_result)
    else:
        print("File parsing skipped.")
    
    # Example 4: Creating a sample CSV file
    print("\n\nExample 4: Creating and parsing a sample file")
    sample_data = '''Product,Price,Description,In Stock
"Laptop",999.99,"High-performance laptop with 16GB RAM",Yes
"Mouse",29.99,"Wireless optical mouse",Yes
"Keyboard",79.99,"Mechanical keyboard with ""RGB lighting""",No
"Monitor",299.99,"24-inch 4K display, perfect for work",Yes'''
    
    try:
        with open('sample.csv', 'w') as f:
            f.write(sample_data)
        print("Created sample.csv")
        
        sample_result = parser.parse_file('sample.csv')
        display_csv_data(sample_result)
        
        # Convert to dictionary format
        print("\nConverting to list of dictionaries:")
        if sample_result and sample_result['headers']:
            dict_data = []
            for row in sample_result['data']:
                row_dict = {}
                for i, header in enumerate(sample_result['headers']):
                    row_dict[header] = row[i] if i < len(row) else ''
                dict_data.append(row_dict)
            
            for i, record in enumerate(dict_data[:3]):  # Show first 3 records
                print(f"Record {i+1}: {record}")
    
    except Exception as e:
        print(f"Error creating sample file: {e}")


if __name__ == "__main__":
    main()