<div align="center">

# Winux Kit

**Un escritorio familiar como Windows 11, con la libertad de Xubuntu.**

Una skill pública para que agentes como Claude Code u OpenCode conviertan Xubuntu/XFCE en un escritorio moderno, práctico y fácil de usar.

[Instalación](#inicio-rápido) · [Qué incluye](docs/03-que-incluye.md) · [Preparar Xubuntu](docs/01-instalar-xubuntu.md) · [Usar agentes](docs/02-usar-con-agentes.md)

</div>

---

## ¿Qué es Winux Kit?

Winux Kit es una guía operativa para agentes de programación. No es una distribución de Linux ni una imagen modificada: es una **skill reproducible** que documenta cómo configurar Xubuntu con una experiencia inspirada en Windows 11.

El agente inspecciona el computador, pregunta qué módulos instalar, crea respaldos y ejecuta la configuración por etapas. La skill incluye instrucciones, scripts, accesos `.desktop`, estilos, iconos propios y procedimientos de reversión.

Fue probado en equipos reales con XFCE/X11 y está pensado para personas que quieren migrar desde Windows sin perder una interfaz familiar.

## Qué puede configurar

- Apariencia clara/oscura inspirada en Windows 11.
- Barra inferior centrada, menú de inicio y explorador Thunar en vista de lista.
- Brave y ONLYOFFICE como aplicaciones principales.
- WhatsApp Web como aplicación, con soporte para varias cuentas y marcas.
- Capturas con `Super + Shift + S`.
- Historial de portapapeles con `Super + V`.
- Dictado local opcional mediante Mini-STT.
- Ajustes opcionales de WiFi, Bluetooth, PipeWire y diagnóstico.
- Respaldos y procedimientos de reversión antes de modificar el sistema.

El inventario completo está en [docs/03-que-incluye.md](docs/03-que-incluye.md).

## Requisitos

- **Xubuntu 26.04 LTS, 64 bits**, recomendado. También puede funcionar en versiones cercanas, pero los comandos fueron documentados para XFCE 4.20, X11 y PipeWire.
- Sesión gráfica **XFCE sobre X11**.
- Conexión a internet.
- Una cuenta con permisos administrativos para autorizar ventanas de `pkexec`.
- Claude Code —recomendado— u OpenCode.

Si el computador todavía tiene Windows, empieza por [Instalar Xubuntu desde una USB](docs/01-instalar-xubuntu.md).

## Inicio rápido

### 1. Descargar el repositorio

```bash
git clone https://github.com/1511170/winux-kit.git
cd winux-kit
```

### 2. Abrir un agente

Con Claude Code:

```bash
claude
```

Con OpenCode:

```bash
opencode
```

### 3. Pedir la configuración

Ejemplo recomendado:

```text
Usa la skill xubuntu-windows11 de este repositorio. Primero revisa mi sistema,
explícame qué vas a cambiar, crea respaldos y ayúdame a instalar todos los
módulos de Winux Kit. Quiero escala 125 % y modo oscuro inicial.
```

La skill está en:

```text
.claude/skills/xubuntu-windows11/SKILL.md
```

OpenCode también descubre skills ubicadas en `.claude/skills/`, por lo que no se mantiene una segunda copia que pueda quedar desactualizada.

Consulta la guía detallada: [docs/02-usar-con-agentes.md](docs/02-usar-con-agentes.md).

## Instalar la skill globalmente

Si quieres usar Winux Kit desde cualquier carpeta:

```bash
./scripts/install-skill.sh
```

Esto instala la skill en `~/.claude/skills/xubuntu-windows11`. Claude Code y las versiones actuales de OpenCode pueden descubrirla allí.

Para instalarla únicamente dentro de otro proyecto:

```bash
./scripts/install-skill.sh --project /ruta/al/proyecto
```

## Estructura

```text
.
├── .claude/skills/xubuntu-windows11/
│   ├── SKILL.md                 # contrato principal del agente
│   ├── referencias/             # apariencia, apps, utilidades y sistema
│   └── archivos/                # scripts, iconos, CSS y configuraciones
├── docs/
│   ├── 01-instalar-xubuntu.md
│   ├── 02-usar-con-agentes.md
│   └── 03-que-incluye.md
├── scripts/
│   ├── install-skill.sh
│   └── check.sh
├── docs/04-contrato-agentes.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

## Seguridad y alcance

Winux Kit modifica configuración del usuario y, en módulos opcionales, archivos del sistema. Por eso la skill exige:

1. inspeccionar el entorno antes de actuar;
2. crear respaldos;
3. mostrar los cambios relevantes;
4. pedir autorización gráfica para acciones administrativas;
5. no borrar perfiles o datos sin confirmación;
6. probar cada módulo y documentar cómo revertirlo.

Lee [SECURITY.md](SECURITY.md) antes de usarlo en un equipo con información importante.

## Para agentes

- [docs/04-contrato-agentes.md](docs/04-contrato-agentes.md) resume el contrato operativo.
- `SKILL.md` indica qué referencia cargar para cada módulo.
- Las acciones destructivas o de sistema nunca deben ejecutarse sin respaldo y contexto.
- No se debe aplicar a GNOME, KDE, Wayland u otra distribución como si fuera XFCE/X11.

## Autoría

Creado y mantenido por **KINTO** — [kinto.co](https://kinto.co)  
Compartido por **Mago Digital** — TikTok: [@mago.digital](https://www.tiktok.com/@mago.digital)

La idea es ayudar a más personas a adoptar Linux acompañadas por agentes de IA, con instrucciones claras y una experiencia menos intimidante.

## Licencia y marcas

El código y la documentación propia se publican bajo la [licencia MIT](LICENSE).

Este proyecto es independiente y no está afiliado con Microsoft, Canonical, Xubuntu, Anthropic, OpenCode, Brave, WhatsApp/Meta ni ONLYOFFICE. Los nombres y marcas pertenecen a sus respectivos propietarios. Los temas y programas de terceros conservan sus propias licencias y se descargan desde sus proyectos oficiales; no se redistribuyen aquí.
