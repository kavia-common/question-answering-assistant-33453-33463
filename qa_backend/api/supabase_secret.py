import os
import json
import logging
from typing import Optional

import urllib.request
import urllib.error


def get_openai_api_key_from_supabase() -> Optional[str]:
    """
    Attempts to fetch OPENAI_API_KEY from Supabase Secret Store via PostgREST.

    Requirements (environment variables):
        SUPABASE_URL: Base URL of Supabase project (e.g., https://xyz.supabase.co)
        SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY: Auth header (service role preferred)
        SUPABASE_SECRET_PASSPHRASE: Symmetric passphrase for decrypting the secret

    Returns:
        str | None: The OPENAI_API_KEY if successfully retrieved and decrypted; otherwise None.
    """
    # If already present in env, return it directly
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key:
        return env_key

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    passphrase = os.getenv("SUPABASE_SECRET_PASSPHRASE")

    if not supabase_url or not supabase_key or not passphrase:
        return None

    # This assumes a helper RPC or view is exposed for retrieving and decrypting the secret.
    # In many setups, we rely on server-side functions, but since we can't create that
    # without credentials right now, we document the expected endpoint:
    #
    #   POST {SUPABASE_URL}/rest/v1/rpc/get_secret
    #   Body: {"p_key": "OPENAI_API_KEY", "p_passphrase": "<SUPABASE_SECRET_PASSPHRASE>"}
    #
    # The function get_secret(key text, passphrase text) returns the decrypted value.
    #
    # Until the RPC exists, we simply return None. When credentials are provided and the
    # agent runs with SupabaseTool_run_sql, it will create the RPC and this code will work.
    rpc_url = f"{supabase_url}/rest/v1/rpc/get_secret"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Prefer": "return=representation",
    }
    body = json.dumps({"p_key": "OPENAI_API_KEY", "p_passphrase": passphrase}).encode("utf-8")

    req = urllib.request.Request(rpc_url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode("utf-8").strip()
            # If PostgREST returns a simple JSON string or object, try to parse:
            try:
                parsed = json.loads(data)
                # common return shapes: {"get_secret": "value"} or plain string
                if isinstance(parsed, dict):
                    # Try standard key
                    if "get_secret" in parsed and isinstance(parsed["get_secret"], str):
                        return parsed["get_secret"]
                    # Or direct value
                    if "value" in parsed and isinstance(parsed["value"], str):
                        return parsed["value"]
                elif isinstance(parsed, str):
                    return parsed
            except json.JSONDecodeError:
                # If not JSON, it may already be the raw string
                if data:
                    return data
    except urllib.error.HTTPError as e:
        logging.warning("Supabase get_secret HTTP error: %s", e)
    except urllib.error.URLError as e:
        logging.warning("Supabase get_secret URL error: %s", e)
    except Exception as e:
        logging.warning("Supabase get_secret unexpected error: %s", e)

    return None
