# Usar Winux Kit con agentes

Winux Kit está diseñado para que un agente lea la skill, inspeccione el computador y aplique únicamente los módulos elegidos.

## Opción recomendada: Claude Code

Claude Code suele ofrecer la experiencia más consistente para una configuración larga y guiada.

### Instalar

Consulta siempre la guía oficial vigente: <https://code.claude.com/docs/en/setup>

En Linux, Anthropic ofrece un instalador nativo. Si ya tienes Node.js, también puedes usar el método npm documentado oficialmente.

Después de instalar:

```bash
claude --version
claude doctor
```

Inicia sesión siguiendo las instrucciones de Claude Code.

### Ejecutar Winux Kit

```bash
git clone https://github.com/1511170/winux-kit.git
cd winux-kit
claude
```

Prompt sugerido:

```text
Carga la skill xubuntu-windows11. Antes de modificar el equipo, revisa sistema,
sesión gráfica, monitor y paquetes. Crea respaldos. Quiero todos los módulos,
escala 125 %, modo oscuro inicial, Mini-STT y Telegram. Explícame cada solicitud
de contraseña y verifica el resultado al terminar.
```

Puedes pedir solo una parte:

```text
Usa la skill xubuntu-windows11, pero instala únicamente el historial del
portapapeles con Super+V. No cambies temas ni aplicaciones.
```

## Alternativa: OpenCode

OpenCode es un agente de terminal de código abierto. Puede conectarse a numerosos proveedores y modelos locales. Su catálogo Zen incluye modelos promocionales; **Big Pickle puede ser gratuito por tiempo limitado**, no de manera garantizada o permanente.

- Inicio: <https://opencode.ai/docs/>
- Modelos: <https://opencode.ai/docs/models/>
- OpenCode Zen: <https://opencode.ai/docs/zen/>
- Skills: <https://opencode.ai/docs/skills/>

Instala OpenCode siguiendo su documentación oficial vigente y luego:

```bash
git clone https://github.com/1511170/winux-kit.git
cd winux-kit
opencode
```

OpenCode descubre skills dentro de `.claude/skills/`, por lo que puede cargar `xubuntu-windows11` directamente.

Antes de empezar, configura un proveedor/modelo dentro de OpenCode. Los modelos gratuitos y sus límites cambian; comprueba el catálogo actual con las herramientas del propio OpenCode.

## Instalar la skill para cualquier carpeta

```bash
git clone https://github.com/1511170/winux-kit.git
cd winux-kit
./scripts/install-skill.sh
```

La skill queda en:

```text
~/.claude/skills/xubuntu-windows11/
```

Para copiarla dentro de otro proyecto:

```bash
./scripts/install-skill.sh --project ~/mi-proyecto
```

## Qué debe hacer el agente antes de cambiar el sistema

El agente debe:

1. comprobar distribución, XFCE y X11;
2. detectar monitor y escala adecuada;
3. preguntar qué módulos quieres;
4. revisar si hay perfiles o documentos que podrían borrarse;
5. crear respaldo de XFCE, accesos y archivos que vaya a tocar;
6. agrupar operaciones administrativas;
7. explicar las ventanas de autorización;
8. verificar cada módulo y dejar instrucciones de reversión.

## Qué no debes aceptar a ciegas

Detente si el agente intenta:

- borrar el perfil de Firefox sin revisar si tiene datos;
- ejecutar `apt autoremove` como parte de esta instalación;
- borrar toda la configuración del panel XFCE;
- aplicar comandos hechos para XFCE/X11 sobre GNOME, KDE o Wayland;
- tocar particiones, cuentas o archivos personales como parte de la personalización;
- continuar después de un error de paquetes sin explicar el estado.

## Privacidad

La skill no requiere claves privadas, tokens ni credenciales. WhatsApp se vincula mediante QR en cada computador. Mini-STT procesa voz localmente según la configuración de su proyecto.
