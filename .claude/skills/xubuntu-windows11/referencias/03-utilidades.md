# C. Utilidades propias

`S` = carpeta de la skill. Requieren `xdotool`, `xclip` (B1) y `xfce4-screenshooter` (viene en Xubuntu).

## C1. Recortes / capturas estilo Windows (Win+Shift+S)
Captura **sin abrir la app**: guarda en `~/Imágenes/Capturas/Captura AAAA-MM-DD HH-MM-SS.png`, la **copia al portapapeles**
(lista para Ctrl+V) y muestra una notificación con miniatura. Esc durante el recorte = cancelar sin guardar.
```bash
cp $S/archivos/bin/captura ~/.local/bin/ && chmod +x ~/.local/bin/captura
xfconf-query -c xfce4-keyboard-shortcuts -l -v | grep -iE "print|<Super><Shift>s" > ~/backups/$(date +%F)/atajos-capturas.txt
k(){ xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/$1" -n -t string -s "$2" 2>/dev/null || xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/$1" -s "$2"; }
C=$HOME/.local/bin/captura
k "<Super><Shift>s" "$C recorte"; k "<Shift>Print" "$C recorte"; k "Print" "$C pantalla"; k "<Alt>Print" "$C ventana"
```
Por defecto Xubuntu tenía `Print → xfce4-screenshooter -f`, que captura y luego **abre la ventana** de la app (lo que no se quería).
Verificar con `xdotool key Print` → nuevo PNG en Capturas y `xclip -o -selection clipboard -t TARGETS` incluye `image/png` (borrar la captura de prueba).

## C2. Portapapeles — historial con Win+V (app propia)
App Python + GTK3 (`archivos/portapapeles/portapapeles.py`), estilo Win11, sigue el tema claro/oscuro:
- Servicio en segundo plano (`Gtk.Application` única) que guarda **texto e imágenes** copiados (incluye las capturas de C1); últimas 50 + fijadas,
  sin duplicados (lo repetido sube arriba), persiste en `~/.local/share/portapapeles/historial.json` + `imagenes/`.
  Ignora lo marcado como contraseña (`x-kde-passwordManagerHint`).
- **Win+V** abre una ventana flotante redondeada junto al puntero: buscador, tarjetas (texto en 3 líneas / miniatura + hora), 📌 fijar, ✕ borrar,
  "Borrar todo" (respeta las fijadas). **Clic o Enter pega directamente** en la ventana donde se estaba (`xdotool key ctrl+v`;
  `ctrl+shift+v` en terminales). Flechas para moverse, Esc o clic fuera para cerrar.
```bash
mkdir -p ~/.local/share/portapapeles ~/.local/share/icons/hicolor/scalable/apps ~/.config/autostart
cp $S/archivos/portapapeles/portapapeles.py ~/.local/share/portapapeles/
cp $S/archivos/bin/portapapeles ~/.local/bin/ && chmod +x ~/.local/bin/portapapeles ~/.local/share/portapapeles/portapapeles.py
cp $S/archivos/iconos/portapapeles.svg ~/.local/share/icons/hicolor/scalable/apps/portapapeles.svg   # el menú NO lo muestra con ruta absoluta
[ -f ~/.local/share/icons/hicolor/index.theme ] || cp /usr/share/icons/hicolor/index.theme ~/.local/share/icons/hicolor/
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor
sed "s|@HOME@|$HOME|g" $S/archivos/desktop/portapapeles.desktop > ~/.local/share/applications/portapapeles.desktop
sed "s|@HOME@|$HOME|g" $S/archivos/desktop/autostart-portapapeles.desktop > ~/.config/autostart/portapapeles.desktop
update-desktop-database ~/.local/share/applications
xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/<Super>v" -n -t string -s "$HOME/.local/bin/portapapeles --mostrar"
# xfce4-clipman competiría con el Portapapeles: desactivar su autoarranque
cp /etc/xdg/autostart/xfce4-clipman-plugin-autostart.desktop ~/.config/autostart/ 2>/dev/null
CM=~/.config/autostart/xfce4-clipman-plugin-autostart.desktop
[ -f $CM ] && { grep -q '^Hidden=' $CM && sed -i 's/^Hidden=.*/Hidden=true/' $CM || echo 'Hidden=true' >> $CM; }
pkill -x xfce4-clipman 2>/dev/null
(setsid ~/.local/bin/portapapeles >/dev/null 2>&1 &)
```
Pruebas: copiar 2–3 textos con `xclip -selection clipboard` y ver `historial.json`; probar el pegado sobre `zenity --entry` (Win+V, ↓, Enter, y leer la
salida de zenity), **no** sobre Mousepad (se une a ventanas existentes). Al terminar, vaciar el historial de prueba: detener el servicio, poner `[]` en
`historial.json`, borrar `imagenes/*.png` y arrancarlo de nuevo.
Reiniciar el servicio: `pkill -f "^python3 .*portapapeles\.py"` (no `pkill -f portapapeles.py`: mata la propia shell).
Quitarla: borrar `~/.local/share/portapapeles`, `~/.local/bin/portapapeles`, los dos `.desktop`, el icono y el atajo `<Super>v`.
