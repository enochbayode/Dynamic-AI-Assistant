import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

TEAM_MEMBERS_ENDPOINT = os.getenv("TEAM_MEMBERS_ENDPOINT")

MANAGE_TEAM_URL = os.getenv("MANAGE_TEAM_URL")

async def fetch_team_members(organization_id: str, bearer_token: str) -> dict:
    """
    Fetch team members for assistant use — returns top 5 and full first page data.
    """
    if not TEAM_MEMBERS_ENDPOINT:
        logging.error("TEAM_MEMBERS_ENDPOINT not defined in environment variables.")
        return {
            "team_members": [],
            "page_team_members": [],
            "view_all_url": "#"
        }

    if not bearer_token:
        logging.error("Bearer token is missing or empty.")
        return {
            "team_members": [],
            "page_team_members": [],
            "view_all_url": "#"
        }

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }

    params = {
        "organization_id": organization_id,
        "limit": 10,
        "page": 1
    }

    try:
        logging.info(f"Calling {TEAM_MEMBERS_ENDPOINT} with org={organization_id}")
        logging.debug(f"Headers: {headers}")
        logging.debug(f"Params: {params}")

        async with httpx.AsyncClient(timeout=100.0) as client:

            url = TEAM_MEMBERS_ENDPOINT.format(organization_id=organization_id)
            
            response = await client.get(url, params=params, headers=headers)

        logging.debug(f"HTTP status: {response.status_code}")
        logging.debug(f"Raw response: {response.text}")

        if response.status_code != 200:
            logging.warning(f"Team member fetch failed for org {organization_id} — status {response.status_code}")
            return {
                "team_members": [],
                "page_team_members": [],
                "view_all_url": "#"
            }

        payload = response.json()
        if not payload.get("success") or "data" not in payload:
            logging.warning(f"Invalid payload structure for org {organization_id}: {payload}")
            return {
                "team_members": [],
                "page_team_members": [],
                "view_all_url": "#"
            }

        full_page_data = payload["data"]
        formatted = [
            {
                "id": item.get("team_member_id", ""),
                "name": f"{item.get('first_name', '')} {item.get('last_name', '')}".strip(),
                "title": item.get("title", ""),
                "email": item.get("email", ""),
                "phone": item.get("mobile_phone") or item.get("phone_number", ""),
                "total_sessions": item.get("total_sessions", "0"),
                "primary_language": item.get("primary_language", ""),
                "time_zone": item.get("time_zone", "")
            }
            for item in full_page_data if isinstance(item, dict)
        ]

        return {
            "team_members": formatted[:5],
            "page_team_members": formatted,
            "view_all_url": MANAGE_TEAM_URL
        }

    except httpx.RequestError as e:
        logging.error(f"HTTPX request error during team member fetch: {e!r}")
        return {
            "team_members": [],
            "page_team_members": [],
            "view_all_url": "#"
        }

    except Exception as e:
        logging.error(f"Unexpected error during team member fetch: {e!r}")
        return {
            "team_members": [],
            "page_team_members": [],
            "view_all_url": "#"
        }
