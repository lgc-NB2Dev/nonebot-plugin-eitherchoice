from nonebot import get_driver
from pydantic import BaseModel


class ConfigModel(BaseModel):
    either_choice_lang: str = "zh-CN"
    either_choice_allow_public: bool = True


config: ConfigModel = ConfigModel.parse_obj(get_driver().config.dict())
