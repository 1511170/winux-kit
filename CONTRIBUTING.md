# Contribuir a Winux Kit

Gracias por ayudar a mejorar una migración a Linux más amigable.

## Antes de abrir un cambio

1. Explica el problema y la versión de Xubuntu/XFCE donde lo viste.
2. Evita incluir datos personales, perfiles, capturas con información privada o credenciales.
3. Conserva los cambios reversibles y documenta el rollback.
4. No agregues binarios, temas o assets de terceros si su licencia no permite redistribuirlos.
5. Mantén la documentación principal en español claro.

## Validación

```bash
./scripts/check.sh
```

Este comando valida sintaxis de Bash y Python, placeholders, frontmatter y ausencia de patrones comunes de secretos.

## Pull requests

Incluye:

- qué cambia;
- por qué es necesario;
- cómo se probó;
- versiones de Xubuntu/XFCE;
- cómo revertirlo;
- capturas solo si no contienen datos privados.
