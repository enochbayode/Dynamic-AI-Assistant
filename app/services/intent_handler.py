import os
from app.services.service_search import fetch_services
from app.services.team_member_search import fetch_team_members

from app.services.openai_task import (
    generate_service_summary,
    generate_team_member_summary,
    generate_create_team_member_summary,
    generate_create_patient_summary,
    generate_search_appointment_summary,
    generate_patient_search_summary,
    generate_practice_location_summary,
    generate_contact_page_summary,
    generate_billing_summary,
    generate_payer_summary,
    generate_Eprescription_summary,
    generate_admin_settings_summary,
    generate_billing_setting_summary,
    generate_payment_settings_summary,
    generate_practice_settings_summary,
    dashboard_generate_response_summary,
    generate_client_dashboard_summary,
    generate_client_appointment_summary,
    generate_client_pratice_search_summary,
    generate_manage_files_summary,
    generate_client_document_summary
    
)

from dotenv import load_dotenv

load_dotenv()

import logging


ADD_CLIENTS_URL = os.getenv("ADD_CLIENTS_URL")

MANAGE_CLIENT_URL = os.getenv("MANAGE_CLIENT_URL")

ADD_TEAM_MEMBER_URL = os.getenv("ADD_TEAM_MEMBER_URL")

MANAGE_APPOINTMENT_URL = os.getenv("MANAGE_APPOINTMENT_URL")

ADMIN_DASHBOARD_URL = os.getenv("ADMIN_DASHBOARD_URL")

PRACTICE_LOCATION_URL = os.getenv("PRACTICE_LOCATION_URL")

CONTACT_PAGE_URL = os.getenv("CONTACT_PAGE_URL")

PAYER_PAGE_URL = os.getenv("PAYER_PAGE_URL")

BILLING_PAGE_URL = os.getenv("BILLING_PAGE_URL")

E_PRESCRIPTIONS_URL = os.getenv("E_PRESCRIPTIONS_URL")

ADMIN_SETTING_URL = os.getenv("ADMIN_SETTING_URL")

BILLING_SETTING_URL = os.getenv("BILLING_SETTING_URL")

PAYMENT_SETTING_URL = os.getenv("PAYMENT_SETTING_URL")

PRACTICE_SETTING_URL = os.getenv("PRACTICE_SETTING_URL")

CLIENT_DASHBOARD_URL = os.getenv("CLIENT_DASHBOARD_URL")

CLIENT_APPOINTMENT_URL = os.getenv("CLIENT_APPOINTMENT_URL")

CLIENT_PRACTICE_SEARCH_URL = os.getenv("CLIENT_PRACTICE_SEARCH_URL")

CLIENT_DOCUMENT_URL = os.getenv("CLIENT_DOCUMENT_URL")

MANAGE_ADMIN_FILES_URL = os.getenv("MANAGE_ADMIN_FILES_URL")

