from sqlalchemy.orm import Session
from app.models.chat_interaction import AssistantInteraction
from sqlalchemy.exc import SQLAlchemyError
from app.core.db import get_db
from fastapi import Depends, Query


def get_chat_history(
    user_id: str,
    assistant_session_id: str,
    organization_id: str,
    db: Session
):
    interactions = (
        db.query(AssistantInteraction)
        .filter(
            AssistantInteraction.user_id == str(user_id).strip(),
            AssistantInteraction.assistant_session_id == str(assistant_session_id).strip(),
            AssistantInteraction.organization_id == str(organization_id).strip()
        )
        .order_by(AssistantInteraction.created_at)
        .all()
    )

    print(f"[HISTORY DEBUG from get_chat_history]: user_id={user_id} ({type(user_id)}), session_id={assistant_session_id} ({type(assistant_session_id)})")

    print(f"[HISTORY DEBUG from get_chat_history]: Found {len(interactions)} messages for user {user_id}")
    return [
        {
            "user_query": h.user_query,
            "assistant_response": h.assistant_response,
            "intent": h.intent,
            "response_source": h.response_source,
            "created_at": h.created_at.isoformat(),
        }
        for h in interactions
    ]


def clear_chat_history(
    db: Session, 
    user_id: str, 
    assistant_session_id: str,
    organization_id: str
):
    try:
        deleted_count = db.query(AssistantInteraction).filter(
            AssistantInteraction.user_id == user_id.strip(),
            AssistantInteraction.assistant_session_id == assistant_session_id.strip(),
            AssistantInteraction.organization_id == organization_id.strip()
        ).delete(synchronize_session=False)

        db.commit()
        print(f"[CLEAR DEBUG]: Deleted {deleted_count} interactions for user={user_id}, session={assistant_session_id}, org={organization_id}")

        return {
            "status": "success",
            "message": f"Deleted {deleted_count} interaction(s)."
        }
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[CLEAR ERROR]: Failed to clear history due to: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to clear history: {str(e)}"
        }
