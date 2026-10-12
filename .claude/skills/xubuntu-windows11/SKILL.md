---
name: xubuntu-windows11
description: Deja un Xubuntu (XFCE 4.20, X11) como un PC con Windows 11 bien armado — look Win11 (tema Fluent, iconos Win11, barra centrada, Explorador en lista, modo claro/oscuro intercambiable con botón 🌙), apps (Brave, ONLYOFFICE, LibreWolf, WhatsApp como app con varias cuentas, Mini-STT, opcionales Syncthing/Telegram), utilidades propias (recortes con Win+Shift+S, historial del portapapeles con Win+V) y ajustes de sistema (WiFi, Bluetooth/audio, diagnóstico). Úsalo cuando pidan "que este PC parezca/funcione como Windows 11", "replicar el setup de Xubuntu", "instalar lo mismo que en el otro PC" o una parte (p. ej. "pon el historial del portapapeles", "las cuentas de WhatsApp").
version: 1.0.0
author: KINTO / Mago Digital
license: MIT
repository: https://github.com/1511170/winux-kit
---

# Xubuntu → PC estilo Windows 11

Replica un setup probado en un portátil de 14" con Intel UHD 620 y en un PC de escritorio Ryzen 5700G con monitor 24" 2560×1440
(Xubuntu/Ubuntu 26.04 LTS, XFCE 4.20, X11, PipeWire). Todo es por usuario
(`~/.themes`, `~/.local/...`, xfconf) salvo instalar paquetes y los ajustes de `/etc`.

## Cómo está organizada
| Parte | Archivo | Contenido |
|---|---|---|
| A. Apariencia | `referencias/01-apariencia.md` | Tema Fluent, iconos Win11, barra, menú, Thunar, carpetas, escala, **claro/oscuro** |
| B. Apps | `referencias/02-apps.md` | Brave, ONLYOFFICE, LibreWolf, **WhatsApp + cuentas**, **Mini-STT**, opcionales |
| C. Utilidades | `referencias/03-utilidades.md` | **Recortes** (Win+Shift+S), **Portapapeles** (Win+V) |
| D. Sistema | `referencias/04-sistema.md` | WiFi, Bluetooth/audio, diagnóstico, respaldos |
| Archivos | `archivos/` | Copias exactas de lo que funciona: scripts, app, CSS, iconos, `.desktop`, confs |

Lee solo la referencia de la parte que vayas a hacer. Los archivos de `archivos/` se copian tal cual; en los `.desktop`
y en `bin/tema` hay marcadores que se reemplazan al instalar:
- `@HOME@` → `$HOME` (los `.desktop` no expanden variables): `sed -i "s|@HOME@|$HOME|g" archivo`
- `@MONITOR@` → nombre del monitor de `xrandr | awk '/ connected/{print $1; exit}'` (p. ej. `eDP-1`, `HDMI-A-1`)

## Antes de empezar (siempre)
1. **Preguntar** (AskUserQuestion, una sola vez): qué partes (A/B/C/D, por defecto todas); **escala** 125 % (pantalla chica o persona
   mayor) o 100 % (monitor grande); modo inicial claro u oscuro; opcionales (Syncthing, Telegram, Mini-STT).
2. Entorno: `cat /etc/os-release`, `echo $XDG_CURRENT_DESKTOP $XDG_SESSION_TYPE` (XFCE / x11), `xrandr | grep -w connected`, `snap list`.
3. **Root sin terminal**: `sudo` no funciona (no hay TTY). Usar **`pkexec`** (ventana gráfica de contraseña, hay agente polkit) y agrupar
   todo lo de root en **una** llamada `pkexec bash -c '...'` con timeout ≥ 180 s. Lo largo (snap de 1 GB) en segundo plano.
4. **Respaldos** antes de tocar nada: `mkdir -p ~/backups/$(date +%F)`; copiar `~/.config/xfce4`, `~/.config/user-dirs.dirs`, cada archivo
   de `/etc` que se edite y los atajos (`xfconf-query -c xfce4-keyboard-shortcuts -l -v`). Dejar un `LEEME.txt` y un `revertir.sh` por parte.
