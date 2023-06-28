from nonebot.plugin import PluginMetadata

from . import __main__ as __main__
from .config import ConfigModel

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="EitherChoice",
    description="让 AI 帮你锐评两样东西",
    usage="指令：choice <事物1> <事物2>\n如果参数中有空格，请用引号括起来",
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-eitherchoice",
    config=ConfigModel,
    supported_adapters={"~onebot.v11"},
    extra={"License": "MIT", "Author": "student_2333"},
)
