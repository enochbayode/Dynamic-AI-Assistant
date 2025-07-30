from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.db import Base
import uuid

class AssistantInteraction(Base):
    __tablename__ = "assistant_interaction"


    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) # Unique identifier for the interaction

    user_id = Column(String, nullable=False)  
    assistant_session_id = Column(String, nullable=False)  
    organization_id = Column(String, nullable=False)  

    user_query = Column(Text, nullable=False)
    intent = Column(Text, nullable=False)
    response_source = Column(Text, nullable=False)
    assistant_response = Column(Text, nullable=False)
    feedback = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    last_update_at = Column(DateTime, default=func.now(), onupdate=func.now())
