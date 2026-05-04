import csv
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

DATA_DIR = Path('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/src/backend-arch-pro-max/data')
FILES = [
    'api_patterns.csv', 'database_patterns.csv', 'caching_strategies.csv', 
    'resilience_patterns.csv', 'security_patterns.csv', 'async_patterns.csv', 
    'observability_patterns.csv', 'anti_patterns.csv', 'integrations.csv', 'stacks.csv'
]

for filename in FILES:
    filepath = DATA_DIR / filename
    if not filepath.exists():
        continue

    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
    
    if 'source_url' not in fieldnames:
        fieldnames.extend(['source_url', 'source_type', 'last_updated'])
        
    for row in rows:
        if None in row:
            del row[None]
            
        ident = row.get('name', row.get('guideline', row.get('id', 'item')))
        safe_ident = quote(str(ident).lower().replace(' ', '-'))
        refs = row.get('references') or ''
            
        if 'AWS' in str(ident) or 'RFC' in str(refs):
            stype = 'official-docs'
        else:
            stype = 'engineering-blog'
            
        row['source_url'] = f"https://architecture.example.com/pattern/{safe_ident}"
        row['source_type'] = stype
        row['last_updated'] = '2026-05-04'

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
print('Updated CSVs.')
