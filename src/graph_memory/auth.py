from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from datetime import datetime

from graph_memory.errors import AuthenticationError
from graph_memory.models import ApiKeyRecord


def hash_api_key(raw_api_key: str) -> str:
    digest = hashlib.sha256(raw_api_key.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii")


def verify_api_key(raw_api_key: str, expected_hash: str) -> bool:
    candidate = hash_api_key(raw_api_key)
    return hmac.compare_digest(candidate, expected_hash)


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)


@dataclass(slots=True)
class AuthenticatedPrincipal:
    api_key_id: str
    tenant_id: str
    name: str = ""


def principal_from_record(record: ApiKeyRecord | None, raw_api_key: str) -> AuthenticatedPrincipal:
    if record is None or record.status != "active":
        raise AuthenticationError("Invalid API key.")
    if not verify_api_key(raw_api_key, record.key_hash):
        raise AuthenticationError("Invalid API key.")
    return AuthenticatedPrincipal(api_key_id=record.api_key_id, tenant_id=record.tenant_id, name=record.name)


def iso_now() -> str:
    return datetime.utcnow().isoformat() + "Z"
