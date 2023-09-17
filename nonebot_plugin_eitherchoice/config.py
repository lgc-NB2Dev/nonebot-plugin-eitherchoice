from typing import Optional

from nonebot import get_driver
from pydantic import BaseModel, validator


class ConfigModel(BaseModel):
    proxy: Optional[str] = None
    either_choice_timeout: Optional[int] = None
    either_choice_retry: int = 2
    either_choice_lang: str = "zh-CN"
    either_choice_allow_public: str = "true"
    either_choice_force_ask: bool = True
    either_choice_pic_width: int = 1280
    either_choice_main_font: str = (
        "'Microsoft YaHei UI', 'Microsoft YaHei', "
        "'Source Han Sans CN', 'Source Han Sans SC', "
        "'PingFang SC', 'Hiragino Sans GB', 'WenQuanYi Micro Hei', sans-serif"
    )
    either_choice_code_font: str = (
        "'JetBrains Mono', 'JetBrainsMono Nerd Font', "
        "'Victor Mono', 'VictorMono Nerd Font', "
        "'Fira Code', 'FiraCode Nerd Font', "
        "'Cascadia Code', 'CascadiaCode Nerd Font', "
        "'Consolas', 'Courier New', monospace"
    )

    @validator("either_choice_allow_public", pre=True)
    def either_choice_allow_public_validator(cls, v):  # noqa: N805
        v = str(v).lower()
        if v in ("true", "false"):
            return v
        raise ValueError("`either_choice_allow_public` must be `true` or `false`")


config: ConfigModel = ConfigModel.parse_obj(get_driver().config.dict())
