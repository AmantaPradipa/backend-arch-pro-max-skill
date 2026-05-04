import re
from pathlib import Path

def fix_args(path_str):
    path = Path(path_str)
    if not path.exists():
        return
        
    content = path.read_text(encoding='utf-8')
    content = re.sub(
        r'(parser\.add_argument\("--json",.*?\n)\s*parser\.add_argument\("--stale.*?\n\s*parser\.add_argument\("--max-age-months.*?\n\s*parser\.add_argument\("--stale.*?\n\s*parser\.add_argument\("--max-age-months.*?\n',
        r'\g<1>    parser.add_argument("--stale", action="store_true", help="Check for stale records")\n    parser.add_argument("--max-age-months", type=int, default=18, help="Threshold for stale check (months)")\n',
        content, flags=re.DOTALL
    )
    
    path.write_text(content, encoding='utf-8')

fix_args('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/scripts/search.py')
fix_args('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/cli/assets/skill/scripts/search.py')
