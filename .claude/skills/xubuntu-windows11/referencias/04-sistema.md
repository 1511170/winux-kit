# D. Ajustes de sistema (cada uno opcional; preguntar cuáles)

`S` = carpeta de la skill. Todo lo de root con `pkexec bash -c '...'` (una ventana). Respaldar antes en `~/backups/$(date +%F)/`
y dejar un `revertir.sh` por cada grupo.

## D1. Forma de trabajar
- **pkexec** en vez de `sudo` (no hay TTY). Timeout ≥ 180 s. `pkexec` dentro de `( … &)` falla ("dead parents") → usar `run_in_background`.
- Guardar en `CLAUDE.md` de la carpeta de trabajo qué se cambió y cómo revertirlo; y en `~/backups/FECHA/LEEME.txt`.

## D2. WiFi: sin picos de latencia (videollamadas)
El ahorro de energía del WiFi causa picos (30–100 ms) que en Meet se sienten como "se va la señal".
```bash
pkexec bash -c "
cp '$S/archivos/sistema/zz-wifi-powersave-off.conf' /etc/NetworkManager/conf.d/zz-wifi-powersave-off.conf
cp '$S/archivos/sistema/99-network-tuning.conf' /etc/sysctl.d/99-network-tuning.conf
echo tcp_bbr > /etc/modules-load.d/bbr.conf && modprobe tcp_bbr && sysctl -p /etc/sysctl.d/99-network-tuning.conf
CON=\$(nmcli -t -f NAME,TYPE connection show --active | awk -F: '\$2==\"802-11-wireless\"{print \$1; exit}')
[ -n \"\$CON\" ] && nmcli connection modify \"\$CON\" 802-11-wireless.powersave 2
IF=\$(iw dev | awk '/Interface/{print \$2; exit}'); [ -n \"\$IF\" ] && iw dev \$IF set power_save off
nmcli general reload conf"
iw dev $(iw dev | awk '/Interface/{print $2; exit}') get power_save   # → off
```
- **El nombre debe empezar por `zz-`**: NM lee `conf.d` en orden alfabético y `default-wifi-powersave-on.conf` pisa a un `99-…`.
- No reconecta el WiFi (no corta llamadas). BBR + buffers: mejora leve; el tope real suele ser el router o el plan.
- Diagnóstico de cortes: ping cada 0,2 s al router y a 8.8.8.8 en paralelo + señal cada 2 s, registrando solo eventos con hora
  (pérdida al router = WiFi/router; solo a internet = operador; nada = Meet / el otro lado).

## D3. Bluetooth y audio (PipeWire + WirePlumber 0.5)
Problema real: un Echo Dot (u otro parlante que también sabe ser "fuente") se conectaba **al revés**, usando el PC como *su* parlante
(perfil `audio-gateway`, stream `bluez_input…`), y no aparecía como salida.
```bash
mkdir -p ~/.config/wireplumber/wireplumber.conf.d
cp $S/archivos/sistema/51-bluez-roles.conf $S/archivos/sistema/52-bluez-no-suspend.conf ~/.config/wireplumber/wireplumber.conf.d/
pkexec bash -c '
cp -n /etc/bluetooth/main.conf /etc/bluetooth/main.conf.bak-$(date +%F)
sed -i "s/^\[General\]$/[General]\nFastConnectable = true/" /etc/bluetooth/main.conf
sed -i "s/^\[Policy\]$/[Policy]\nReconnectAttempts = 7\nReconnectIntervals = 1,2,4,8,16,32,64\nAutoEnable = true/" /etc/bluetooth/main.conf
systemctl restart bluetooth'
rfkill unblock bluetooth; bluetoothctl power on       # tras reiniciar bluetooth puede quedar soft-blocked
systemctl --user restart wireplumber                  # desconecta los parlantes BT → reconectar:
# bluetoothctl connect <MAC>
```
- `51-bluez-roles.conf`: `bluez5.roles = [ a2dp_source bap_source hfp_ag hsp_ag ]` → el PC **nunca** hace de parlante/teléfono; parlantes y
  audífonos siempre entran como salida (`a2dp-sink`). Sigue pudiendo usar el micrófono de los audífonos (hfp_ag, autoswitch de WirePlumber).
- `52-bluez-no-suspend.conf`: `session.suspend-timeout-seconds = 0` en `bluez_output.*` → los sonidos cortos (notificaciones) no se pierden al
  despertar el enlace. Para probar sonido usar un tono de varios segundos con 1 s de silencio inicial, no `complete.oga` (0,5 s).
- Cambiar salida/entrada: icono de volumen de la barra (plugin pulseaudio) o `pavucontrol`; al conectar un dispositivo BT pasa a ser la salida por defecto.
- Ver estado: `wpctl status`, `bluetoothctl info <MAC>`, `pw-dump` (perfiles en `EnumProfile`).

## D4. Diagnóstico (memoria, cuelgues)
```bash
pkexec bash -c 'mkdir -p /var/log/journal && systemd-tmpfiles --create --prefix /var/log/journal && systemctl restart systemd-journald &&
DEBIAN_FRONTEND=noninteractive apt-get install -y rasdaemon && systemctl enable --now rasdaemon'
```
- Journal persistente: `journalctl --list-boots`, `journalctl -b -1 -k` (arranque anterior). rasdaemon: `ras-mc-ctl --summary`
  (con RAM sin ECC no ve bits malos; sí MCE). RAM defectuosa = muchos SIGSEGV de programas sin relación en `/var/crash` → confirmar con
  MemTest86+ (GRUB oculto: mantener Shift al arrancar).

## D5. Revertir
- Red: borrar `zz-wifi-powersave-off.conf`, `99-network-tuning.conf`, `bbr.conf`; `nmcli connection modify <red> 802-11-wireless.powersave 0`; `nmcli general reload conf`.
- Bluetooth/audio: borrar `51-` y `52-bluez-*.conf`, restaurar `main.conf.bak-*`, reiniciar wireplumber y bluetooth, `rfkill unblock bluetooth`.
