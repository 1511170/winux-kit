#!/usr/bin/env python3
"""Portapapeles: historial de lo copiado (texto e imágenes) con ventana estilo Windows 11.

Uso:
  portapapeles            arranca el servicio en segundo plano
  portapapeles --mostrar  abre la ventana (atajo Super+V)
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, GdkPixbuf, Gio, GLib, Gtk, Pango  # noqa: E402

APP_ID = "co.camilo.Portapapeles"
DATA = os.path.expanduser("~/.local/share/portapapeles")
IMGS = os.path.join(DATA, "imagenes")
HIST = os.path.join(DATA, "historial.json")
MAX_ITEMS = 50          # sin contar los fijados
MAX_TEXT = 200_000      # caracteres
PASSWORD_HINT = "x-kde-passwordManagerHint"
TERMINALES = ("terminal", "kitty", "alacritty", "konsole", "tilix", "xterm", "wezterm", "foot")

CSS = b"""
.pp-ventana { background: transparent; }
.pp-marco {
  background-color: @theme_bg_color;
  border-radius: 12px;
  border: 1px solid alpha(@theme_fg_color, 0.12);
  padding: 12px;
}
.pp-titulo { font-weight: bold; font-size: 1.1em; }
.pp-vacio { color: alpha(@theme_fg_color, 0.55); padding: 40px 10px; }
list.pp-lista, .pp-lista { background: transparent; }
.pp-lista row { background: transparent; padding: 3px 0; outline: none; }
.pp-tarjeta {
  background-color: alpha(@theme_fg_color, 0.05);
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 10px 12px;
}
.pp-lista row:hover .pp-tarjeta { background-color: alpha(@theme_fg_color, 0.09); }
.pp-lista row:selected .pp-tarjeta { border-color: @theme_selected_bg_color;
  background-color: alpha(@theme_selected_bg_color, 0.15); }
