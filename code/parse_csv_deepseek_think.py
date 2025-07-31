def parse_csv(filename):
    rows = []
    current_row = []
    current_field = ""
    in_quote = False
    
    with open(filename, 'r') as file:
        for line in file:
            index = 0
            while index < len(line):
                char = line[index]
                if in_quote:
                    if char == '"':
                        if index + 1 < len(line) and line[index + 1] == '"':
                            current_field += '"'
                            index += 1
                        else:
                            in_quote = False
                    else:
                        current_field += char
                else:
                    if char == ',':
                        current_row.append(current_field)
                        current_field = ""
                    elif char == '"':
                        if current_field == '':
                            in_quote = True
                        else:
                            current_field += char
                    elif char == '\n':
                        if current_field.endswith('\r'):
                            current_field = current_field[:-1]
                        current_row.append(current_field)
                        current_field = ""
                        rows.append(current_row)
                        current_row = []
                        break
                    else:
                        current_field += char
                index += 1
    
    if in_quote or current_field != '' or len(current_row) > 0:
        current_row.append(current_field)
        rows.append(current_row)
    
    return rows

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python csv_parser.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        parsed_data = parse_csv(filename)
        for row in parsed_data:
            print(row)
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        sys.exit(1)