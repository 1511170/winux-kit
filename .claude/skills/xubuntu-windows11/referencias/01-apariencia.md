# A. Apariencia Windows 11

`S` = carpeta de la skill (`.claude/skills/xubuntu-windows11`). Las funciones `x`, `q`, `P` se definen en un bloque y se reutilizan:
si se ejecuta en llamadas de shell separadas, **volver a definirlas**.

## A1. Paquetes de apariencia (dentro de la llamada única de pkexec de la parte B)
`git sassc gtk2-engines-murrine xfce4-docklike-plugin fonts-inter xdotool wmctrl xclip`

## A2. Tema, iconos y cursores
```bash
mkdir -p ~/.cache/win11-setup && cd ~/.cache/win11-setup
for r in vinceliuice/Fluent-gtk-theme yeyushengfan258/Win11-icon-theme vinceliuice/Fluent-icon-theme; do
  n=${r#*/}; curl -sL "https://codeload.github.com/$r/tar.gz/HEAD" -o $n.tgz
  mkdir -p $n && tar xzf $n.tgz -C $n --strip-components=1
done
```
**Los `install.sh` los bloquea el auto mode** → pedir al usuario que pegue estas 4 líneas, una por una, con `!`:
```
! cd ~/.cache/win11-setup/Fluent-gtk-theme && ./install.sh -c light -s standard --tweaks round -l
! cd ~/.cache/win11-setup/Fluent-gtk-theme && ./install.sh -c dark -s standard --tweaks round -l
! cd ~/.cache/win11-setup/Win11-icon-theme && ./install.sh -a
! cd ~/.cache/win11-setup/Fluent-icon-theme/cursors && ./install.sh
```
Resultado: `~/.themes/Fluent-round-{Light,Dark}`, `~/.local/share/icons/{Win11,Win11-dark,Fluent-cursors,Fluent-dark-cursors}`.
(No existe repo "Win11-cursors": los cursores Fluent son los estilo Win11.)

### Arreglos obligatorios a los iconos (en `Win11` **y** `Win11-dark`)
```bash
SRC=~/.cache/win11-setup/Win11-icon-theme/src/apps/scalable/file-manager.svg
mkdir -p ~/.local/share/icons/custom && cp $SRC ~/.local/share/icons/custom/win11-explorer.svg
for T in ~/.local/share/icons/Win11 ~/.local/share/icons/Win11-dark; do
  # a) Explorador = carpeta amarilla con pieza azul (como Win11)
  for n in org.xfce.thunar thunar Thunar system-file-manager file-manager user-file-manager thunar-filemanager; do
    for f in $(find $T \( -path "*apps*" -o -path "*preferences*" \) -name "$n.svg"); do rm -f "$f"; cp $SRC "$f"; done
  done
  # b) places 16/22/24 son monocromos → barra lateral de Thunar gris. Quitarlos:
  mkdir -p ~/.cache/win11-setup/places-mono/$(basename $T)
  for s in 16 22 24; do [ -d $T/places/$s ] && mv $T/places/$s ~/.cache/win11-setup/places-mono/$(basename $T)/$s; done
done
# c) SOLO en Win11 (claro): apagar/reiniciar vienen blancos (#f2f2f2) → invisibles en fondo claro. En Win11-dark se dejan blancos.
T=~/.local/share/icons/Win11
for f in $(find $T \( -name 'system-shutdown*.svg' -o -name 'system-reboot*.svg' -o -name 'system-log-out*.svg' -o -name 'system-lock-screen*.svg' -o -name 'xfsm-*.svg' -o -name 'system-suspend*.svg' \)); do
  if grep -qi 'f2f2f2\|dfdfdf' "$f"; then [ -L "$f" ] && { t=$(readlink -f "$f"); rm "$f"; cp "$t" "$f"; }; sed -i 's/#f2f2f2/#363636/Ig; s/#dfdfdf/#363636/Ig' "$f"; fi
done
gtk-update-icon-cache -f ~/.local/share/icons/Win11; gtk-update-icon-cache -f ~/.local/share/icons/Win11-dark
mkdir -p ~/.icons/default && printf '[Icon Theme]\nInherits=Fluent-cursors\n' > ~/.icons/default/index.theme
```
**Ojo:** `start-here.svg` del tema Win11 es una manzana de Apple → no usarlo; se usa `win11-start.svg` (A3).

