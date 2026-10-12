#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
SOURCE="$ROOT/.claude/skills/xubuntu-windows11"

usage() {
  cat <<'EOF'
Uso:
  ./scripts/install-skill.sh
  ./scripts/install-skill.sh --project /ruta/al/proyecto

Sin argumentos instala la skill en ~/.claude/skills/.
--project la instala en <proyecto>/.claude/skills/.
EOF
}

case "${1:-}" in
  "") TARGET="$HOME/.claude/skills/xubuntu-windows11" ;;
  --project)
    [ "$#" -eq 2 ] || { usage; exit 2; }
    PROJECT=$(cd "$2" 2>/dev/null && pwd) || { echo "No existe el proyecto: $2" >&2; exit 1; }
    TARGET="$PROJECT/.claude/skills/xubuntu-windows11"
    ;;
  -h|--help) usage; exit 0 ;;
  *) usage; exit 2 ;;
esac

[ -f "$SOURCE/SKILL.md" ] || { echo "No se encontró la skill en $SOURCE" >&2; exit 1; }
mkdir -p "$(dirname "$TARGET")"
if [ -e "$TARGET" ]; then
  BACKUP="${TARGET}.backup-$(date +%Y%m%d-%H%M%S)"
  mv "$TARGET" "$BACKUP"
  echo "Respaldo anterior: $BACKUP"
fi
cp -a "$SOURCE" "$TARGET"
printf 'Skill instalada en: %s\n' "$TARGET"
printf 'Abre Claude Code u OpenCode y pide: Usa la skill xubuntu-windows11.\n'
