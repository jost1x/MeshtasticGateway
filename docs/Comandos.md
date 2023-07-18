# Configuración LiLyGo T-Beam Meshtastic

# Comandos

## Cambio de región

```sh
meshtastic --set lora.region ANZ
```

## Setear contraseña estatica bluetooth

```sh
meshtastic --set bluetooth.mode FIXED_PIN
meshtastic --set bluetooth.fixed_pin 111111
```

## Configurar tiempo de telemetria


```sh
meshtastic --set position.gpsAttemptTime 450
meshtastic --set position.positionBroadcastSecs 120
meshtastic --set telemetry.device_update_interval 120
```

## Configurar envio de Informacion de Bateria

```sh
meshtastic --set positionFlags 33
```