## A3. Recursos propios (de `archivos/iconos/`)
```bash
cp $S/archivos/iconos/{win11-start,whatsapp,whatsapp-cuentas}.svg ~/.local/share/icons/custom/
mkdir -p ~/Imágenes/Fondos && cp $S/archivos/iconos/win11-bloom{,-dark}.svg ~/Imágenes/Fondos/   # hacer A4 antes (carpetas)
read W H < <(xrandr | awk '/\*/{split($1,a,"x"); print a[1], a[2]; exit}')
for f in win11-bloom win11-bloom-dark; do
python3 -c "import gi,os,sys;gi.require_version('GdkPixbuf','2.0');from gi.repository import GdkPixbuf;d=os.path.expanduser('~/Imágenes/Fondos/');GdkPixbuf.Pixbuf.new_from_file_at_size(d+sys.argv[1]+'.svg',int(sys.argv[2]),int(sys.argv[3])).savev(d+sys.argv[1]+'.png','png',[],[])" $f $W $H
done
```
(No hay rsvg-convert/ImageMagick: se rasteriza con GdkPixbuf. El "Bloom" es propio; el original de Microsoft tiene copyright.)

## A4. Carpetas en español
```bash
cd ~
for p in Desktop:Escritorio Documents:Documentos Downloads:Descargas Music:Música Videos:Vídeos Templates:Plantillas Public:Público Pictures:Imágenes; do
  a=${p%%:*}; b=${p##*:}; [ -d "$a" ] && [ ! -e "$b" ] && mv "$a" "$b"
done
cat > ~/.config/user-dirs.dirs <<'EOF'
XDG_DESKTOP_DIR="$HOME/Escritorio"
XDG_DOWNLOAD_DIR="$HOME/Descargas"
XDG_TEMPLATES_DIR="$HOME/Plantillas"
XDG_PUBLICSHARE_DIR="$HOME/Público"
XDG_DOCUMENTS_DIR="$HOME/Documentos"
XDG_MUSIC_DIR="$HOME/Música"
XDG_PICTURES_DIR="$HOME/Imágenes"
XDG_VIDEOS_DIR="$HOME/Vídeos"
EOF
echo es_ES > ~/.config/user-dirs.locale
xfdesktop --quit; sleep 1; rmdir ~/Desktop 2>/dev/null; (setsid xfdesktop >/dev/null 2>&1 &)   # xfdesktop recrea ~/Desktop
H=file://$HOME; mkdir -p ~/.config/gtk-3.0
printf '%s\n' "$H/Descargas Descargas" "$H/Documentos Documentos" "$H/Im%C3%A1genes Imágenes" "$H/M%C3%BAsica Música" "$H/V%C3%ADdeos Vídeos" > ~/.config/gtk-3.0/bookmarks
```
(No añadir "Escritorio" a bookmarks: sale duplicado.)