async def handle_service_search_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str,
    bearer_token: str
) -> dict:
    """
    Handles the `service_search` intent by fetching services, generating summaries,
    and preparing both assistant text and UI widget payload.
    """

    if not bearer_token:
        logging.warning(
            f"No Bearer token provided | Org: {organization_id} | User: {user_id} | Session: {assistant_session_id}"
        )
        return {
            "response": "Authentication token missing. Please login again to continue.",
            "ui_event": None
        }

    try:
        result = await fetch_services(user_query, organization_id, bearer_token=bearer_token)
        logging.info(f"result: {result}")

    except Exception as e:
        logging.error(
            f"Service fetch failed | Org: {organization_id} | User: {user_id} | Token: {bearer_token[:10]}... | Error: {str(e)}"
        )
        return {
            "response": "There was an issue fetching services. Please try again later.",
            "ui_event": None
        }

    if not result or not result.get("services"):
        logging.info(f"No services found | Query: '{user_query}' | Org: {organization_id}")
        return {
            "response": (
                "I couldn’t find any services matching your request. "
                f"You can view all available services [here]({result.get('view_all_url', '#')})."
            ),
            "ui_event": None
        }


    summary = await generate_service_summary(
        services=result["services"],
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": result["page_services"],
            "view all_url": result["view_all_url"],
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_team_member_search_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str,
    bearer_token: str
) -> dict:
    """
    Handles the `team_member_search` intent by fetching team members, generating summaries,
    and preparing both assistant text and UI widget payload.
    """

    if not bearer_token:
        logging.warning(
            f"No Bearer token provided | Org: {organization_id} | User: {user_id} | Session: {assistant_session_id}"
        )
        return {
            "response": "Authentication token missing. Please login again to continue.",
            "ui_event": None
        }

    try:
        result = await fetch_team_members(organization_id, bearer_token)
        logging.info(f"result: {result}")

    except Exception as e:
        logging.error(
            f"Team member fetch failed | Org: {organization_id} | User: {user_id} | Token: {bearer_token[:10]}... | Error: {str(e)}"
        )
        return {
            "response": "There was an issue fetching team members. Please try again later.",
            "ui_event": None
        }

    if not result or not result.get("team_members"):
        logging.info(f"No team member found | Query: '{user_query}' | Org: {organization_id}")
        return {
            "response": (
                "I couldn’t find any team member matching your request. "
                f"You can view all available members [here]({result.get('view_all_url', '#')})."
            ),
            "ui_event": None
        }


    summary = await generate_team_member_summary(
        team_members=result["team_members"],
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": result["page_team_members"],
            "view_all_url": result["view_all_url"],
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_dashboard_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `dashboard` intent by preparing a response and UI widget payload.
    """
    summary = await dashboard_generate_response_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": ADMIN_DASHBOARD_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_create_team_member_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `create_team_member` intent by preparing a response and UI widget payload.
    """
    summary = await generate_create_team_member_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": ADD_TEAM_MEMBER_URL,
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_create_patient_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `create_patient` intent by preparing a response and UI widget payload.
    """
    summary = await generate_create_patient_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": ADD_CLIENTS_URL,
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_patient_search_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `patient_search` intent by preparing a response and UI widget payload.
    """
    summary = await generate_patient_search_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": MANAGE_CLIENT_URL,
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_appointment_search_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `appointment_search` intent by preparing a response and UI widget payload.
    """
    summary = await generate_search_appointment_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": MANAGE_APPOINTMENT_URL,
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_practice_location_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `practice_location` intent by preparing a response and UI widget payload.
    """
    summary = await generate_practice_location_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": PRACTICE_LOCATION_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_contact_page_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict: 
    """
    Handles the `contact page` intent by preparing a response and UI widget payload.
    """
    summary = await generate_contact_page_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": CONTACT_PAGE_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_payer_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict: 
    """
    Handles the `billing page` intent by preparing a response and UI widget payload.
    """
    summary = await generate_payer_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": PAYER_PAGE_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_billing_intent( 
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict: 
    """
    Handles the `billing page` intent by preparing a response and UI widget payload.
    """
    summary = await generate_billing_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": BILLING_PAGE_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_Eprescriptions_intent(
     user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict: 
    """
    Handles the `Eprescriptions` intent by preparing a response and UI widget payload.
    """
    summary = await generate_Eprescription_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": E_PRESCRIPTIONS_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_admin_setting_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `admin_setting` intent by preparing a response and UI widget payload.
    """
    summary = await generate_admin_settings_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": ADMIN_SETTING_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_billing_setting_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `billing_setting` intent by preparing a response and UI widget payload.
    """
    summary = await generate_billing_setting_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": BILLING_SETTING_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_payment_setting_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `payment_setting` intent by preparing a response and UI widget payload.
    """
    summary = await generate_payment_settings_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": PAYMENT_SETTING_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_practice_setting_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `practice_setting` intent by preparing a response and UI widget payload.
    """
    summary = await generate_practice_settings_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": PRACTICE_SETTING_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_manage_files_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `manage_files` intent by preparing a response and UI widget payload.
    """
    summary = await generate_manage_files_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": MANAGE_ADMIN_FILES_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

# >>>>>>>>>>>>>>> Clients function handlers >>>>>>>>>>>>>>>>>>
async def handle_client_dashboard_intent(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `client_dashboard` intent by preparing a response and UI widget payload.
    """
    summary = await generate_client_dashboard_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": CLIENT_DASHBOARD_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_client_appointment_summary(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `client_appointment` intent by preparing a response and UI widget payload.
    """
    summary = await generate_client_appointment_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": CLIENT_APPOINTMENT_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_client_practice_search_summary(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict:
    """
    Handles the `client_practice_search` intent by preparing a response and UI widget payload.
    """
    summary = await generate_client_pratice_search_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": CLIENT_PRACTICE_SEARCH_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }

async def handle_client_document_summary(
    user_query: str,
    organization_id: str,
    user_id: str,
    assistant_session_id: str
) -> dict: 
    """
    Handles the `client_document` intent by preparing a response and UI widget payload.
    """
    summary = await generate_client_document_summary(
        user_query=user_query,
        user_id=user_id,
        assistant_session_id=assistant_session_id,
        organization_id=organization_id
    )

    return {
        "response": summary,
        "ui_event": {
            "type": "widget_trigger",
            "action": "navigate",
            "payload": None,
            "view_all_url": CLIENT_DOCUMENT_URL,  
            "user_id": user_id,
            "assistant_session_id": assistant_session_id,
            "organization_id": organization_id
        }
    }