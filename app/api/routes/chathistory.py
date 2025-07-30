from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.db import get_db
from app.services.session_history import clear_chat_history, get_chat_history
from app.api.auth import verify_token_http

router = APIRouter()
http_bearer = HTTPBearer()

@router.delete("/chat/clear/")
def clear_history(
    user_id: str,
    assistant_session_id: str,
    organization_id: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    payload = verify_token_http(credentials)
    if payload is None:
        return {"error": "Payload verification failed", "status_code": 401}

    result = clear_chat_history(
        db=db, 
        user_id=user_id, 
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )
    return result


@router.get("/chat/history/")
def get_history(
    user_id: str,
    assistant_session_id: str,
    organization_id: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    payload = verify_token_http(credentials)
    if payload is None:
        return {"error": "Payload verification failed", "status_code": 401}

    history = get_chat_history(
        db=db, 
        user_id=user_id, 
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "status": "success", 
        "history": history
    }