## A5. Apariencia general y escala
```bash
x(){ xfconf-query -c "$1" -p "$2" -n -t "$3" -s "$4" 2>/dev/null || xfconf-query -c "$1" -p "$2" -s "$4"; }
DPI=120   # 125 % (pantalla chica / persona mayor). Monitor grande: DPI=96 (100 %)
x xsettings /Gtk/FontName string "Inter 10"
x xsettings /Xft/DPI int $DPI
x xsettings /Xft/Antialias int 1
x xsettings /Xft/HintStyle string hintslight
x xsettings /Xft/RGBA string rgb
x xsettings /Gtk/CursorThemeSize int 30
x xfwm4 /general/title_font string "Inter Semi-Bold 10"
x xfwm4 /general/title_alignment string left
x xfwm4 /general/button_layout string "O|HMC"
x xfce4-desktop /desktop-icons/icon-size uint 64
x xfce4-desktop /desktop-icons/use-custom-font-size bool true
x xfce4-desktop /desktop-icons/font-size double 11
MON=$(xrandr | awk '/ connected/{print $1; exit}')
for ws in 0 1 2 3; do b=/backdrop/screen0/monitor$MON/workspace$ws
  x xfce4-desktop $b/image-style int 5; x xfce4-desktop $b/color-style int 0; done
```
Tema, iconos, cursor y fondo los pone el script `tema` (A10). Si aparece la notificación de Snap "Some required themes are missing" o
"Installing missing themes" pidiendo contraseña: es inofensiva (snapd-desktop-integration); se puede cancelar.

## A6. Barra de tareas (UNA sola barra, centrada)
Distribución de `panel-1` (abajo, 48 px):
`[16 sep][10 sep][1 Inicio][15 Buscar][11 docklike][12 sep][17 🌙 tema][5 bandeja][6 notif][7 batería][8 volumen][9 reloj][13 mostrar escritorio]`
**Centrado:** 2 separadores elásticos a la izquierda y 1 a la derecha (reparto 2:1). Revisar los IDs con `xfconf-query -c xfce4-panel -l -v`.
```bash
P=xfce4-panel; q(){ xfconf-query -c $P -p "$1" -n -t "$2" -s "$3" 2>/dev/null || xfconf-query -c $P -p "$1" -s "$3"; }
for i in 2 3 4; do xfconf-query -c $P -p /plugins/plugin-$i -r -R 2>/dev/null; done   # separador, tasklist, separador de Xubuntu
for i in 10 12 16; do q /plugins/plugin-$i string separator; q /plugins/plugin-$i/expand bool true; q /plugins/plugin-$i/style uint 0; done
q /plugins/plugin-11 string docklike
q /plugins/plugin-13 string showdesktop
q /plugins/plugin-15 string launcher
q /plugins/plugin-17 string launcher
mkdir -p ~/.config/xfce4/panel/launcher-15 ~/.config/xfce4/panel/launcher-17
printf '[Desktop Entry]\nType=Application\nName=Buscar\nExec=xfce4-popup-whiskermenu\nIcon=system-search\n' > ~/.config/xfce4/panel/launcher-15/buscar.desktop
sed "s|@HOME@|$HOME|g" $S/archivos/desktop/tema.desktop > ~/.config/xfce4/panel/launcher-17/tema.desktop
xfconf-query -c $P -p /plugins/plugin-15/items -rR 2>/dev/null; xfconf-query -c $P -p /plugins/plugin-15/items -n -a -t string -s buscar.desktop
xfconf-query -c $P -p /plugins/plugin-17/items -rR 2>/dev/null; xfconf-query -c $P -p /plugins/plugin-17/items -n -a -t string -s tema.desktop
xfconf-query -c $P -p /panels/panel-1/plugin-ids -rR
xfconf-query -c $P -p /panels/panel-1/plugin-ids -n -a $(for i in 16 10 1 15 11 12 17 5 6 7 8 9 13; do echo -t int -s $i; done)
q /panels/panel-1/position string "p=8;x=0;y=0"; q /panels/panel-1/position-locked bool true
q /panels/panel-1/length double 100; q /panels/panel-1/length-adjust bool true
q /panels/panel-1/size uint 48; q /panels/panel-1/icon-size uint 32; q /panels/panel-1/nrows uint 1
q /panels/panel-1/mode uint 0; q /panels/panel-1/background-style uint 0
q /plugins/plugin-9/mode uint 2; q /plugins/plugin-9/digital-layout uint 1                       # reloj en 2 líneas
q /plugins/plugin-9/digital-time-format string "%H:%M"; q /plugins/plugin-9/digital-date-format string "%d/%m/%Y"
q /plugins/plugin-9/digital-time-font string "Inter 10"; q /plugins/plugin-9/digital-date-font string "Inter 10"
```
### Apps ancladas (docklike) — con el panel DETENIDO
Docklike no encuentra los `.desktop` de Snap tras reiniciar → copiarlos a `~/.local/share/applications/`.
```bash
A=~/.local/share/applications; OO=onlyoffice-desktopeditors_onlyoffice-desktopeditors
cp /var/lib/snapd/desktop/applications/{brave_brave,$OO}.desktop $A/
sed -e 's|^Name=.*|Name=Explorador de archivos|' -e 's|^Name\[es\]=.*|Name[es]=Explorador de archivos|' -e 's|^Icon=.*|Icon=org.xfce.thunar|' /usr/share/applications/thunar.desktop > $A/thunar.desktop
update-desktop-database $A
xfce4-panel -q; sleep 2
cat > ~/.config/xfce4/panel/docklike-11.rc <<EOF
[user]
pinned=thunar;brave_brave;whatsapp-web;$OO;org.xfce.ristretto;
noWindowsListIfSingle=true
onlyDisplayVisible=false
onlyDisplayScreen=false
showPreviews=true
indicatorOrientation=0
indicatorStyle=0
inactiveIndicatorStyle=0
indicatorColorFromTheme=true
EOF
(setsid xfce4-panel >/dev/null 2>&1 &)
```
(`whatsapp-web` existe después de B4; si se hace antes, docklike lo ignora hasta que exista.)

