import re

def parse_csv(csv_string, delimiter=',', quotechar='"'):
    """
    Parse a CSV string into a list of lists (rows and fields)
    
    Args:
        csv_string (str): The CSV content as a string
        delimiter (str): Field delimiter (default: ',')
        quotechar (str): Character used for quoting fields (default: '"')
    
    Returns:
        list: List of rows, each row is a list of fields
    """
    rows = []
    current_row = []
    current_field = []
    in_quotes = False
    i = 0
    n = len(csv_string)
    
    while i < n:
        char = csv_string[i]
        
        if char == quotechar:
            if in_quotes:
                # Check if this is an escaped quote (double quote)
                if i + 1 < n and csv_string[i+1] == quotechar:
                    current_field.append(quotechar)
                    i += 1  # Skip next quote
                else:
                    in_quotes = False
            else:
                in_quotes = True
        elif char == delimiter and not in_quotes:
            # End of field
            current_row.append(''.join(current_field))
            current_field = []
        elif char == '\n' and not in_quotes:
            # End of row
            current_row.append(''.join(current_field))
            rows.append(current_row)
            current_row = []
            current_field = []
            # Handle Windows line endings (\r\n)
            if i + 1 < n and csv_string[i+1] == '\r':
                i += 1
        elif char == '\r' and not in_quotes:
            # End of row (Mac or old Windows line endings)
            current_row.append(''.join(current_field))
            rows.append(current_row)
            current_row = []
            current_field = []
            # Handle Windows line endings (\r\n)
            if i + 1 < n and csv_string[i+1] == '\n':
                i += 1
        else:
            current_field.append(char)
        i += 1
    
    # Add the last field and row if they exist
    if current_field:
        current_row.append(''.join(current_field))
    if current_row:
        rows.append(current_row)
    
    return rows

def read_csv_file(filename, delimiter=',', quotechar='"', encoding='utf-8'):
    """
    Read a CSV file and parse its contents
    
    Args:
        filename (str): Path to the CSV file
        delimiter (str): Field delimiter (default: ',')
        quotechar (str): Character used for quoting fields (default: '"')
        encoding (str): File encoding (default: 'utf-8')
    
    Returns:
        list: List of rows, each row is a list of fields
    """
    with open(filename, 'r', encoding=encoding) as file:
        csv_string = file.read()
    return parse_csv(csv_string, delimiter, quotechar)

def write_csv_file(filename, data, delimiter=',', quotechar='"', encoding='utf-8'):
    """
    Write data to a CSV file
    
    Args:
        filename (str): Path to the output CSV file
        data (list): List of rows, each row is a list of fields
        delimiter (str): Field delimiter (default: ',')
        quotechar (str): Character used for quoting fields (default: '"')
        encoding (str): File encoding (default: 'utf-8')
    """
    with open(filename, 'w', encoding=encoding) as file:
        for row in data:
            formatted_fields = []
            for field in row:
                if isinstance(field, (int, float)):
                    field = str(field)
                # Quote fields that contain delimiter, quotechar, or newlines
                if (delimiter in field or 
                    quotechar in field or 
                    '\n' in field or 
                    '\r' in field):
                    field = quotechar + field.replace(quotechar, quotechar*2) + quotechar
                formatted_fields.append(field)
            file.write(delimiter.join(formatted_fields) + '\n')

# Example usage
if __name__ == "__main__":
    # Example CSV content
    example_csv = """Name,Age,Occupation
"John Doe",30,"Software Developer"
Jane ""The Rocket"" Smith,25,Athlete
"Alice, Wonder",28,"Writer, Poet"
Bob,35,Engineer"""
    
    # Parse the example CSV
    parsed_data = parse_csv(example_csv)
    print("Parsed CSV:")
    for row in parsed_data:
        print(row)
    
    # Write to a file and read back
    test_filename = "test_csv.csv"
    write_csv_file(test_filename, parsed_data)
    print(f"\nWritten to {test_filename}")
    
    print("\nReading back from file:")
    file_data = read_csv_file(test_filename)
    for row in file_data:
        print(row)