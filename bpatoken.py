# get bpa token for authentication
from inventory import PROD2  # More explicit import
import json
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# It's generally a good practice to disable warnings for unverified HTTPS requests
# only if you understand the risks and have a specific reason to do so.
# For production, always prefer to use verify=True with a valid certificate.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bpa_token(environment_config: dict) -> str | None:
    """
    Retrieves a BPA token for authentication from the specified environment.

    Args:
        environment_config: A dictionary containing 'host' and 'Authorization' (Base64 encoded).

    Returns:
        The access token string if successful, None otherwise.
    """
    host = environment_config.get('host')
    auth_b64 = environment_config.get('Authorization')

    if not host or not auth_b64:
        logging.error("Host or Authorization not found in environment_config.")
        return None

    url = f"https://{host}/bpa/login"
    auth_header = f"Basic {auth_b64}"

    headers = {
        'Authorization': auth_header,
        'Accept': "*/*",
        # 'Host': host, # requests usually sets this automatically
        'Connection': "keep-alive", # Often managed by requests/urllib3 automatically with sessions
    }

    try:
        with requests.Session() as session:
            response = session.post(url, headers=headers, verify=False) # SECURITY RISK: verify=False
            response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)

        token_data = response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            logging.error("'access_token' not found in response.")
            return None

        logging.info("Successfully retrieved BPA token.")
        return access_token

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An unexpected error occurred with the request: {req_err}")
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON response: {response.text}")

    return None

if __name__ == "__main__":
    # Example usage:
    token = get_bpa_token(PROD2)
    if token:
        print(f"Retrieved token: {token[:20]}...") # Print first 20 chars for brevity
    else:
        print("Failed to retrieve token.")
