from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="EitherChoice",
    description="让 AI 列出两个事物的优劣",
    usage="指令：锐评 要顶的事物 和 要踩的事物\n例：锐评 Python 和 JavaScript",
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-eitherchoice",
    config=ConfigModel,
    supported_adapters={
        "~onebot.v11",
        "~onebot.v12",
        "~kaiheila",
        "~qqguild",
        "~telegram",
    },
    extra={"License": "MIT", "Author": "student_2333"},
)
