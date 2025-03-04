import httpx
import json
import wmill


def main(
    grist_docs_id: str,
    grist_path_credentials: str = "u/krichkorn/json_grist_credentials_sw_kukkik"
):
    try:
        _ = wmill.get_variable(grist_path_credentials)
        creds_grist = json.loads(_)
    except Exception as e:
        raise e

    assert creds_grist.get("base_url"), "Please add `base_url` in your JSON"
    assert creds_grist.get("api_key"), "Please add `api_key` in your JSON"
    grist_base_url = creds_grist.get("base_url")
    grist_api_key = creds_grist.get("api_key")

    # Define the URL
    url = f"{grist_base_url}/api/docs/{grist_docs_id}/tables"

    # Define the headers
    headers = {"accept": "application/json", "Authorization": f"Bearer {grist_api_key}"}

    # Make the GET request using httpx
    response = httpx.get(url, headers=headers)

    return response.json()
