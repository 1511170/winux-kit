# Instalar Xubuntu antes de usar Winux Kit

Esta guía es para una persona que actualmente usa Windows y quiere preparar un computador para Winux Kit.

## 1. Qué sistema descargar

Recomendamos **Xubuntu 26.04 LTS de 64 bits**.

- Descarga oficial: <https://xubuntu.org/download/>
- Información de la versión: <https://xubuntu.org/release/26.04/>
- Es una versión LTS publicada en abril de 2026 y mantenida por el proyecto Xubuntu hasta abril de 2029.

Xubuntu combina Ubuntu con el escritorio XFCE. Es más liviano que otros escritorios y encaja con los procedimientos de esta skill.

## 2. Antes de instalar

1. Haz copia de seguridad de documentos, fotos, claves y archivos importantes.
2. Ten una memoria USB de al menos 8 GB. Su contenido será borrado.
3. Conecta el portátil a la corriente.
4. Decide si vas a:
   - reemplazar Windows por Xubuntu; o
   - conservar ambos sistemas mediante arranque dual.
5. Si dependes de programas exclusivos de Windows, verifica alternativas antes de borrar el sistema anterior.

> La instalación de un sistema operativo puede borrar datos. Si no estás seguro, pide ayuda presencial o prueba Xubuntu desde la USB sin instalarlo.

## 3. Crear la USB de instalación

Desde Windows puedes usar cualquiera de estas herramientas:

- **Rufus:** <https://rufus.ie/>
- **balenaEtcher:** <https://etcher.balena.io/>
- **Ventoy:** <https://www.ventoy.net/>

Flujo general:

1. Descarga la imagen ISO desde la web oficial de Xubuntu.
2. Conecta la USB.
3. Abre la herramienta elegida.
4. Selecciona la ISO y la USB correcta.
5. Inicia la escritura y espera a que termine.
6. Expulsa la memoria de forma segura.

## 4. Iniciar desde la USB

1. Reinicia el computador con la USB conectada.
2. Abre el menú de arranque. La tecla cambia según el fabricante: suele ser `F12`, `F9`, `Esc` o `F2`.
3. Selecciona la memoria USB en modo UEFI.
4. Elige **Try or Install Xubuntu**.

Primero puedes usar la opción de probar para revisar WiFi, sonido, Bluetooth, teclado, cámara y pantalla sin modificar el disco.

## 5. Instalar Xubuntu

El instalador te pedirá idioma, teclado, zona horaria, usuario y particionado.

- Si quieres borrar Windows por completo, usa la opción de instalar Xubuntu usando todo el disco.
- Para conservar Windows, elige la opción de instalar junto a Windows cuando esté disponible.
- Si el disco está cifrado con BitLocker, guarda la clave de recuperación antes de cambiar particiones.
- No elijas particionado manual si no entiendes sus implicaciones.

Al terminar, reinicia, retira la USB cuando el instalador lo indique y entra con tu usuario.

## 6. Actualizar el sistema

Abre una terminal con `Ctrl + Alt + T` y ejecuta:

```bash
sudo apt update
sudo apt full-upgrade -y
sudo reboot
```

## 7. Confirmar que el entorno es compatible

Después de reiniciar:

```bash
cat /etc/os-release
echo "$XDG_CURRENT_DESKTOP"
echo "$XDG_SESSION_TYPE"
```

El resultado esperado es Xubuntu/Ubuntu, escritorio XFCE y sesión `x11`.

## 8. Continuar con el agente

Sigue [Usar Winux Kit con Claude Code u OpenCode](02-usar-con-agentes.md).

## Problemas frecuentes

- **La USB no aparece:** revisa el menú UEFI/BIOS y desactiva temporalmente Fast Startup de Windows.
- **No hay WiFi durante la prueba:** termina la instalación usando cable o tethering USB y actualiza el sistema.
- **La pantalla queda negra:** prueba las opciones de gráficos seguros del menú de arranque.
- **No sabes si borrar Windows:** detente; prueba Xubuntu desde la USB o pide ayuda antes de particionar.