## A7. Menú Inicio (Whisker, diseño clásico)
```bash
B=/plugins/plugin-1; w(){ q $B/$1 "$2" "$3"; }
w button-icon string "$HOME/.local/share/icons/custom/win11-start.svg"
w show-button-title bool false; w show-button-icon bool true
w view-mode int 1; w launcher-icon-size int 4; w category-icon-size int 2
w position-search-alternate bool true; w position-commands-alternate bool true; w position-categories-alternate bool false
w menu-width int 640; w menu-height int 700; w menu-opacity int 100; w default-category int 0
for c in settings lockscreen logout restart shutdown; do w show-command-$c bool true; done
for c in switchuser suspend hibernate menueditor profile; do w show-command-$c bool false; done
xfconf-query -c $P -p $B/favorites -rR 2>/dev/null
xfconf-query -c $P -p $B/favorites -n -a $(for d in brave_brave whatsapp-web thunar $OO org.xfce.ristretto org.xfce.Parole org.xfce.mousepad tema portapapeles xfce-settings-manager; do echo -t string -s $d.desktop; done)
```

## A8. Explorador (Thunar) estilo Windows 11
```bash
thunar -q 2>/dev/null; t(){ x thunar "$1" "$2" "$3"; }
t /default-view string ThunarDetailsView; t /last-view string ThunarDetailsView
t /misc-directory-specific-settings bool false
t /last-details-view-visible-columns string "THUNAR_COLUMN_NAME,THUNAR_COLUMN_DATE_MODIFIED,THUNAR_COLUMN_TYPE,THUNAR_COLUMN_SIZE"
t /last-details-view-fixed-columns bool false
t /last-details-view-zoom-level string THUNAR_ZOOM_LEVEL_50_PERCENT   # 100 % = filas enormes
t /last-icon-view-zoom-level string THUNAR_ZOOM_LEVEL_150_PERCENT
t /misc-date-style string THUNAR_DATE_STYLE_CUSTOM; t /misc-date-custom-style string "%d/%m/%Y %H:%M"
t /misc-folders-first bool true; t /last-sort-column string THUNAR_COLUMN_NAME; t /last-sort-order string GTK_SORT_ASCENDING
t /misc-use-csd bool true; t /last-menubar-visible bool false; t /last-statusbar-visible bool true
t /last-toolbar-visible-buttons string "back:1,forward:1,open-parent:1,reload:1,location-bar:1,search:1,view-switcher:1,menu:1,open-home:0,new-tab:0,new-window:0,toggle-split-view:0,undo:0,redo:0,zoom-out:0,zoom-in:0,zoom-reset:0,view-as-icons:0,view-as-detailed-list:0,view-as-compact-list:0"
t /misc-symbolic-icons-in-sidepane bool false; t /misc-symbolic-icons-in-toolbar bool true
t /shortcuts-icon-size string THUNAR_ICON_SIZE_24; t /last-side-pane string ThunarShortcutsPane
t /last-separator-position int 230; t /last-location-bar string ThunarLocationButtons
t /last-window-width int 1250; t /last-window-height int 780
t /misc-full-path-in-title bool false; t /misc-single-click bool false
```

