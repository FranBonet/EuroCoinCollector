<div align="center">
  <h1>🇪🇺 EuroCoinCollector</h1>
  <p><i>Plataforma Integral para la Gestión de Colecciones de Monedas Conmemorativas de 2€</i></p>
</div>

---

## 📌 Sobre el Proyecto

**EuroCoinCollector** es una aplicación web Full-Stack diseñada para numismáticos y coleccionistas. Permite gestionar una colección personal, buscar información de monedas en un catálogo oficial, administrar una lista de deseos y realizar intercambios con otros coleccionistas.

Este proyecto ha sido desarrollado utilizando un enfoque de microservicios con contenedores, garantizando un despliegue rápido e independiente del entorno local.

### 🛠️ Tecnologías Utilizadas

- **Frontend:** HTML5, CSS3 (Custom Properties, Glassmorphism), Vanilla JavaScript ES6+
- **Backend:** Python 3.11, FastAPI, Pydantic, SQLAlchemy
- **Base de Datos:** MySQL 8.0
- **Testing:** Pytest (con SQLite In-Memory)
- **Infraestructura:** Docker, Docker Compose

---

## 🚀 Cómo probar el proyecto (Guía para Evaluadores y Responsables)

Gracias a la implementación de **Docker**, no es necesario instalar Python, MySQL ni configurar bases de datos locales para probar esta aplicación. Todo el entorno está encapsulado.

### Requisitos previos
- Tener instalado [Docker](https://www.docker.com/products/docker-desktop/) en el sistema.
- (Opcional pero recomendado) Git para clonar el repositorio.

### Pasos para ejecutar:

1. **Clonar el repositorio** (o descargar el .zip y descomprimirlo):
   ```bash
   git clone <URL_DEL_REPOSITORIO_GITHUB>
   cd EuroCoinCollector
   ```

2. **Levantar los contenedores**:
   En la raíz del proyecto, ejecuta el siguiente comando. Docker descargará las imágenes necesarias, creará la base de datos, insertará los datos iniciales (50 monedas) e iniciará de manera independiente el backend y el frontend.
   ```bash
   docker-compose up -d --build
   ```

3. **Acceder a la aplicación**:
   Una vez que los contenedores estén corriendo, abre tu navegador y visita:
   👉 **[http://localhost](http://localhost)**
   
   *(Nota: La API del backend se expone en el puerto 8000: `http://localhost:8000`)*

4. **Detener la aplicación**:
   Para apagar el servidor de forma segura, presiona `Ctrl + C` en la terminal, o ejecuta en otra terminal:
   ```bash
   docker-compose down
   ```

---

## 📚 Documentación Técnica Adjunta

Dentro del repositorio encontrarás los siguientes documentos PDF detallando toda la fase de planificación, arquitectura y pruebas del proyecto:

1. `1_Documentacion_Proyecto.pdf`: Arquitectura, diagrama Entidad-Relación, flujos de la API REST y uso de contenedores.
2. `2_Guia_Git_GitHub.pdf`: Flujo de trabajo y ramas empleadas.
3. `3_Reporte_Tests.pdf`: Estrategia de Pruebas Unitarias (TDD) y cobertura de código.

---

<div align="center">
  <i>Desarrollado como Proyecto Final para el Grado Superior de Desarrollo de Aplicaciones Multiplataforma (DAM).</i>
</div>