.pp-lista row:selected label { color: @theme_fg_color; }
.pp-hora { font-size: 0.85em; color: alpha(@theme_fg_color, 0.55); }
.pp-acciones { opacity: 0.25; }
.pp-lista row:hover .pp-acciones, .pp-lista row:selected .pp-acciones { opacity: 1; }
.pp-acciones button { min-width: 26px; min-height: 26px; padding: 0; border-radius: 6px; }
.pp-fijado { color: @theme_selected_bg_color; }
"""


def ahora_txt(ts):
    t = time.localtime(ts)
    if time.strftime("%Y%m%d", t) == time.strftime("%Y%m%d"):
        return time.strftime("%H:%M", t)
    return time.strftime("%d/%m %H:%M", t)


def ventana_activa():
    try:
        wid = subprocess.run(["xdotool", "getactivewindow"], capture_output=True, text=True, timeout=2).stdout.strip()
        clase = subprocess.run(["xprop", "-id", wid, "WM_CLASS"], capture_output=True, text=True, timeout=2).stdout.lower()
        return wid, clase
    except Exception:
        return "", ""


class Historial:
    def __init__(self):
        os.makedirs(IMGS, exist_ok=True)
        self.items = []
        try:
            with open(HIST) as f:
                self.items = json.load(f)
        except Exception:
            self.items = []

    def guardar(self):
        tmp = HIST + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.items, f, ensure_ascii=False)
        os.replace(tmp, HIST)

    def agregar(self, item):
        # sin duplicados: si ya estaba, sube arriba (conserva si estaba fijado)
        previo = next((i for i in self.items if i["hash"] == item["hash"]), None)
        if previo:
            self.items.remove(previo)
            item["pinned"] = previo.get("pinned", False)
            item["id"] = previo["id"]
        self.items.insert(0, item)
        self.podar()
        self.guardar()

    def podar(self):
        libres = 0
        quedan = []
        for i in self.items:
            if i.get("pinned"):
                quedan.append(i)
            elif libres < MAX_ITEMS:
                quedan.append(i)
                libres += 1
        self.items = quedan
        self.limpiar_imagenes()

    def limpiar_imagenes(self):
        usadas = {i.get("img") for i in self.items if i["type"] == "image"}
        for f in os.listdir(IMGS):
            if f not in usadas:
                try:
                    os.remove(os.path.join(IMGS, f))
                except OSError:
                    pass

    def borrar(self, item_id):
        self.items = [i for i in self.items if i["id"] != item_id]
        self.limpiar_imagenes()
        self.guardar()

    def borrar_todo(self):
        self.items = [i for i in self.items if i.get("pinned")]
        self.limpiar_imagenes()
        self.guardar()

    def fijar(self, item_id):
        for i in self.items:
            if i["id"] == item_id:
                i["pinned"] = not i.get("pinned", False)
        self.guardar()


class Ventana(Gtk.Window):
    def __init__(self, app):
        super().__init__(title="Portapapeles")
        self.app = app
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_default_size(380, 500)
        self.set_icon_name("edit-paste")
        visual = self.get_screen().get_rgba_visual()
        if visual and self.get_screen().is_composited():
            self.set_visual(visual)
            self.set_app_paintable(True)
        self.get_style_context().add_class("pp-ventana")
        self.mostrada_en = 0

        marco = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        marco.get_style_context().add_class("pp-marco")
        self.add(marco)

        cab = Gtk.Box(spacing=8)
        titulo = Gtk.Label(label="Portapapeles", xalign=0)
        titulo.get_style_context().add_class("pp-titulo")
        cab.pack_start(titulo, True, True, 0)
        b_todo = Gtk.Button(label="Borrar todo")
        b_todo.set_relief(Gtk.ReliefStyle.NONE)
        b_todo.set_tooltip_text("Borra todo menos lo fijado")
        b_todo.connect("clicked", lambda *_: (self.app.hist.borrar_todo(), self.recargar()))
        cab.pack_end(b_todo, False, False, 0)
        marco.pack_start(cab, False, False, 0)

        self.buscar = Gtk.SearchEntry(placeholder_text="Buscar…")
        self.buscar.connect("search-changed", lambda *_: (self.lista.invalidate_filter(), self.seleccionar_primera()))
        marco.pack_start(self.buscar, False, False, 0)

        self.lista = Gtk.ListBox()
        self.lista.get_style_context().add_class("pp-lista")
        self.lista.set_selection_mode(Gtk.SelectionMode.BROWSE)
        self.lista.set_activate_on_single_click(True)
        self.lista.set_filter_func(self.filtro)
        self.lista.connect("row-activated", lambda _l, row: self.app.pegar(row.item))
        self.vacio = Gtk.Label(label="Lo que copies aparecerá aquí.\nCopia con Ctrl+C y abre esta lista con Win+V.")
        self.vacio.set_justify(Gtk.Justification.CENTER)
        self.vacio.get_style_context().add_class("pp-vacio")
        self.vacio.show()
        self.lista.set_placeholder(self.vacio)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.lista)
        marco.pack_start(scroll, True, True, 0)

        self.connect("key-press-event", self.tecla)
        self.connect("focus-out-event", self.foco_perdido)
        self.connect("delete-event", lambda *_: self.hide() or True)

    # --- contenido ---
    def filtro(self, row):
        q = self.buscar.get_text().strip().lower()
        if not q:
            return True
        it = row.item
        if it["type"] == "text":
            return q in it["text"].lower()
        return q in "imagen captura"

    def recargar(self):
        for r in self.lista.get_children():
            self.lista.remove(r)
        for it in self.app.hist.items:
            self.lista.add(self.fila(it))
        self.lista.show_all()
        self.seleccionar_primera()

    def fila(self, it):
        row = Gtk.ListBoxRow()
        row.item = it
        tarjeta = Gtk.Box(spacing=10)
        tarjeta.get_style_context().add_class("pp-tarjeta")
        izq = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        if it["type"] == "text":
            txt = it["text"].strip().replace("\t", "  ")
            lab = Gtk.Label(label=txt[:600], xalign=0)
            lab.set_line_wrap(True)
            lab.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
            lab.set_lines(3)
            lab.set_ellipsize(Pango.EllipsizeMode.END)
            lab.set_max_width_chars(36)
            izq.pack_start(lab, False, False, 0)
        else:
            try:
                pb = GdkPixbuf.Pixbuf.new_from_file_at_scale(os.path.join(IMGS, it["img"]), 280, 110, True)
                izq.pack_start(Gtk.Image.new_from_pixbuf(pb), False, False, 0)
            except GLib.Error:
                izq.pack_start(Gtk.Label(label="(imagen no disponible)", xalign=0), False, False, 0)
        hora = Gtk.Label(label=("📌 " if it.get("pinned") else "") + ahora_txt(it["time"]), xalign=0)
        hora.get_style_context().add_class("pp-hora")
        izq.pack_start(hora, False, False, 0)
        tarjeta.pack_start(izq, True, True, 0)

        acc = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        acc.get_style_context().add_class("pp-acciones")
        b_fijar = Gtk.Button.new_from_icon_name("view-pin-symbolic", Gtk.IconSize.BUTTON)
        b_fijar.set_relief(Gtk.ReliefStyle.NONE)
        b_fijar.set_tooltip_text("Desfijar" if it.get("pinned") else "Fijar (no se borra)")
        if it.get("pinned"):
            b_fijar.get_style_context().add_class("pp-fijado")
        b_fijar.connect("clicked", lambda *_: (self.app.hist.fijar(it["id"]), self.recargar()))
        b_borrar = Gtk.Button.new_from_icon_name("window-close-symbolic", Gtk.IconSize.BUTTON)
        b_borrar.set_relief(Gtk.ReliefStyle.NONE)
        b_borrar.set_tooltip_text("Borrar")
        b_borrar.connect("clicked", lambda *_: (self.app.hist.borrar(it["id"]), self.recargar()))
        acc.pack_start(b_fijar, False, False, 0)
        acc.pack_start(b_borrar, False, False, 0)
        tarjeta.pack_end(acc, False, False, 0)
        row.add(tarjeta)
        return row

    def filas_visibles(self):
        return [r for r in self.lista.get_children() if r.get_child_visible() and self.filtro(r)]

    def seleccionar_primera(self):
        v = self.filas_visibles()
        if v:
            self.lista.select_row(v[0])

    # --- mostrar / ocultar ---
    def mostrar(self):
        self.buscar.set_text("")
        self.recargar()
        self.realize()
        w, h = 380, 500
        disp = Gdk.Display.get_default()
        _s, px, py = disp.get_default_seat().get_pointer().get_position()
        mon = disp.get_monitor_at_point(px, py).get_workarea()
        x = min(max(px - w // 2, mon.x + 8), mon.x + mon.width - w - 8)
        y = min(max(py - 40, mon.y + 8), mon.y + mon.height - h - 8)
        self.move(x, y)
        self.resize(w, h)
        self.show_all()
        self.present_with_time(Gtk.get_current_event_time() or int(time.time()))
        self.mostrada_en = time.time()
        GLib.timeout_add(80, self.forzar_foco)
        self.buscar.grab_focus()

    def forzar_foco(self):
        gw = self.get_window()
        if gw:
            try:
                subprocess.Popen(["xdotool", "windowactivate", str(gw.get_xid())])
            except Exception:
                pass
        return False

    def foco_perdido(self, *_):
        if time.time() - self.mostrada_en > 0.5:
            self.hide()
        return False

    def tecla(self, _w, ev):
        k = ev.keyval
        if k == Gdk.KEY_Escape:
            self.hide()
            return True
        if k in (Gdk.KEY_Down, Gdk.KEY_Up):
            v = self.filas_visibles()
            if not v:
                return True
            sel = self.lista.get_selected_row()
            i = v.index(sel) if sel in v else -1
            i = min(i + 1, len(v) - 1) if k == Gdk.KEY_Down else max(i - 1, 0)
            self.lista.select_row(v[i])
            v[i].grab_focus()
            self.buscar.grab_focus_without_selecting()
            return True
        if k in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            sel = self.lista.get_selected_row()
            if sel:
                self.app.pegar(sel.item)
            return True
        return False


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        self.hist = None
        self.ventana = None
        self.ignorar_hash = None
        self.destino = ("", "")

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.hold()  # queda corriendo en segundo plano
        prov = Gtk.CssProvider()
        prov.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), prov, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.hist = Historial()
        self.ventana = Ventana(self)
        self.add_window(self.ventana)
        self.clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clip.connect("owner-change", self.cambio)

    def do_command_line(self, cl):
        args = cl.get_arguments()[1:]
        if "--mostrar" in args:
            self.destino = ventana_activa()
            self.ventana.mostrar()
        return 0

    # --- captura del portapapeles ---
    def cambio(self, clip, _ev):
        clip.request_targets(self.con_targets)

    def con_targets(self, clip, atoms, *_):
        nombres = [a.name() for a in (atoms or [])]
        if PASSWORD_HINT in nombres:
            return
        if any(n.startswith("image/") for n in nombres):
            clip.request_image(self.con_imagen)
        elif nombres:
            clip.request_text(self.con_texto)

    def con_texto(self, _clip, texto, *_):
        if not texto or not texto.strip():
            return
        texto = texto[:MAX_TEXT]
        h = "t:" + hashlib.sha1(texto.encode("utf-8", "replace")).hexdigest()
        if h == self.ignorar_hash:
            return
        self.hist.agregar({"id": uuid.uuid4().hex, "type": "text", "text": texto, "hash": h, "time": time.time(), "pinned": False})
        self.refrescar_si_visible()

    def con_imagen(self, _clip, pb, *_):
        if pb is None:
            return
        h = "i:" + hashlib.sha1(pb.get_pixels()).hexdigest()
        if h == self.ignorar_hash:
            return
        nombre = h[2:18] + ".png"
        ruta = os.path.join(IMGS, nombre)
        if not os.path.exists(ruta):
            pb.savev(ruta, "png", [], [])
        self.hist.agregar({"id": uuid.uuid4().hex, "type": "image", "img": nombre, "hash": h, "time": time.time(), "pinned": False})
        self.refrescar_si_visible()

    def refrescar_si_visible(self):
        if self.ventana.get_visible():
            self.ventana.recargar()

    # --- pegar ---
    def pegar(self, it):
        self.ignorar_hash = it["hash"]
        if it["type"] == "text":
            self.clip.set_text(it["text"], -1)
        else:
            try:
                self.clip.set_image(GdkPixbuf.Pixbuf.new_from_file(os.path.join(IMGS, it["img"])))
            except GLib.Error:
                return
        self.clip.store()
        self.ventana.hide()
        GLib.timeout_add(150, self.enviar_pegado)

    def enviar_pegado(self):
        wid, clase = self.destino
        tecla = "ctrl+shift+v" if any(t in clase for t in TERMINALES) else "ctrl+v"
        cmd = "xdotool key --clearmodifiers " + tecla
        if wid:
            cmd = f"xdotool windowactivate --sync {wid} 2>/dev/null; sleep 0.05; " + cmd
        subprocess.Popen(["sh", "-c", cmd])
        return False


if __name__ == "__main__":
    sys.exit(App().run(sys.argv))
