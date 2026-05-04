import re
from pathlib import Path

def add_freshness_to_search(path_str):
    path = Path(path_str)
    if not path.exists():
        return
        
    content = path.read_text(encoding='utf-8')
    
    stale_logic = '''
def check_stale(domain=None, max_age_months=18):
    domains = [domain] if domain else [k for k in CSV_CONFIG.keys() if k != "anti-patterns"]
    if domain == "anti-patterns":
        domains = ["anti-patterns"]
    elif not domain:
        domains.extend(["anti-patterns"])
        
    from datetime import datetime
    now = datetime.now()
    stale_results = []
    
    for d in domains:
        if d not in CSV_CONFIG: continue
        config = CSV_CONFIG[d]
        filepath = DATA_DIR / config["file"]
        if not filepath.exists(): continue
        
        rows = load_csv(filepath)
        for i, row in enumerate(rows, 2):
            last_updated = row.get("last_updated")
            if not last_updated:
                stale_results.append(f"- {config['file']}:{i} (No last_updated date) - {row.get('name', row.get('id', 'Unknown'))}")
                continue
                
            try:
                dt = datetime.strptime(last_updated, "%Y-%m-%d")
                months_old = (now.year - dt.year) * 12 + now.month - dt.month
                if months_old > max_age_months:
                    stale_results.append(f"- {config['file']}:{i} ({months_old} months old, {last_updated}) - {row.get('name', row.get('id', 'Unknown'))}")
            except ValueError:
                stale_results.append(f"- {config['file']}:{i} (Invalid date format: {last_updated}) - {row.get('name', row.get('id', 'Unknown'))}")
                
    if not stale_results:
        return "All records are fresh!"
        
    return f"## Stale Records (>{max_age_months} months)\\n" + "\\n".join(stale_results)

def compare_items('''
    
    content = content.replace("def compare_items(", stale_logic)
    
    arg_add = '''    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--stale", action="store_true", help="Check for stale records")
    parser.add_argument("--max-age-months", type=int, default=18, help="Threshold for stale check (months)")'''
    
    content = content.replace('    parser.add_argument("--json", action="store_true", help="Output JSON")', arg_add)
    
    exec_logic = '''    if args.stale:
        print(check_stale(args.domain, args.max_age_months))
        return
        
    if args.architecture:'''
    
    content = content.replace('    if args.architecture:', exec_logic)
    
    path.write_text(content, encoding='utf-8')
    print(f"Updated {path}")

add_freshness_to_search('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/scripts/search.py')
add_freshness_to_search('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/cli/assets/skill/scripts/search.py')
