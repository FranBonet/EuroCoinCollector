# 🪙 EuroCoinCollector v3 — Walkthrough

## Resumen

Proyecto completo creado en `C:\Users\Fran\Desktop\Grado Superior DAM\antigravity\EuroCoinCollector\` con **27 archivos**, **33 tests unitarios** pasando al 100%.

---

## Estructura Final

```
EuroCoinCollector/
├── .env                          # Variables de entorno
├── .gitignore                    # Exclusiones Git
├── Dockerfile                    # Imagen Python 3.11
├── docker-compose.yml            # MySQL 8 + FastAPI
├── requirements.txt              # Dependencias Python
├── database/
│   └── init.sql                  # Schema + 50 monedas reales
├── backend/
│   ├── __init__.py
│   ├── config.py                 # get_database_url()
│   ├── database.py               # Engine, SessionLocal, get_db()
│   ├── models.py                 # Pais, Moneda, Coleccion, ListaDeseos
│   ├── schemas.py                # Pydantic request/response
│   ├── crud.py                   # Operaciones DB (una instrucción/función)
│   ├── main.py                   # Factory crear_app() + StaticFiles
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── paises.py             # GET /paises
│   │   ├── monedas.py            # GET /monedas, GET /monedas/{id}
│   │   ├── coleccion.py          # GET /coleccion, PUT /coleccion/{id}
│   │   ├── lista_deseos.py       # GET/POST/DELETE /lista_deseos
│   │   ├── estadisticas.py       # GET /estadisticas
│   │   └── exportar.py           # GET /exportar/csv
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py           # SQLite in-memory + fixtures
│       ├── test_paises.py        # 3 tests
│       ├── test_monedas.py       # 9 tests
│       ├── test_coleccion.py     # 6 tests
│       ├── test_lista_deseos.py  # 7 tests
│       ├── test_estadisticas.py  # 4 tests
│       └── test_exportar.py      # 4 tests
└── frontend/
    ├── index.html                # Dashboard + Catálogo + Colección + Deseos
    ├── style.css                 # Dark theme con glassmorphism
    └── app.js                    # Fetch API (funciones una instrucción)
```

---

## Decisiones de Diseño

| Decisión | Implementación |
|---|---|
| **Una instrucción por función** | Todas las funciones en `crud.py`, `app.js` y routes tienen un solo `return` o una sola operación |
| **Sin Nginx** | Frontend servido con `FastAPI.StaticFiles` → solo 2 servicios Docker |
| **Sin pandas** | CSV generado con `csv.writer` estándar → imagen Docker más ligera |
| **SQLite para tests** | `conftest.py` usa SQLite in-memory → tests rápidos sin MySQL |
| **Upsert en colección** | `PUT /coleccion/{id}` crea o actualiza automáticamente |
| **UNIQUE en lista_deseos** | No se puede duplicar una moneda en la wishlist (409 Conflict) |
| **Idioma español** | Endpoints, prioridades (`alta/media/baja`) y tipos (`comun/conmemorativa`) en español |

---

## Tests

```
============================= 33 passed in 0.35s ==============================
```

| Módulo | Tests | Estado |
|---|---|---|
| test_paises.py | 3 | ✅ |
| test_monedas.py | 9 | ✅ |
| test_coleccion.py | 6 | ✅ |
| test_lista_deseos.py | 7 | ✅ |
| test_estadisticas.py | 4 | ✅ |
| test_exportar.py | 4 | ✅ |

---

## Cómo arrancar

```bash
# Con Docker (producción):
cd EuroCoinCollector
docker-compose up --build

# API: http://localhost:8000/docs
# Frontend: http://localhost:8000

# Solo tests (sin Docker):
cd EuroCoinCollector
pip install -r requirements.txt
python -m pytest backend/tests/ -v
```

---

## API REST — Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/paises` | Lista de países emisores |
| `GET` | `/monedas?tipo=&pais=&anyo=` | Catálogo con filtros |
| `GET` | `/monedas/{id}` | Detalle de una moneda |
| `GET` | `/coleccion` | Monedas poseídas (cantidad > 0) |
| `PUT` | `/coleccion/{id_moneda}` | Añadir/actualizar en colección |
| `GET` | `/lista_deseos` | Lista de deseos completa |
| `POST` | `/lista_deseos/{id_moneda}` | Añadir a deseos |
| `DELETE` | `/lista_deseos/{id_moneda}` | Quitar de deseos |
| `GET` | `/estadisticas` | Dashboard stats |
| `GET` | `/exportar/csv` | Descargar CSV |

## Base de Datos

- **19 países** de la eurozona y otras emisiones
- **50 monedas reales** de 2€ actualizadas (Mapeadas y descargadas automáticamente de TodoNumismatica mediante Playwright)
- Precios de mercado inicializados y unificados
- Imágenes reales alojadas localmente en el contenedor bajo `frontend/img/coins/`
