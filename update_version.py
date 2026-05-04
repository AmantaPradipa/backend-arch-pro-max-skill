import json
from pathlib import Path

def update_version(file_path):
    p = Path(file_path)
    if not p.exists():
        return
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['version'] = '0.2.0'
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\\n')
    print(f'Updated {file_path}')

update_version('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/package.json')
update_version('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/skill.json')
update_version('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/cli/package.json')
update_version('d:/Pemrograman/Agent-Skills/backend-arch-pro-max-skill/cli/assets/skill/skill.json')
