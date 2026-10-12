# Contrato para agentes

Esta página resume cómo debe operar cualquier agente que use Winux Kit.

## Fuente de verdad

Carga `.claude/skills/xubuntu-windows11/SKILL.md` antes de configurar un computador. Después, lee únicamente la referencia correspondiente al módulo elegido.

## Reglas obligatorias

1. Inspeccionar `/etc/os-release`, escritorio, tipo de sesión, monitores y paquetes antes de modificar nada.
2. Esta skill apunta a Xubuntu/XFCE sobre X11. No aplicarla a ciegas en GNOME, KDE, Wayland u otra distribución.
3. Preguntar módulos, escala, tema inicial y aplicaciones opcionales.
4. Respaldar toda configuración de usuario o sistema antes de tocarla y dejar instrucciones legibles de restauración.
5. No borrar perfiles de navegador, archivos personales, particiones ni datos del usuario sin confirmación explícita.
6. Simular primero cualquier eliminación de paquetes. No ejecutar `apt autoremove` como parte del proceso.
7. Explicar cada acción privilegiada y usar el flujo de autorización gráfica documentado.
8. Informar el origen antes de descargar o ejecutar instaladores de terceros.
9. Verificar cada función instalada y explicar cómo revertirla.
10. No pedir, guardar ni publicar claves, tokens o datos privados de cuentas.

## Mantenimiento del repositorio

- Mantener una sola copia canónica en `.claude/skills/xubuntu-windows11/`.
- Ejecutar `./scripts/check.sh` antes de publicar cambios.
- Actualizar README y guías cuando cambien comportamiento o dependencias.
- Mantener el español como idioma principal de cara al usuario.
