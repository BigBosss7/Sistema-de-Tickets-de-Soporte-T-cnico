from fastapi import FastAPI

from app.database import (
    engine,
    Base
)
from app.models.user import User
from app.models.ticket import Ticket
from app.models.ticket_comment import TicketComment
from app.models.ticket_event import TicketEvent 

from app.routers.auth import router as auth_router
from app.routers.comments import router as comments_router
from app.routers.tickets import router as ticket_router
from app.routers.events import router as events_router
from app.routers.dashboard import router as dashboard_router
from app.routers.users import router as users_router



app = FastAPI(
    title="Support Ticket System",
    description="API para gestionar tickets de soporte técnico.",
    version="0.1.0"
)

app.include_router(auth_router)

app.include_router(ticket_router)

app.include_router(comments_router)

app.include_router(events_router)

app.include_router(dashboard_router)

app.include_router(users_router)

Base.metadata.create_all(bind=engine)

@app.get(
    "/",
    summary="Health check inicial",
    description="Verifica que la API está funcionando correctamente."
)
def home():
    return {
        "status": "ok",
        "message": "Support Ticket System API is running"
    }

@app.get("/health",
    summary="Health check",
    description="Verifica que la API está funcionando correctamnete"
)
def health():
    return {
        "api": "running",
        "version": "0.1.0"
    }

@app.get("/db-check")
def db_check():
    try:
        with engine.connect():
            return {"database": "connected"}
    except Exception as error:
        return {
            "database": "error",
            "detail": str(error)
        }
















