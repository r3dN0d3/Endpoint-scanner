# ☠ EndpointScanner GUI 

---

## Requisitos

**Python 3.9 o superior.**

```bash
pip install requests urllib3 colorama
```

| Librería | Uso | Obligatoria |
|---|---|---|
| `requests` | Peticiones HTTP | ✅ Sí |
| `urllib3` | Pool de conexiones y retry | ✅ Sí |
| `colorama` | Colores en terminal (CLI) | ✅ Sí |
| `tkinter` | Interfaz gráfica | ✅ Sí (incluida en Python) |

> `tkinter` viene incluido con Python en Windows y macOS. En Linux puede que necesites instalarlo:
> ```bash
> # Debian/Ubuntu
> sudo apt install python3-tk
>
> # Fedora
> sudo dnf install python3-tkinter
>
> # Arch
> sudo pacman -S tk
> ```

El archivo `symfony_scanner_gui.py` es **completamente standalone** — no necesita `main.py` ni ningún otro archivo externo.

---

## Uso GUI (`symfony_scanner_gui.py`)

```bash
python symfony_scanner_gui.py
```

Abre la interfaz gráfica. No necesita ningún otro archivo.

---

## Opciones

### Argumentos posicionales

| Argumento | Descripción |
|---|---|
| `url` | URL base del objetivo (ej: `https://ejemplo.com`) |

### Opciones numéricas

| Flag | Descripción | Default |
|---|---|---|
| `--threads` | Hilos concurrentes | 20 |
| `--timeout` | Timeout por petición (s) | 7 |
| `--retries` | Reintentos por fallo transitorio | 2 |
| `--backoff` | Factor de backoff exponencial | 0.4 |
| `--delay` | Delay fijo por petición (s) | 0.0 |
| `--jitter` | Jitter ±(s) sobre el delay | 0.0 |
| `--rps` | Requests por segundo máximo global | 0.0 |
| `--fuzz-limit` | Combinaciones máximas por placeholder | 8 |
| `--fuzz-threads` | Hilos para la fase de Smart Fuzz | 8 |

### Opciones de filtrado y salida

| Flag | Descripción |
|---|---|
| `--codes` | Códigos HTTP a reportar, separados por coma (ej: `200,301,403`) |
| `--format` | Formato de salida: `json` o `csv` |
| `--out` | Ruta del archivo de salida (requerido con `--format`) |

### Opciones de red

| Flag | Descripción |
|---|---|
| `-w, --wordlist` | Archivo con rutas adicionales (una por línea) |
| `-p, --paths` | Rutas extra separadas por espacios |
| `-H, --header` | Header extra, repetible (ej: `-H "Cookie: a=b"`) |
| `--proxy` | Proxy HTTP/HTTPS (ej: `http://127.0.0.1:8080`) |

### Flags booleanos

| Flag | Descripción |
|---|---|
| `--follow` | Seguir redirecciones |
| `--head-first` | Enviar HEAD antes de GET |
| `--insecure` | Ignorar errores de certificado TLS |
| `--verbose` | Mostrar todas las respuestas, no solo hits |
| `--save-all` | Guardar todos los resultados con `--format` |
| `--smart-fuzz` | Activar Smart Fuzz en endpoints con placeholders |
| `--prefer-http` | Probar HTTP antes que HTTPS |
| `--dual` | Escanear con HTTP y HTTPS simultáneamente |

---

## Rutas incluidas

| Lista | Cantidad | Descripción |
|---|---|---|
| `COMMON_PATHS` | ~160 | Rutas típicas de Symfony: profiler, API, login, build, bundles, archivos sensibles... |
| `BACKUP_PATHS` | ~35 | Backups: `.env.bak`, `dump.sql`, `database.sql.gz`, `backup.zip`... |
| `gen_backup_candidates()` | ~500 | Generadas combinando basenames × directorios × sufijos |

---

## Smart Fuzz

Cuando un endpoint con placeholders devuelve `200`, el escáner genera variantes automáticamente usando el catálogo de fuzz y las prueba en una segunda fase.

**Placeholders soportados:**

| Placeholder | Valores de prueba |
|---|---|
| `{id}` | 1, 2, 3, 5, 10, 25, 50, 100, 999, 0, -1 |
| `{token}` | abcdef1234, deadbeef, 0123456789abcdef, ... |
| `{slug}` | test, admin, profile, config, sitemap, api, graphql, docs |
| `{provider}` | google, github, facebook, twitter, microsoft, azure, apple |
| `{code}` | 200, 302, 400, 401, 403, 404, 500 |
| `{_format}` | json, html, xml, txt |
| `{fontName}` | OpenSans-Regular, Roboto-Regular, ... |

---

## Comportamiento de red

**Fallback HTTPS → HTTP:** si una petición HTTPS falla por error de red o TLS, el escáner reintenta automáticamente con HTTP.

**Probe inicial:** antes del escaneo, prueba el host en ambos esquemas y clasifica el estado como `HTTPS-only`, `HTTP-only`, `Dual` o `HTTPS-broken-API`. El resto del escaneo usa el esquema más adecuado.

**Fingerprinting Symfony:** detecta headers `X-Debug-Token`, `X-Debug-Token-Link`, estructura FOSJsRouting y archivos Encore (manifest/entrypoints).

---

## Uso con Burp Suite

```bash
python main.py https://ejemplo.com \
  --proxy http://127.0.0.1:8080 \
  --insecure \
  --threads 5
```

En la GUI: campo `--proxy` → `http://127.0.0.1:8080` y marcar `Ignorar TLS`.

---

## Ejemplos de salida

```
[+] [base] https://ejemplo.com/_profiler/ (Status 200) (312 ms) [text/html]
[+] [base] https://ejemplo.com/.env (Status 200) (89 ms) [text/plain]
[+] [base] https://ejemplo.com/api/doc.json (Status 200) (201 ms) [application/json]
[-] [base] https://ejemplo.com/admin (Status 404) (45 ms)
[+] [fuzz] https://ejemplo.com/download/1 (Status 200) (134 ms) [parent=/download/{id}]

Resumen: interesantes=3 | errores=0 | total=312
Host status: ejemplo.com = HTTPS-only
```

---

## Notas legales

Esta herramienta está diseñada para:
- Pruebas en tus propios sistemas
- Auditorías con permiso escrito del cliente
- Entornos de laboratorio y CTFs
