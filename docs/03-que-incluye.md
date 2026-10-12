# Qué incluye Winux Kit

La implementación vive en `.claude/skills/xubuntu-windows11/` y está dividida en cuatro módulos.

## A. Apariencia

Referencia: `referencias/01-apariencia.md`

- Tema Fluent claro y oscuro.
- Iconos inspirados en Windows 11 y cursores Fluent.
- Fondos propios claro/oscuro.
- Acento azul y tipografía Inter.
- Escala 100 % o 125 %.
- Barra inferior de XFCE con aplicaciones centradas.
- Menú Whisker en diseño clásico.
- Thunar en vista detallada, con carpetas primero.
- Carpetas personales en español.
- Botón y atajo para cambiar tema sin cerrar las ventanas.

## B. Aplicaciones

Referencia: `referencias/02-apps.md`

- Brave como navegador predeterminado.
- ONLYOFFICE para documentos, hojas de cálculo y presentaciones.
- LibreWolf como navegador alternativo.
- WhatsApp Web como aplicación de escritorio.
- Gestor gráfico de varias cuentas de WhatsApp, cada una con nombre e icono.
- Mini-STT opcional para dictado local en español.
- Syncthing y Telegram como opciones adicionales.

Algunas decisiones, como eliminar Firefox o LibreOffice, requieren comprobar datos existentes y confirmación del usuario.

## C. Utilidades

Referencia: `referencias/03-utilidades.md`

### Capturas

- `Super + Shift + S`: seleccionar región.
- `Print`: pantalla completa.
- `Alt + Print`: ventana activa.
- Guarda el PNG y lo copia al portapapeles.

### Portapapeles

- `Super + V`: historial flotante.
- Texto e imágenes.
- Búsqueda, fijados y eliminación.
- Hasta 50 elementos no fijados.
- Evita duplicados.
- Ignora contenido marcado por aplicaciones como contraseña.

## D. Sistema

Referencia: `referencias/04-sistema.md`

Todos estos cambios son opcionales:

- Desactivar ahorro de energía del WiFi para reducir picos de latencia.
- Configurar BBR y buffers de red.
- Ajustar roles Bluetooth para que parlantes y audífonos funcionen como salidas.
- Evitar suspensión agresiva del audio Bluetooth.
- Activar journal persistente y `rasdaemon` para diagnóstico.
- Procedimientos de reversión por módulo.

## Archivos incluidos

- `archivos/bin/`: utilidades ejecutables.
- `archivos/desktop/`: lanzadores y autoarranque.
- `archivos/gtk-3.0/`: ajustes visuales.
- `archivos/iconos/`: recursos SVG propios o adaptados para este proyecto.
- `archivos/portapapeles/`: aplicación GTK del historial.
- `archivos/sistema/`: fragmentos de NetworkManager, sysctl y WirePlumber.

## Dependencias externas

Winux Kit no redistribuye los proyectos externos. La skill los instala desde sus fuentes:

- Fluent GTK Theme.
- Win11 Icon Theme.
- Fluent Icon Theme/cursors.
- Brave.
- ONLYOFFICE.
- LibreWolf.
- Mini-STT.

Cada proyecto mantiene sus propios términos y licencia.
