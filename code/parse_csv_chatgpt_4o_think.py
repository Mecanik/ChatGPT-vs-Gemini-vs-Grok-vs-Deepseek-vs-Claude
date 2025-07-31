"""
parse_csv.py -- Lightweight CSV parser (no external libraries)

Features
--------
* Customisable field delimiter (default ',').
* Handles quoted fields and escaped quotes ( "" → " ).
* Optionally interprets the first row as a header and yields dictionaries.

Limitations
-----------
* Does **not** support literal new‑lines embedded inside quoted fields (the vast majority of everyday CSVs don’t need this).

Usage (CLI)
-----------
$ python parse_csv.py path/to/file.csv                   # prints each record as JSON
$ python parse_csv.py path/to/file.csv --no-header       # treat first row as data, output lists
$ cat file.csv | python parse_csv.py -d ';'              # read from stdin, semicolon‑delimited

You can also import the module and call `parse_csv()` directly:

```python
from parse_csv import parse_csv
for row in parse_csv('people.csv'):
    print(row['email'])
```
"""
from __future__ import annotations

import sys
import json
from typing import Iterator, List, Dict, Union, TextIO


def _parse_row(row: str, delimiter: str = ',') -> List[str]:
    """Split *row* into fields, honouring quotes and escaped quotes."""
    fields: List[str] = []
    field: List[str] = []
    in_quotes = False
    i = 0
    while i < len(row):
        ch = row[i]
        if in_quotes:
            if ch == '"':
                # Double quote inside a quoted field → literal quote
                if i + 1 < len(row) and row[i + 1] == '"':
                    field.append('"')
                    i += 1  # Skip the escape char
                else:
                    in_quotes = False  # Closing quote
            else:
                field.append(ch)
        else:
            if ch == '"':
                in_quotes = True  # Opening quote
            elif ch == delimiter:
                fields.append(''.join(field))
                field.clear()
            else:
                field.append(ch)
        i += 1
    # Append last field
    fields.append(''.join(field))
    return fields


def _row_iter(handle: TextIO) -> Iterator[str]:
    """Yield each line stripped of trailing CR/LF."""
    for raw in handle:
        yield raw.rstrip('\n').rstrip('\r')


def parse_csv(
    fp: Union[str, TextIO],
    delimiter: str = ',',
    *,
    header: bool = True,
) -> Iterator[Union[List[str], Dict[str, str]]]:
    """Yield records from *fp* (path or file‑like).

    With *header* True (default) the first row becomes the key list and
    each subsequent record is yielded as a dict; otherwise lists are
    yielded.
    """
    should_close = False
    if isinstance(fp, str):
        fp = open(fp, encoding='utf‑8', newline='')  # type: ignore [assignment]
        should_close = True

    try:
        rows = (_parse_row(line, delimiter) for line in _row_iter(fp))
        rows_iter = iter(rows)

        if header:
            try:
                columns = next(rows_iter)
            except StopIteration:
                return  # Empty file
            for record in rows_iter:
                # Pad missing cells; ignore extras
                yield {col: (record[i] if i < len(record) else '') for i, col in enumerate(columns)}
        else:
            yield from rows_iter
    finally:
        if should_close:
            fp.close()


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Parse CSV without the csv module.")
    parser.add_argument('file', help="CSV file path, or '-' for stdin")
    parser.add_argument('-d', '--delimiter', default=',', help="Field delimiter (default ',')")
    parser.add_argument('--no-header', action='store_true', help='Treat first row as data (output lists)')
    args = parser.parse_args()

    source: Union[str, TextIO] = sys.stdin if args.file == '-' else args.file
    for record in parse_csv(source, delimiter=args.delimiter, header=not args.no_header):
        print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    _cli()
