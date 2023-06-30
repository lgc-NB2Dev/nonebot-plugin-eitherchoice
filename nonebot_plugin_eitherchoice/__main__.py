import string
from typing import Tuple

from nonebot import logger, on_command
from nonebot.internal.adapter import Message
from nonebot.internal.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot_plugin_saa import Image, MessageFactory

from .data_source import get_choice_pic

STRIP_CHARS = "'\"“”‘’"
ARG_PREFIX = ("下", "一下")


def strip_prefix(s: str) -> str:
    for p in ARG_PREFIX:
        if s.startswith(p):
            return s[len(p) :]
    return s


async def check_rule(state: T_State, arg: Message = CommandArg()) -> bool:
    arg_str = arg.extract_plain_text()

    if arg_str.count("和") != 1:
        return False

    ta, tb = arg_str.split("和")
    ta = strip_prefix(ta.strip()).strip(STRIP_CHARS)
    tb = tb.strip(string.whitespace + STRIP_CHARS)
    if not (ta and tb):
        return False

    state["things"] = ta, tb
    return True


cmd_choice = on_command(
    "对比",
    rule=check_rule,
    aliases={"比较", "锐评", "评价", "如何评价"},
)


@cmd_choice.handle()
async def _(matcher: Matcher, state: T_State):
    things: Tuple[str, str] = state["things"]
    # await matcher.finish(f"Things: {things}")

    await matcher.send("请稍等，AI 正在帮你评价...")
    try:
        pic = await get_choice_pic(*things)
    except Exception:
        logger.exception("发生错误")
        logger.error("如果多次发生 Server disconnected 错误，请尝试增加 retry 次数")
        await matcher.finish("发生错误，请检查后台日志")

    await MessageFactory(Image(pic)).finish()
