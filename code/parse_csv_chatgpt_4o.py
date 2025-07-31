def parse_csv_line(line):
    fields = []
    field = ''
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if in_quotes:
            if char == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    field += '"'
                    i += 1
                else:
                    in_quotes = False
            else:
                field += char
        else:
            if char == '"':
                in_quotes = True
            elif char == ',':
                fields.append(field)
                field = ''
            else:
                field += char
        i += 1
    fields.append(field)
    return fields

def parse_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        rows = []
        buffer = ''
        in_quotes = False
        for line in f:
            line = line.rstrip('\n')
            quote_count = line.count('"')
            buffer += (line + '\n') if in_quotes else line
            in_quotes ^= (quote_count % 2 != 0)

            if not in_quotes:
                rows.append(parse_csv_line(buffer.strip()))
                buffer = ''
        return rows

def main():
    filename = 'example.csv'  # Replace with your file path
    data = parse_csv(filename)

    for row in data:
        print(row)

if __name__ == '__main__':
    main()
