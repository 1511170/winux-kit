#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SKILL="$ROOT/.claude/skills/xubuntu-windows11"
FAILED=0

ok() { printf '✓ %s\n' "$1"; }
fail() { printf '✗ %s\n' "$1" >&2; FAILED=1; }

[ -f "$SKILL/SKILL.md" ] && ok "SKILL.md existe" || fail "Falta SKILL.md"
python3 - "$SKILL/SKILL.md" <<'PY' || FAILED=1
from pathlib import Path
import re, sys
p=Path(sys.argv[1]); text=p.read_text(encoding='utf-8')
if not text.startswith('---\n') or '\n---\n' not in text[4:]:
    raise SystemExit('✗ Frontmatter YAML ausente o inválido')
head=text.split('---',2)[1]
for key in ('name:', 'description:'):
    if key not in head:
        raise SystemExit(f'✗ Falta {key} en frontmatter')
print('✓ Frontmatter básico válido')
PY

while IFS= read -r -d '' file; do
  first=$(head -n 1 "$file" || true)
  case "$first" in
    *bash*)
      if bash -n "$file"; then ok "Bash: ${file#$ROOT/}"; else fail "Bash inválido: ${file#$ROOT/}"; fi
      ;;
    *python*)
      if python3 - "$file" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
compile(p.read_text(encoding='utf-8'), str(p), 'exec')
PY
      then ok "Python: ${file#$ROOT/}"; else fail "Python inválido: ${file#$ROOT/}"; fi
      ;;
  esac
done < <(find "$SKILL/archivos/bin" "$SKILL/archivos/portapapeles" "$ROOT/scripts" -type f -print0)

for required in README.md LICENSE SECURITY.md CONTRIBUTING.md docs/01-instalar-xubuntu.md docs/02-usar-con-agentes.md docs/03-que-incluye.md docs/04-contrato-agentes.md; do
  [ -s "$ROOT/$required" ] && ok "$required" || fail "Falta o está vacío: $required"
done

if grep -RInE --exclude='check.sh' '(gho_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|Bearer [A-Za-z0-9._-]{20,})' "$ROOT"; then
  fail "Posible secreto encontrado"
else
  ok "Sin patrones comunes de secretos"
fi

for placeholder in '@HOME@' '@MONITOR@'; do
  grep -Rqs "$placeholder" "$SKILL" && ok "Placeholder documentado: $placeholder" || fail "Falta placeholder esperado: $placeholder"
done

[ "$FAILED" -eq 0 ] || exit 1
printf '\nTodas las validaciones pasaron.\n'
