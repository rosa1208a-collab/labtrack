import secrets
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy import delete, select

from app.models import AuthSession, LoginThrottle, User, utcnow
from app.schemas import LoginInput
from app.security import (
    COOKIE_NAME,
    DUMMY_HASH,
    digest,
    get_current_user,
    get_db,
    password_hasher,
    verify_origin,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginInput, request: Request, response: Response, db=Depends(get_db)):
    verify_origin(request)
    now = utcnow()
    email = str(payload.email).lower()
    # Límite persistente por cuenta: cinco fallos durante quince minutos.
    key = digest(email)
    throttle = db.get(LoginThrottle, key)
    if throttle and throttle.window_start <= now - timedelta(minutes=15):
        db.delete(throttle)
        db.flush()
        throttle = None
    if throttle and throttle.attempts >= 5:
        raise HTTPException(429, "Demasiados intentos. Espera quince minutos.")
    user = db.scalar(select(User).where(User.email == email))
    valid = password_hasher.verify(payload.password, user.password_hash if user else DUMMY_HASH)
    if not user or not valid:
        if throttle:
            throttle.attempts += 1
        else:
            db.add(LoginThrottle(key=key, attempts=1, window_start=now))
        db.commit()
        raise HTTPException(401, "Correo o contraseña incorrectos.")
    if throttle:
        db.delete(throttle)
    old_token = request.cookies.get(COOKIE_NAME)
    if old_token:
        db.execute(delete(AuthSession).where(AuthSession.token_hash == digest(old_token)))
    db.execute(delete(AuthSession).where(AuthSession.expires_at <= now))
    token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    ttl = request.app.state.settings.session_hours * 3600
    db.add(
        AuthSession(
            token_hash=digest(token),
            user_id=user.id,
            csrf_token=csrf,
            expires_at=now + timedelta(seconds=ttl),
        )
    )
    db.commit()
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=ttl,
        httponly=True,
        secure=request.app.state.settings.session_cookie_secure,
        samesite="lax",
        path="/",
    )
    return {"email": user.email, "csrf_token": csrf}


@router.get("/me")
def me(request: Request, user=Depends(get_current_user)):
    return {"email": user.email, "csrf_token": request.state.auth_session.csrf_token}


@router.post("/logout", status_code=204)
def logout(
    request: Request, response: Response, user=Depends(get_current_user), db=Depends(get_db)
):
    db.delete(request.state.auth_session)
    db.commit()
    response.delete_cookie(COOKIE_NAME, path="/")
