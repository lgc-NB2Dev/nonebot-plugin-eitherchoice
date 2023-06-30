import time
import urllib.parse
from pathlib import Path
from typing import AsyncIterator, Optional

import jinja2
import markdown
from httpx import AsyncClient
from nonebot import logger
from nonebot_plugin_htmlrender.data_source import get_new_page, read_tpl

from .config import config

RES_PATH = Path(__file__).parent / "res"
HTML_TEMPLATE = jinja2.Template((RES_PATH / "template.html.jinja").read_text("u8"))


async def render_image(thing_a: str, thing_b: str, content: str) -> bytes:
    parsed_md = markdown.markdown(
        content,
        extensions=[
            "pymdownx.tasklist",
            "tables",
            "fenced_code",
            "codehilite",
            "mdx_math",
            "pymdownx.tilde",
        ],
        extension_configs={"mdx_math": {"enable_dollar_delimiter": True}},
    )

    katex_js = await read_tpl("katex/katex.min.js")
    mathtex_js = await read_tpl("katex/mathtex-script-type.min.js")
    extra = f"<script defer>{katex_js}</script><script defer>{mathtex_js}</script>"
    css_txt = "\n\n".join(
        (
            await read_tpl("github-markdown-light.css"),
            await read_tpl("pygments-default.css"),
            await read_tpl("katex/katex.min.b64_fonts.css"),
        ),
    )

    rendered_html = HTML_TEMPLATE.render(
        css=css_txt,
        main_font=config.either_choice_main_font,
        code_font=config.either_choice_code_font,
        a=thing_a,
        b=thing_b,
        table=parsed_md,
        extra=extra,
    )

    async with get_new_page(
        viewport={"width": config.either_choice_pic_width, "height": 720},
    ) as page:
        await page.goto(RES_PATH.as_uri())
        await page.set_content(rendered_html, wait_until="networkidle")

        elem = await page.query_selector(".body")
        assert elem
        return await elem.screenshot(type="jpeg")


def url_enc(s: str) -> str:
    return urllib.parse.quote(s, safe="")


def build_referer(thing_a: str, thing_b: str) -> str:
    return (
        f"https://eitherchoice.com/fighting/{url_enc(thing_a)}-vs-{url_enc(thing_b)}?"
        f"t={time.time() * 1000:.0f}&p={config.either_choice_allow_public}"
    )


async def get_choice_stream(
    thing_a: str,
    thing_b: str,
    referer: Optional[str] = None,
) -> AsyncIterator[str]:
    if not referer:
        referer = build_referer(thing_a, thing_b)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 "
            "Safari/537.36"
        ),
        "Origin": "https://eitherchoice.com",
        "Referer": referer,
    }
    body = {
        "A": thing_a,
        "B": thing_b,
        "allowPublic": config.either_choice_allow_public,
        "lang": config.either_choice_lang,
    }

    async with AsyncClient(  # noqa: SIM117
        timeout=config.either_choice_timeout,
        proxies=config.proxy,
        http2=True,
        headers=headers,
    ) as client:
        async with client.stream(
            "POST",
            "https://eitherchoice.com/api/prompt/ask",
            json=body,
        ) as stream:
            async for chunk in stream.aiter_text():
                yield chunk


async def get_choice_all(
    thing_a: str,
    thing_b: str,
    retry: int = 2,
    referer: Optional[str] = None,
) -> str:
    retry -= 1

    if not referer:
        referer = build_referer(thing_a, thing_b)
    logger.info(f"Referer: {referer}")

    try:
        return "".join([i async for i in get_choice_stream(thing_a, thing_b, referer)])
    except Exception as e:
        if retry > 0:
            logger.opt(exception=e).warning(
                f"Failed to get choice, retrying ({retry} left)",
            )
            return await get_choice_all(thing_a, thing_b, retry, referer)
        raise


async def get_choice_pic(thing_a: str, thing_b: str) -> bytes:
    return await render_image(thing_a, thing_b, await get_choice_all(thing_a, thing_b))
