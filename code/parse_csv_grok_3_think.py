def parse_line(line):
    """Parse a single CSV line into a list of values."""
    line = line.rstrip('\n')  # Remove trailing newline
    values = []
    current_value = ""
    in_quotes = False
    i = 0
    
    while i < len(line):
        char = line[i]
        if char == '"':
            if in_quotes:
                # Check if it's an escaped quote or end of quoted field
                if i + 1 < len(line) and line[i + 1] == '"':
                    current_value += '"'
                    i += 1  # Skip the next quote
                else:
                    in_quotes = False
            else:
                in_quotes = True
        elif char == ',' and not in_quotes:
            values.append(current_value)
            current_value = ""
        else:
            current_value += char
        i += 1
    
    # Append the last value
    values.append(current_value)
    return values

def parse_csv(filename):
    """Parse a CSV file and return a list of rows, where each row is a list of values."""
    with open(filename, 'r') as file:
        data = []
        for line in file:
            parsed_line = parse_line(line)
            data.append(parsed_line)
        return data

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parse_csv.py <filename>")
        sys.exit(1)
    try:
        data = parse_csv(sys.argv[1])
        for row in data:
            print(row)
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")