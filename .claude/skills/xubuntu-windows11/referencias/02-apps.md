# B. Apps

`S` = carpeta de la skill. `A=~/.local/share/applications`.

## B1. Paquetes (UNA sola ventana de contraseña)
```bash
pkexec bash -c '
apt-get update -qq &&
DEBIAN_FRONTEND=noninteractive apt-get install -y git sassc gtk2-engines-murrine xfce4-docklike-plugin fonts-inter \
  xdotool wmctrl xclip python3-pil fonts-noto-color-emoji extrepo &&
extrepo enable librewolf && apt-get update -qq &&
DEBIAN_FRONTEND=noninteractive apt-get install -y librewolf &&
snap install brave &&
snap install onlyoffice-desktopeditors &&
DEBIAN_FRONTEND=noninteractive apt-get purge -y "libreoffice*" firefox &&
snap remove --purge firefox'
```
- Correr en **segundo plano** (`run_in_background`): ONLYOFFICE pesa ~1 GB y puede pasar de 10 min.
- Antes del purge, simular: `apt-get -s purge 'libreoffice*' firefox | grep ^Purg` y confirmar que no toca paquetes del escritorio.
- **NO** ejecutar `apt autoremove` (quitaba `grub-pc-bin` y `gstreamer1.0-gtk3`).
- Si el perfil de Firefox tiene datos (`logins.json`, `places.sqlite` grande) → **preguntar** si importarlos a Brave antes de borrar.
- Opcionales (solo si el usuario los pidió): `syncthing` (apt) y `snap install telegram-desktop`.

## B2. Brave por defecto
```bash
xdg-settings set default-web-browser brave_brave.desktop
xdg-mime default brave_brave.desktop text/html x-scheme-handler/http x-scheme-handler/https application/xhtml+xml x-scheme-handler/about x-scheme-handler/unknown
mkdir -p ~/.local/share/xfce4/helpers
cat > ~/.local/share/xfce4/helpers/custom-WebBrowser.desktop <<'EOF'
[Desktop Entry]
NoDisplay=true
Version=1.0
Encoding=UTF-8
Type=X-XFCE-Helper
X-XFCE-Category=WebBrowser
X-XFCE-CommandsWithParameter=/snap/bin/brave "%s"
Icon=brave_brave
Name=Brave
X-XFCE-Commands=/snap/bin/brave
EOF
grep -q '^WebBrowser=' ~/.config/xfce4/helpers.rc 2>/dev/null && sed -i 's/^WebBrowser=.*/WebBrowser=custom-WebBrowser/' ~/.config/xfce4/helpers.rc || echo 'WebBrowser=custom-WebBrowser' >> ~/.config/xfce4/helpers.rc
rm -f $A/firefox_firefox.desktop; rm -rf ~/snap/firefox
```
Tema de Brave: ver A11 (Classic + Device).

## B3. ONLYOFFICE por defecto para documentos
```bash
OO=onlyoffice-desktopeditors_onlyoffice-desktopeditors
xdg-mime default $OO.desktop application/vnd.openxmlformats-officedocument.wordprocessingml.document application/msword application/vnd.oasis.opendocument.text application/rtf application/vnd.openxmlformats-officedocument.spreadsheetml.sheet application/vnd.ms-excel application/vnd.oasis.opendocument.spreadsheet text/csv application/vnd.openxmlformats-officedocument.presentationml.presentation application/vnd.ms-powerpoint application/vnd.oasis.opendocument.presentation
D=~/snap/onlyoffice-desktopeditors/current/.config/onlyoffice; mkdir -p $D
[ -f $D/DesktopEditors.conf ] || printf '[General]\nUITheme=theme-system\n' > $D/DesktopEditors.conf   # sigue claro/oscuro
```

