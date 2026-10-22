import hashlib
import secrets

from fastapi import Depends, HTTPException, Request
from pwdlib import PasswordHash

from app.models import AuthSession, User, utcnow

password_hasher = PasswordHash.recommended()
# Igualamos el coste de verificar un usuario inexistente.
DUMMY_HASH = password_hasher.hash(secrets.token_urlsafe(32))
COOKIE_NAME = "labtrack_session"
SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def get_db(request: Request):
    with request.app.state.session_factory() as db:
        yield db


def verify_origin(request: Request):
    if request.headers.get("origin") not in request.app.state.settings.allowed_origins:
        raise HTTPException(403, "Origen no permitido.")


def get_current_user(request: Request, db=Depends(get_db)) -> User:
    token = request.cookies.get(COOKIE_NAME)
    session = db.get(AuthSession, digest(token)) if token else None
    if session is None or session.expires_at <= utcnow():
        raise HTTPException(401, "Inicia sesión para continuar.")
    if request.method not in SAFE_METHODS:
        verify_origin(request)
        supplied = request.headers.get("x-csrf-token", "")
        if not secrets.compare_digest(supplied, session.csrf_token):
            raise HTTPException(403, "Token CSRF inválido. Vuelve a iniciar sesión.")
    user = db.get(User, session.user_id)
    if user is None:
        raise HTTPException(401, "Sesión inválida.")
    request.state.auth_session = session
    return user