5. Si la carpeta personal tiene archivos, **preguntar** antes de renombrar carpetas o borrar Firefox con datos.

## Orden recomendado
D (respaldos, pkexec) → B paquetes (una ventana de contraseña) → A (apariencia) → B resto (WhatsApp, Mini-STT) → C → D ajustes →
cerrar sesión y volver a entrar una vez.

## Decisiones ya tomadas por los usuarios (no volver a preguntar)
- Acento azul `#0067C0`. Barra **abajo, centrada**, 48 px, **una sola barra**, sin widget del clima.
- Menú Whisker en **diseño clásico** (el "tipo Win11" con cuadrícula fue rechazado).
- Explorador en **vista lista** en todas las carpetas. Carpetas personales **en español**.
- **ONLYOFFICE** en vez de LibreOffice; **Brave** navegador por defecto; **sin Firefox**.
- El modo claro/oscuro debe ser **intercambiable** (botón 🌙), no fijo. Cambiar de tema **no debe cerrar ventanas**.
- WhatsApp: la barra debe **minimizar/restaurar** la misma ventana (nunca abrir otra) y los links deben abrir en el **Brave normal**.
- Todo lo que se pueda hacer, lo hace Claude; al usuario solo se le pide la contraseña (pkexec) o lo que el auto mode bloquee.

## Errores conocidos (evitarlos)
1. **`install.sh` bajados de GitHub** (tema Fluent, iconos Win11, cursores): el auto mode de Claude Code los bloquea como "código externo",
   aunque el usuario lo autorice en el chat, y tampoco se puede crear uno mismo la regla de permiso. → Pedir al usuario que corra cada línea con `!`.
2. `xfconf-query -c xfce4-panel -p /panels -rR` borra toda la config del panel. Nunca usar `-R` sobre `/panels`.
3. Dos paneles superpuestos para centrar = iconos opacos y clics bloqueados. Usar separadores elásticos 2:1.
4. `docklike-11.rc` **solo** se edita con el panel detenido (`xfce4-panel -q`, editar, `xfce4-panel`); si no, docklike lo sobrescribe y pierde anclados.
5. `gtk.css` se lee al abrir cada app: **nunca** copiar un CSS distinto por tema; usar uno solo con colores del tema (`@theme_fg_color`…).
6. Brave en modo "GTK" deja la barra gris claro (Adwaita): usar **"Classic" + modo "Device"**. Brave abierto desde antes no se entera del
   modo oscuro → `brave://restart` (restaura pestañas; cerrarlo a mano las pierde si no está "continuar donde lo dejaste").
7. WhatsApp con `--user-data-dir` aparte → los links abren en un perfil vacío. Usar perfil de Brave (`--profile-directory`) y renombrar la clase.
8. NetworkManager lee `conf.d` en orden alfabético: un `99-…` pierde contra `default-wifi-powersave-on.conf`. Usar prefijo **`zz-`**.
9. `systemctl --user restart wireplumber` desconecta los parlantes Bluetooth; `systemctl restart bluetooth` puede dejar rfkill en soft-block
   (`rfkill unblock bluetooth && bluetoothctl power on`).
10. `pkill -f nombre.py` mata también la propia shell si su comando contiene ese texto: usar `pkill -f "^python3 .*nombre\.py"`.
11. `pkexec` lanzado en segundo plano con `( … &)` falla ("dead parents"): usar `run_in_background` de la herramienta.
12. Al probar pegados con xdotool, no abrir editores que ya tengan ventanas de otras sesiones (Mousepad se une a la existente): usar `zenity --entry`.

## Verificación final (con capturas)
- `xfce4-screenshooter -f -s <scratchpad>/shot.png` y leer la imagen (recortar con PIL). Los menús emergentes no salen en capturas: pedir confirmación.
- Barra centrada, iconos nítidos; botón 🌙 alterna claro/oscuro con Thunar abierto sin que se cierre; Win+V y Win+Shift+S funcionan;
  WhatsApp minimiza/restaura desde la barra; `xdg-mime query default x-scheme-handler/https` → brave.