## B4. WhatsApp como app (cuenta 1)
Es WhatsApp Web en una ventana "app" de Brave (sin pestañas), con su icono en la barra que **minimiza/restaura la misma ventana**
y con los links abriéndose en el Brave normal.
```bash
cp $S/archivos/bin/whatsapp-app ~/.local/bin/ && chmod +x ~/.local/bin/whatsapp-app
sed "s|@HOME@|$HOME|g" $S/archivos/desktop/whatsapp-web.desktop > $A/whatsapp-web.desktop
update-desktop-database $A
```
Cómo funciona `whatsapp-app [N]` (no cambiarlo sin entender esto):
- Cuenta 1 = **perfil principal** de Brave (`--app=https://web.whatsapp.com/`) → los links abren en el Brave de siempre y no hay que escanear el QR
  si ya estaba logueado ahí. **No** usar `--user-data-dir` aparte (los links abrían en un perfil vacío).
- Docklike agrupa por la clase de la ventana ("Brave"), así que el script **renombra la clase** a `WhatsApp` con `xdotool set_window --class`.
  `StartupWMClass=WhatsApp` en el `.desktop`. Si la ventana ya existe, solo la activa: nunca abre dos.
- Tras `brave://restart` la ventana vuelve a la clase "Brave"; se corrige sola en el primer clic al icono.

## B5. Cuentas de WhatsApp (varias cuentas, una app por marca)
Gestor gráfico (GTK) para **crear, editar y borrar** cuentas. Cada cuenta N≥2 es un perfil de Brave `"WhatsApp N"` que abre
`whatsapp-app N` en `https://web.whatsapp.com/cuenta-N` (instancia única `web.whatsapp.com__cuenta-N`, clase `WhatsApp-N`), con **nombre e
icono propios** (logo de WhatsApp + emoji elegido con buscador en español; fuente Noto Color Emoji, licencia OFL), su `.desktop`
`whatsapp-web-N.desktop` en el menú y anclada en la barra.
```bash
cp $S/archivos/bin/whatsapp-cuentas ~/.local/bin/ && chmod +x ~/.local/bin/whatsapp-cuentas
sed "s|@HOME@|$HOME|g" $S/archivos/desktop/whatsapp-cuentas.desktop > $A/whatsapp-cuentas.desktop
update-desktop-database $A
```
- Requiere `python3-pil` y `fonts-noto-color-emoji` (B1) y el icono `~/.local/share/icons/custom/whatsapp.svg` (A3).
- El `.desktop` de cada cuenta es la única fuente de verdad (nombre e icono); iconos en `~/.local/share/whatsapp-cuentas/N/`.
- **No** se copian cuentas ni perfiles de otro PC: cada cuenta se vincula escaneando el QR desde el celular.

## B6. Mini-STT (dictado por voz local, opcional pero recomendado)
App de bandeja: Ctrl+Alt+Espacio, hablas en español, y el texto se pega donde está el cursor. 100 % local (Canary 1B v2 / faster-whisper).
Repo del usuario: `https://github.com/1511170/mini-stt`.
```bash
mkdir -p ~/DEVS && git clone https://github.com/1511170/mini-stt ~/DEVS/mini-stt
```
Luego **leer `~/DEVS/mini-stt/README.md`** y seguir la sección Linux: `install.sh` (crea `.venv` y baja el modelo) y `setup_autostart.sh`
(arranque al iniciar sesión con `run.sh --autostart`). Son scripts de un repo: si el auto mode los bloquea, pedirle al usuario que los corra con `!`.
Queda en el menú como "Mini-STT" (`run.sh`; acción "Cerrar Mini-STT" = `run.sh --stop`).

## B7. Opcionales
- **Syncthing**: `systemctl --user enable --now syncthing`; interfaz en `http://127.0.0.1:8384` (abrir en Brave para vincular dispositivos).
- **Telegram**: `snap install telegram-desktop` (en B1). Se puede anclar en la barra (con el panel detenido, ver A6).
- Fuera de esta skill: Tailscale, RustDesk.
