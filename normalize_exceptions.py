#!/usr/bin/env python3
"""Normalize Corrigan Peak exception CSV; preserve uncertain values and report counts."""
import argparse
import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

TERMINALS = {'terminal 3': 'Terminal 3', 't3': 'Terminal 3'}
FORMATS = ('%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M', '%Y-%m-%dT%H:%M:%SZ')
REQUIRED = {'exception_id', 'terminal', 'event_type', 'carrier_code', 'event_ts'}

def normalize_timestamp(raw):
    for fmt in FORMATS:
        try:
            dt = datetime.strptime(raw.strip(), fmt)
            # Source has mixed naive timestamps and UTC-marked timestamps.
            # Do not assume local time zone or convert between zones.
            return dt.strftime('%Y-%m-%dT%H:%M:%S') + ('Z' if fmt.endswith('Z') else '')
        except ValueError:
            continue
    return None

def process(source, output, summary):
    counts = Counter()
    issues = []
    with source.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError('Missing required CSV headers')
        rows = []
        for row in reader:
            record_id = (row['exception_id'] or '').strip()
            terminal_raw = (row['terminal'] or '').strip()
            terminal = TERMINALS.get(terminal_raw.lower())
            if terminal is None:
                terminal = terminal_raw
                issues.append(f'{record_id}: terminal {terminal_raw!r} not in verified alias map')
            carrier = (row['carrier_code'] or '').strip().upper()
            if not carrier:
                issues.append(f'{record_id}: carrier_code missing; cannot infer carrier')
            timestamp_raw = (row['event_ts'] or '').strip()
            timestamp = normalize_timestamp(timestamp_raw)
            if timestamp is None:
                timestamp = timestamp_raw
                issues.append(f'{record_id}: timestamp {timestamp_raw!r} unrecognized')
            elif not timestamp.endswith('Z'):
                issues.append(f'{record_id}: timestamp has no timezone; preserved without assuming UTC')
            event = (row['event_type'] or '').strip().lower()
            if not event:
                issues.append(f'{record_id}: event_type missing')
            else:
                counts[event] += 1
            rows.append({'exception_id': record_id, 'terminal': terminal,
                         'event_type': event, 'carrier_code': carrier, 'event_ts': timestamp})
    with output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['exception_id','terminal','event_type','carrier_code','event_ts'])
        writer.writeheader(); writer.writerows(rows)
    lines = [f'Records processed: {len(rows)}', 'Exception counts by event type:']
    lines += [f'  {event}: {count}' for event, count in sorted(counts.items())]
    lines += ['', 'Data-quality notes:'] + ([f'  - {issue}' for issue in issues] or ['  None'])
    lines += ['', 'No timezone conversion was performed: Z means UTC; timestamps without Z remain timezone-unspecified.',
              'Normalization does not establish the FreightWorks EDI mapping or resolve DET-121.']
    summary.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))
    return counts, issues

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, default=Path('cleaned_exceptions.csv'))
    parser.add_argument('--summary', type=Path, default=Path('exception_summary.txt'))
    args = parser.parse_args()
    process(args.input, args.output, args.summary)
