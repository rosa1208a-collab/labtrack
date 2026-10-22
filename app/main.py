from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError

from app.config import Settings
from app.db import make_engine, make_session_factory
from app.models import Experiment, Project
from app.routes import auth, experiments, projects
from app.security import get_current_user, get_db

WEB = Path(__file__).resolve().parent.parent / "frontend"


def create_app(settings: Settings | None = None):
    settings = settings or Settings()
    engine = make_engine(settings.database_url)

    @asynccontextmanager
    async def lifespan(app):
        yield
        engine.dispose()

    app = FastAPI(title="LabTrack API", version="1.0.0", lifespan=lifespan)
    app.state.settings = settings
    app.state.engine = engine
    app.state.session_factory = make_session_factory(engine)

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        if request.url.path.startswith("/api"):
            response.headers["Cache-Control"] = "no-store"
        if request.url.path == "/":
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; "
                "base-uri 'self'; form-action 'self'"
            )
        return response

    @app.get("/health", tags=["system"])
    def health(db=Depends(get_db)):
        try:
            db.execute(text("SELECT 1"))
            return {"status": "ok"}
        except SQLAlchemyError:
            return JSONResponse({"status": "unavailable"}, status_code=503)

    @app.get("/api/summary", tags=["summary"])
    def summary(user=Depends(get_current_user), db=Depends(get_db)):
        projects_count = db.scalar(
            select(func.count()).select_from(Project).where(Project.user_id == user.id)
        )
        experiments_count = db.scalar(
            select(func.count())
            .select_from(Experiment)
            .join(Project)
            .where(Project.user_id == user.id)
        )
        return {"projects": projects_count, "experiments": experiments_count}

    app.include_router(auth.router, prefix="/api")
    app.include_router(projects.router, prefix="/api")
    app.include_router(experiments.router, prefix="/api")
    app.mount("/static", StaticFiles(directory=WEB), name="static")

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(WEB / "index.html")

    return app
