from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from uuid import UUID
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.db import get_db
from app.models.chat_interaction import AssistantInteraction
from app.api.auth import verify_token_http  

router = APIRouter()
http_bearer = HTTPBearer()


class FeedbackPayload(BaseModel):
    interaction_id: str 
    feedback: str = Field(..., pattern="^(thumbs_up|thumbs_down)$")


@router.post("/chat/feedback/")
def submit_feedback(
    payload: FeedbackPayload,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    """
    Submit feedback for a specific assistant interaction.
    Auth token required to identify user.
    """
    # Extract user ID from token
    token_payload = verify_token_http(credentials)
    if not token_payload or "user_id" not in token_payload:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = token_payload["user_id"]

    # Locate the interaction
    interaction = db.query(AssistantInteraction).filter(
        AssistantInteraction.id == payload.interaction_id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found.")

    # feedback can only be submitted by original user
    if interaction.user_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied: cannot modify another user's interaction.")

    # Save feedback
    interaction.feedback = payload.feedback
    db.commit()

    return {
        "status": "success",
        "message": "Feedback submitted successfully.",
        "interaction_id": str(interaction.id),
        "feedback": interaction.feedback,
        "submitted_by": user_id,
    }
