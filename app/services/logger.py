from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.chat_interaction import AssistantInteraction


def log_assistant_interaction(
    db: Session,
    user_id: str,
    assistant_session_id: str,
    organization_id: str,
    user_query: str,
    intent: str,
    response_source: str,
    assistant_response: str,
):
    try:
        interaction = AssistantInteraction(
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source=response_source,
            assistant_response=assistant_response,
        )
        db.add(interaction)
        db.flush()  # Force insert before commit

        print(f"[DB LOGGING from logger]: Generated interaction_id: {interaction.id}")

        db.commit()
        
        print(f"[DB LOGGING from logger]: Interaction saved — user_id={interaction.user_id}, session_id={interaction.assistant_session_id}, query='{interaction.user_query}', intent='{interaction.intent}', response='{interaction.assistant_response}'")


    except SQLAlchemyError as e:
        db.rollback()
        print(f"[DB LOGGING ERROR]: {str(e)}")
