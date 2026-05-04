import csv
from pathlib import Path

DATA_DIR = Path('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/src/backend-arch-pro-max/data')
FILES = [
    'api_patterns.csv', 'database_patterns.csv', 'caching_strategies.csv', 
    'resilience_patterns.csv', 'security_patterns.csv', 'async_patterns.csv', 
    'observability_patterns.csv', 'anti_patterns.csv', 'integrations.csv', 'stacks.csv'
]

NEW_COLS = ["throughput_tier", "latency_tier", "cost_tier", "complexity_tier"]

for filename in FILES:
    filepath = DATA_DIR / filename
    if not filepath.exists():
        continue
        
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)
        
    added = False
    for col in NEW_COLS:
        if col not in fieldnames:
            fieldnames.append(col)
            added = True
            
    if added:
        for row in rows:
            ident = str(row.get('name', row.get('guideline', row.get('id', 'item')))).lower()
            
            # Simple heuristic guessing based on words
            if 'cache' in ident or 'redis' in ident or 'memcached' in ident or 'in-memory' in ident:
                row['throughput_tier'] = 'extreme'
                row['latency_tier'] = 'low'
                row['cost_tier'] = 'high'
                row['complexity_tier'] = 'medium'
            elif 'kafka' in ident or 'event sourcing' in ident or 'stream' in ident:
                row['throughput_tier'] = 'extreme'
                row['latency_tier'] = 'medium'
                row['cost_tier'] = 'high'
                row['complexity_tier'] = 'high'
            elif 'serverless' in ident or 'lambda' in ident:
                row['throughput_tier'] = 'high'
                row['latency_tier'] = 'medium'
                row['cost_tier'] = 'low'
                row['complexity_tier'] = 'low'
            elif 'anti' in filename or 'bad' in ident:
                row['throughput_tier'] = 'low'
                row['latency_tier'] = 'high'
                row['cost_tier'] = 'high'
                row['complexity_tier'] = 'high'
            else:
                # Default
                row['throughput_tier'] = 'any'
                row['latency_tier'] = 'any'
                row['cost_tier'] = 'medium'
                row['complexity_tier'] = 'medium'
                
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            
print('Constraint columns added.')
