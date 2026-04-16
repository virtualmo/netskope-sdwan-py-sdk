import pytest

SDK_ENV_VARS = [
    "NETSKOPESDWAN_BASE_URL",
    "NETSKOPESDWAN_TENANT_URL",
    "NETSKOPESDWAN_API_TOKEN",
    "NETSKOPESDWAN_TIMEOUT",
    "NETSKOPESDWAN_SDWAN_TENANT_NAME",
    "NETSKOPESDWAN_AUDIT_FROM",
    "NETSKOPESDWAN_AUDIT_TO",
    "NETSKOPESDWAN_AUDIT_TYPE",
    "NETSKOPESDWAN_AUDIT_SUBTYPE",
    "NETSKOPESDWAN_AUDIT_ACTIVITY",
    "NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME",
]


@pytest.fixture(autouse=True)
def clear_sdk_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in SDK_ENV_VARS:
        monkeypatch.delenv(key, raising=False)
