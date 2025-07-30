import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

SERVICE_SEARCH_ENDPOINT = os.getenv("SERVICE_SEARCH_ENDPOINT")

SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL")

async def fetch_services(user_query: str, organization_id: str, bearer_token: str) -> dict:
    """
    Fetch services for assistant use — returns top 5 and full first page data.
    """
    if not SERVICE_SEARCH_ENDPOINT:
        logging.error("SERVICE_SEARCH_ENDPOINT not defined in environment variables.")
        return {
            "services": [],
            "page_services": [],
            "view_all_url": "#"
        }

    if not bearer_token:
        logging.error("Bearer token is missing or empty.")
        return {
            "services": [],
            "page_services": [],
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
        logging.info(f"Calling {SERVICE_SEARCH_ENDPOINT} with org={organization_id}")
        logging.debug(f"Headers: {headers}")
        logging.debug(f"Params: {params}")

        async with httpx.AsyncClient(timeout=100.0) as client: # Set timeout to 100sec for request
            url = SERVICE_SEARCH_ENDPOINT.format(organization_id=organization_id)
            response = await client.get(
                url,
                params=params,
                headers=headers
            )

        logging.debug(f"HTTP status: {response.status_code}")
        logging.debug(f"Raw response: {response.text}")

        if response.status_code != 200:
            logging.warning(f"Service fetch failed for org {organization_id} — status {response.status_code}")
            return {
                "services": [],
                "page_services": [],
                "view_all_url": "#"
            }

        payload = response.json()
        if not payload.get("success") or "data" not in payload:
            logging.warning(f"Invalid payload structure for org {organization_id}: {payload}")
            return {
                "services": [],
                "page_services": [],
                "view_all_url": "#"
            }

        full_page_data = payload["data"]
        formatted = [
            {
                "name": item.get("name", "Unnamed Service"),
                "description": item.get("description", "No description provided."),
                "duration": item.get("duration", ""),
                "amount": item.get("amount", ""),
                "id": item.get("service_id", "")
            }
            for item in full_page_data if isinstance(item, dict)
        ]

        return {
            "services": formatted[:5],
            "page_services": formatted,
            "view_all_url": SEARCH_SERVICE_URL
        }

    except httpx.RequestError as e:
        logging.error(f"HTTPX request error during service fetch: {e!r}")
        return {
            "services": [],
            "page_services": [],
            "view_all_url": "#"
        }

    except Exception as e:
        logging.error(f"Unexpected error during service fetch: {e!r}")
        return {
            "services": [],
            "page_services": [],
            "view_all_url": "#"
        }
