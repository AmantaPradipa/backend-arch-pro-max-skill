# Backend Arch Pro Max Test Report

Date: 2026-04-27

## Commands Run

```powershell
python C:\Users\USER\.codex\skills\.system\skill-creator\scripts\quick_validate.py backend-arch-pro-max-skill
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\src\backend-arch-pro-max\data\_sync_all.py
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest backend-arch-pro-max-skill\tests\test_search.py
$env:PYTHONDONTWRITEBYTECODE='1'; python -c "import ast,pathlib; ast.parse(pathlib.Path('backend-arch-pro-max-skill/scripts/search.py').read_text(encoding='utf-8')); ast.parse(pathlib.Path('backend-arch-pro-max-skill/src/backend-arch-pro-max/data/_sync_all.py').read_text(encoding='utf-8')); print('python syntax ok')"
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\scripts\search.py "jwt refresh token rbac tenant" --domain security -n 3 --json
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\scripts\search.py "cursor pagination rest api" --domain api -n 3
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\scripts\search.py "nestjs service repository transaction" --stack nestjs -n 3
node backend-arch-pro-max-skill\cli\bin\backend-arch-pro-max.js list
node backend-arch-pro-max-skill\cli\bin\backend-arch-pro-max.js init --ai codex --target backend-arch-pro-max-skill\test-output\install --force
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\scripts\search.py "billing webhook payments idempotency postgres queue" --architecture --persist -p "Billing API Test" --service "Webhook Worker" -o backend-arch-pro-max-skill\test-output\persist
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\test-output\install\.codex\skills\backend-arch-pro-max\scripts\search.py "n+1 query repository" --domain anti-patterns -n 2
node -c backend-arch-pro-max-skill\cli\bin\backend-arch-pro-max.js
```

## Results

- Skill metadata validation: PASS.
- CSV validator: PASS, total 295 rows.
- Python syntax parse for `search.py` and `_sync_all.py`: PASS.
- Unit tests: PASS.
- Security JSON search: PASS.
- API domain search: PASS.
- NestJS stack search: PASS.
- CLI list: PASS.
- CLI real install into `test-output/install`: PASS.
- Persist architecture write into `test-output/persist`: PASS.
- Search from installed copy: PASS.
- Node syntax check for CLI installer: PASS.

## Notes

- PowerShell prints a constrained-language `OutputEncoding` warning before command output. The tested commands still exit successfully.
- Unit tests may skip the persist temp-dir test when the environment does not expose a writable system temp directory. The persist write path was tested separately with an explicit output folder and passed.