## A9. CSS (barra + Thunar) — UNO SOLO para claro y oscuro
```bash
cp $S/archivos/gtk-3.0/gtk.css ~/.config/gtk-3.0/gtk.css
mkdir -p ~/.config/xfce4-docklike-plugin && sed -n '1,8p' ~/.config/gtk-3.0/gtk.css > ~/.config/xfce4-docklike-plugin/gtk.css
```
Usa `@theme_fg_color`, `@theme_base_color`, `@theme_selected_bg_color`: se adapta en vivo al cambiar de tema. **No** volver a la idea de copiar un
CSS por tema (GTK solo lee `gtk.css` al abrir la app → Thunar queda "a medias").

## A10. Modo claro / oscuro intercambiable (script `tema`)
```bash
mkdir -p ~/.local/bin; MON=$(xrandr | awk '/ connected/{print $1; exit}')
sed "s|@MONITOR@|$MON|g" $S/archivos/bin/tema > ~/.local/bin/tema && chmod +x ~/.local/bin/tema
sed "s|@HOME@|$HOME|g" $S/archivos/desktop/tema.desktop > ~/.local/share/applications/tema.desktop
xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/<Super><Shift>t" -n -t string -s "$HOME/.local/bin/tema"
~/.local/bin/tema oscuro    # o claro, según lo elegido
```
`tema claro|oscuro|(sin argumento = alterna)` cambia de una vez: tema GTK y xfwm4, iconos, cursores, `gsettings color-scheme`
(`prefer-dark`/`default`, lo leen las apps vía portal), enlaces de `~/.config/gtk-4.0`, fondo, recarga el panel y notifica. Estado en `~/.config/tema-actual`.
Accesos: botón 🌙 (plugin-17), menú "Cambiar tema claro/oscuro", Super+Shift+T. **No cierra ventanas.**

## A11. Que las apps sigan el tema
- **Brave** (y WhatsApp, que corre dentro): `brave://settings/appearance` → Tema **"Classic"** (no "GTK": deja la barra gris de Adwaita) y
  modo **"Device"** (pref `browser.theme.color_scheme2 = 0`). Si estaba abierto desde antes del modo oscuro: `brave://restart` (restaura pestañas).
  Para navegar a `brave://` hay que escribirlo en la barra con `xdotool` (desde la línea de comandos no abre páginas internas).
- **ONLYOFFICE**: `~/snap/onlyoffice-desktopeditors/current/.config/onlyoffice/DesktopEditors.conf` con `[General]` `UITheme=theme-system`
  (crearlo aunque nunca se haya abierto).

## A12. Aplicar
`xfce4-panel -r; xfdesktop --reload` y recomendar **cerrar sesión y volver a entrar** una vez.
Reversión: copiar el respaldo sobre `~/.config/xfce4`, tema `Greybird` / iconos `elementary-xfce`, DPI 96, `xfce4-panel -r`.
