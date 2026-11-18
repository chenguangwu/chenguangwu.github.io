#!/usr/bin/env python3
"""Compare locally supplied AAP 2022 tables with a pinned third-party dataset.

Requires pypdf; this script performs no downloads and contains no table data.
Input PDF mirror: https://pqcnc-documents.s3.amazonaws.com/lpi/PQCNCCareoftheLatePretermInfantWebResourcesAAPClinPracHypebili2022.pdf
Candidate: https://github.com/buithanhninh/bilitool/blob/ec7fe43627850223a7d204275b814874c77574d0/contracts/his-emr/clinical-dataset-aap2022.json
The data comparison does not establish permission to redistribute either input.
"""
import argparse
import hashlib
import json
import logging
import re
import sys
from pathlib import Path

PDF_SHA256 = '0d80f9c16296c9124fe51eed90707fd136d2e7d42b70a55e67f8f154c8db63b4'
JSON_SHA256 = 'afd96f1afd29dd40ea5c7657e1c38101961210ca06589afe7311960c37d30ca7'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('dataset', type=Path)
    args = parser.parse_args()
    for path, expected in ((args.pdf, PDF_SHA256), (args.dataset, JSON_SHA256)):
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f'{path}: SHA-256 {actual}')
        if actual != expected:
            raise ValueError(f'Unrecognized input hash: {path}; expected {expected}')
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit('Install pypdf separately to read the local PDF.') from exc
    logging.disable(logging.CRITICAL)
    entries = json.loads(args.dataset.read_text(encoding='utf-8'))['entries']
    index = {(e['curveGestationalAgeWeeks'], e['riskMode'], e['ageHours']): e for e in entries}
    if len(index) != len(entries) or len(index) != 4032:
        raise ValueError('Unexpected dataset size or duplicate keys')
    reader = PdfReader(str(args.pdf))
    table = 0
    ga = None
    printed = {i: 0 for i in range(1, 5)}
    mismatch = []
    notes = []
    for page in range(40, 47):
        for line in reader.pages[page].extract_text().splitlines():
            match = re.search(r'SUPPLEMENTAL TABLE\s*([1-4])', line)
            if match:
                table = int(match.group(1))
                ga = None
            match = re.search(r'Gestational age of (\d+)', line)
            if match:
                ga = int(match.group(1))
            match = re.search(r'threshold \$(\d+) h .*? is (\d+(?:\.\d+)?) mg/dL', line)
            if match and ga:
                notes.append((table, ga, int(match.group(1)), float(match.group(2))))
            match = re.match(r'^(\d{1,2})\s+((?:\d+\.\d+[a-z]?\s*)+)$', line)
            if not match or not table or not ga:
                continue
            day = int(match.group(1))
            values = re.findall(r'\d+\.\d+', match.group(2))
            if day == 0 and len(values) == 23:
                start = 1
            elif len(values) == 24:
                start = 0
            else:
                raise ValueError(f'Unexpected row at PDF page {page + 1}, table {table}, GA {ga}, day {day}: {len(values)} values')
            for hour, value in enumerate(values, start):
                age = day * 24 + hour
                if not 1 <= age <= 336:
                    continue
                gas = range(38, 41) if ga == 38 and table in (2, 3, 4) else (ga,)
                risk = 'None' if table in (1, 3) else 'Neurotoxicity'
                field = 'phototherapyMgDl' if table in (1, 2) else 'exchangeMgDl'
                for g in gas:
                    actual = index[(g, risk, age)][field]
                    printed[table] += 1
                    if float(value) != actual:
                        mismatch.append((table, g, age, float(value), actual))
    print('Printed cells by table:', printed, '; mismatches:', len(mismatch))
    for item in mismatch:
        print('  printed mismatch (table, GA, hour, PDF, dataset):', item)
    plateau_count = 0
    plateau_mismatch = []
    for table, ga, start, value in notes:
        gas = range(38, 41) if ga == 38 and table in (2, 3, 4) else (ga,)
        risk = 'None' if table in (1, 3) else 'Neurotoxicity'
        field = 'phototherapyMgDl' if table in (1, 2) else 'exchangeMgDl'
        for g in gas:
            for age in range(start, 337):
                plateau_count += 1
                actual = index[(g, risk, age)][field]
                if value != actual:
                    plateau_mismatch.append((table, g, age, value, actual))
    print('Plateau comparisons:', plateau_count, '; mismatches:', len(plateau_mismatch))
    for item in plateau_mismatch:
        print('  plateau mismatch (table, GA, hour, footnote, dataset):', item)
    if printed != {1: 1629, 2: 1196, 3: 1196, 4: 2016} or len(notes) != 7:
        raise ValueError('PDF extraction incomplete or changed; inspect extraction')
    return 1 if mismatch or plateau_mismatch else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, IndexError) as exc:
        sys.exit(str(exc))
