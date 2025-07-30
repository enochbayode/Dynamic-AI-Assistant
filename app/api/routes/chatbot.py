from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.rag import generate_response  
from app.services.intent_classifier import classify_intent
from app.services.logger import log_assistant_interaction
from app.api.auth import verify_token_http

from app.services.intent_handler import (
    handle_service_search_intent,
    handle_team_member_search_intent,
    handle_create_team_member_intent,
    handle_create_patient_intent,
    handle_patient_search_intent,
    handle_appointment_search_intent,
    handle_dashboard_intent,
    handle_practice_location_intent,
    handle_payer_intent,
    handle_billing_intent,
    handle_contact_page_intent,
    handle_Eprescriptions_intent,
    handle_admin_setting_intent,
    handle_billing_setting_intent,
    handle_payment_setting_intent,
    handle_practice_setting_intent,
    handle_client_appointment_summary,
    handle_client_dashboard_intent,
    handle_client_document_summary,
    handle_client_practice_search_summary,
    handle_manage_files_intent
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
http_bearer = HTTPBearer()

@router.post("/chat/")
async def chatbot(
    organization_id: str,
    user_id: str,
    assistant_session_id: str,
    user_query: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    """
    Handles chatbot interaction.
    - `organization_id`: The organization ID to ensure multi-tenancy.
    - `user_id`: The user's unique identifier for tracking.
    - `assistant session_id`: Unique session identifier for this conversation.
    - `user_query`: The user's input.
    """

    payload = verify_token_http(credentials)
    if payload is None:
        return {"error": "Payload verification failed", "status_code": 401}

    # Classify user intent
    intent = await classify_intent(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    # Handle service search intent
    if intent == "service_search":
        response = await handle_service_search_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            bearer_token=credentials.credentials
        )
        
        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="service_search_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    # Handle general information queries (RAG) both for organization and global
    elif intent == "info_query":
        response = await generate_response(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        if not response:
            raise HTTPException(
                status_code=404,
                detail="No relevant information found for this organization."
            )
        
        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="RAG",
            assistant_response=response
        )

        return {"response": response} # RAG response
   
    elif intent == "dashboard_access":
        response = await handle_dashboard_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="dashboard_handler",
            assistant_response=response.get("response", "No response")
        )

        return response

    elif intent == "team_member_search":
        response = await handle_team_member_search_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            bearer_token=credentials.credentials
        )
        
        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="team_member_search_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "create_team_member":
        response = await handle_create_team_member_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            #bearer_token=credentials.credentials
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="create_team_member_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "create_patient":
        response = await handle_create_patient_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="create_patient_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "search_patient":
        response = await handle_patient_search_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="search_patient_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "appointment_search":
        response = await handle_appointment_search_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="appointment_search_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "practice_locations":
        response = await handle_practice_location_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="practice_location_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "payer_page":
        response = await handle_payer_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="payer_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "billing_page":
        response = await handle_billing_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="billing_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "contact_page":
        response = await handle_contact_page_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="contact_page_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "e_prescriptions":
        response = await handle_Eprescriptions_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="e_prescriptions_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "admin_settings":
        response = await handle_admin_setting_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="admin_settings_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "billing_settings":
        response = await handle_billing_setting_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="billing_settings_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "payment_settings":
        response = await handle_payment_setting_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="payment_settings_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "practice_settings":
        response = await handle_practice_setting_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="practice_settings_handler",
            assistant_response=response.get("response", "No response")
        )

        return response

    elif intent == "client_appointment":
        response = await handle_client_appointment_summary(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="client_appointment_handler",
            assistant_response=response.get("response", "No response")
        )

        return response

    elif intent == "client_dashboard":
        response = await handle_client_dashboard_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="client_dashboard_handler",
            assistant_response=response.get("response", "No response")
        )

        return response

    elif intent == "client_document":
        response = await handle_client_document_summary(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="client_document_handler",
            assistant_response=response.get("response", "No response")
        )

        return response
    
    elif intent == "manage_file":
        response = await handle_manage_files_intent(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="manage_file_handler",
            assistant_response=response.get("response", "No response")
        )
    
    elif intent == "client_practice_search":
        response = await handle_client_practice_search_summary(
            user_query=user_query,
            organization_id=organization_id,
            user_id=user_id,
            assistant_session_id=assistant_session_id
        )

        log_assistant_interaction(
            db=db,
            user_id=user_id,
            assistant_session_id=assistant_session_id,
            organization_id=organization_id,
            user_query=user_query,
            intent=intent,
            response_source="client_practice_handler",
            assistant_response=response.get("response", "No response")
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Intent not recognized or not supported."
        )
