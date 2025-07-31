def parse_csv(file_path, delimiter=','):
    """
    Parse a CSV file and return its contents as a list of lists.
    
    Args:
        file_path (str): Path to the CSV file
        delimiter (str): Character used to separate fields (default: comma)
    
    Returns:
        list: List of lists where each inner list represents a row
    """
    result = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            current_row = []
            current_field = []
            in_quotes = False
            
            for char in file.read():
                if char == '"':
                    in_quotes = not in_quotes
                elif char == delimiter and not in_quotes:
                    current_row.append(''.join(current_field).strip())
                    current_field = []
                elif char == '\n' and not in_quotes:
                    if current_field or current_row:  # Handle empty lines
                        current_row.append(''.join(current_field).strip())
                        result.append(current_row)
                        current_row = []
                        current_field = []
                else:
                    current_field.append(char)
            
            # Handle the last field and row if file doesn't end with newline
            if current_field or current_row:
                current_row.append(''.join(current_field).strip())
                result.append(current_row)
                
        return result
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error parsing CSV: {str(e)}")
        return []

# Example usage
if __name__ == "__main__":
    # Example CSV content for testing
    sample_csv = """
    Name,Age,City
    "John Doe",30,"New York"
    "Jane Smith",25,"Los Angeles"
    """
    
    # Create a temporary file for testing
    with open('sample.csv', 'w', encoding='utf-8') as f:
        f.write(sample_csv.strip())
    
    # Parse the CSV file
    data = parse_csv('sample.csv')
    
    # Print results
    for row in data:
        print(row)