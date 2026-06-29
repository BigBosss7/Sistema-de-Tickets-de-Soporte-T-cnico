
# 🎫 Support Ticket System API

REST API desarrollada con **FastAPI** para gestionar tickets de soporte técnico.

Este proyecto implementa autenticación mediante **JWT**, autorización basada en roles (**RBAC**), arquitectura por capas (**Routers + Services**), auditoría mediante eventos y un dashboard con métricas para la gestión de incidencias.

El objetivo del proyecto es aplicar buenas prácticas de desarrollo Backend utilizando una arquitectura mantenible y escalable.

---

# ✨ Características

- ✅ Autenticación con JWT
- ✅ Registro e inicio de sesión
- ✅ Gestión de usuarios
- ✅ Creación de tickets
- ✅ Asignación de tickets
- ✅ Cambio de estado
- ✅ Comentarios
- ✅ Historial de eventos
- ✅ Dashboard
- ✅ Control de acceso basado en roles (RBAC)
- ✅ Arquitectura por capas
- ✅ Service Layer
- ✅ PostgreSQL + SQLAlchemy ORM

---

# 🛠 Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python 3.12 | Lenguaje principal |
| FastAPI | Framework REST |
| PostgreSQL | Base de datos |
| SQLAlchemy | ORM |
| Pydantic | Validación de datos |
| JWT | Autenticación |
| Passlib + Bcrypt | Hash de contraseñas |
| Uvicorn | Servidor ASGI |
| Git & GitHub | Control de versiones |

---

# 🏗 Arquitectura

El proyecto está organizado siguiendo una arquitectura por capas para mantener una clara separación de responsabilidades.

| Carpeta | Responsabilidad |
|----------|-----------------|
| `routers/` | Define los endpoints HTTP |
| `services/` | Contiene la lógica de negocio |
| `models/` | Modelos ORM de SQLAlchemy |
| `schemas/` | Validación con Pydantic |
| `core/` | Seguridad, permisos y funciones reutilizables |
| `exceptions/` | Excepciones personalizadas |
| `database.py` | Configuración de PostgreSQL |

# 🏛️ Decisiones de arquitectura

Durante el desarrollo del proyecto se tomaron las siguientes decisiones para mantener el código organizado y escalable.

---

# 🔄 Flujo de una petición

```mermaid
flowchart TD

A[Cliente]
--> B[Router]
B --> C[Service]
C --> D[SQLAlchemy]
D --> E[(PostgreSQL)]
E --> C
C --> F[JSON Response]
```

Los **routers** reciben las peticiones HTTP.

## Routers

Los endpoints fueron separados por dominio (usuarios, tickets, comentarios, eventos y dashboard) para evitar un archivo `main.py` demasiado grande y facilitar el mantenimiento.

## Service Layer

Toda la lógica de negocio fue movida a la carpeta `services`.

Los routers únicamente reciben la petición HTTP y delegan el procesamiento al servicio correspondiente.

Esto permite reutilizar la lógica desde otros clientes, como un futuro bot de Telegram o una aplicación web.

## RBAC

La autorización se implementó mediante Roles (USER, TECHNICIAN y SUPERVISOR).

Las reglas de negocio se validan dentro de los servicios y no en los routers para mantener la lógica centralizada.

## Eventos

Cada cambio importante genera un evento de auditoría.

Esto permite mantener un historial de modificaciones realizadas sobre cada ticket.

## Excepciones

El proyecto utiliza excepciones personalizadas y manejadores globales para desacoplar la lógica de negocio de las respuestas HTTP.

Los **services** contienen toda la lógica de negocio.

SQLAlchemy se encarga de comunicarse con PostgreSQL.

---

# 🔐 Flujo de autenticación

```mermaid
flowchart TD

A[Usuario]
--> B[/login]
B --> C[JWT Token]
C --> D["Authorization: Bearer TOKEN"]
D --> E[get_current_user()]
E --> F[Endpoint]
```

---

# 👥 Roles (RBAC)

| Rol | Permisos |
|------|----------|
| USER | Crear tickets, comentar y consultar sus tickets |
| TECHNICIAN | Cambiar estado de tickets asignados |
| SUPERVISOR | Asignar tickets, consultar todos los tickets y administrar el sistema |

---

# 📁 Estructura del proyecto

```text
backend/
│
├── app/
│   ├── core/
│   ├── exceptions/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── main.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# ⚙ Variables de entorno

Crear un archivo `.env` en la carpeta `backend`.

```env
DATABASE_URL=postgresql://usuario:password@localhost:5432/support_tickets
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

---

# 🚀 Instalación

Clonar el repositorio:

```bash
git clone https://github.com/TU-USUARIO/support-ticket-system.git
```

Entrar al proyecto:

```bash
cd support-ticket-system/backend
```

Crear entorno virtual:

```bash
python3.12 -m venv venv
```

Activar entorno virtual.

macOS / Linux

```bash
source venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

# ▶ Ejecutar

```bash
uvicorn app.main:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

# 📌 Funcionalidades implementadas

- Registro de usuarios
- Login con JWT
- CRUD de Tickets
- Comentarios
- Eventos
- Dashboard
- RBAC
- Arquitectura por capas
- Service Layer
- Excepciones personalizadas

---

# 🚧 Roadmap

## Backend

- ✅ FastAPI
- ✅ PostgreSQL
- ✅ SQLAlchemy
- ✅ JWT
- ✅ RBAC
- ✅ Dashboard
- ✅ Service Layer
- ✅ Exception Handlers

## Próximas mejoras

- ⬜ Logging
- ⬜ Docker
- ⬜ Docker Compose
- ⬜ Testing con Pytest
- ⬜ CI/CD con GitHub Actions
- ⬜ Telegram Bot
- ⬜ Frontend con Next.js
- ⬜ Redis
- ⬜ Deploy en Render

---
# 📈 Estado del proyecto

Actualmente el backend se encuentra funcional y cuenta con:

- Autenticación JWT.
- RBAC.
- Gestión de tickets.
- Dashboard.
- Arquitectura por capas.
- Service Layer.

Las siguientes etapas del proyecto incluyen:

- Docker.
- Testing.
- CI/CD.
- Frontend con Next.js.
- Deploy en producción.
---

# 👨‍💻 Autor

**Saúl Barrera**

Proyecto desarrollado como parte de mi proceso de aprendizaje para convertirme en Backend Developer, aplicando principios de arquitectura de software y buenas prácticas de desarrollo.
