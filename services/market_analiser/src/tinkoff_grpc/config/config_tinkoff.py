from pydantic.types import SecretStr
from pydantic_settings import SettingsConfigDict

from .config_base import ConfigBase


class ConfigTinkoff(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="TINKOFF_")
    api_token: SecretStr | None = None
    sandbox_service_endpoint: str
