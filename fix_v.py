import re

def fix_pkg(path_str):
    from pathlib import Path
    p = Path(path_str)
    if not p.exists(): return
    content = p.read_text(encoding='utf-8-sig') # Handle BOM if any
    content = re.sub(r'"version":\s*"[^"]+"', '"version": "0.2.0"', content)
    p.write_text(content, encoding='utf-8')
    print(f"Updated {p}")

fix_pkg('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/package.json')
fix_pkg('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/skill.json')
fix_pkg('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/cli/package.json')
fix_pkg('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/cli/assets/skill/skill.json')
