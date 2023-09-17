import string
from typing import Tuple

from nonebot import logger, on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot_plugin_saa import Image, MessageFactory

from .data_source import get_choice_pic

CMD_PREFIX = ("对比", "比较", "锐评", "评价", "如何评价")
CMD_SUFFIX = ("下", "一下")
COMMANDS = CMD_PREFIX + tuple(f"{x}{y}" for x in CMD_PREFIX for y in CMD_SUFFIX)

SEP_CHARS = ("和", "与", "and", "vs", "&")
SEP_CHARS = tuple(f" {x}" for x in SEP_CHARS) + SEP_CHARS
STRIP_CHARS = "'\"“”‘’"


async def check_rule(state: T_State, arg: Message = CommandArg()) -> bool:
    arg_str = arg.extract_plain_text()
    sep = next((x for x in SEP_CHARS if x in arg_str), None)
    if not sep:
        return False

    things = tuple(
        x.strip(string.whitespace + STRIP_CHARS) for x in arg_str.split(sep, 1)
    )
    if len(things) != 2 or (not all(things)):
        return False

    state["things"] = things
    return True


first_cmd, *other_cmd = COMMANDS
cmd_choice = on_command(first_cmd, aliases=set(other_cmd), rule=check_rule)


@cmd_choice.handle()
async def _(state: T_State):
    things: Tuple[str, str] = state["things"]

    tip_receipt = await MessageFactory("请稍等，AI 正在帮你评价...").send()

    try:
        pic = await get_choice_pic(*things)
    except Exception:
        logger.exception("发生错误")
        await MessageFactory("发生错误，请稍后重试……").send(reply=True)
    else:
        await MessageFactory(Image(pic)).send(reply=True)
    finally:
        try:
            await tip_receipt.revoke()
        except Exception as e:
            logger.warning(f"撤回提示消息失败：{e!r}")
