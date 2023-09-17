from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.1.3"
__plugin_meta__ = PluginMetadata(
    name="EitherChoice",
    description="让 AI 帮你对比两件事物",
    usage=(
        "▶ 指令：(对比/比较/锐评/评价/如何评价)[下/一下] 要顶的事物 (和/与/and/vs/&) 要踩的事物\n"
        "▶ 示例：\n"
        "    ▷ 对比 Python 和 JavaScript\n"
        "    ▷ 锐评一下 C# & Java\n"
        "    ▷ 比较 下北泽 与 东京 (加上空格防止 `下` 或 `一下` 被当做指令的一部分去除)"
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
        "~feishu",
        "~red",
    },
    extra={"License": "MIT", "Author": "student_2333"},
)
