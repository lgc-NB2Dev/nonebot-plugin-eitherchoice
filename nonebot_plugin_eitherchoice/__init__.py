from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="EitherChoice",
    description="让 AI 帮你对比两件事物",
    usage=(
        "指令：对比 要顶的事物 和 要踩的事物\n"
        "别名：比较、比较一下、锐评、如何评价\n"
        "\n"
        "例：\n"
        "- 对比 Python 和 JavaScript\n"
        "- 比较一下 C# 和 Java"
    ),
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
