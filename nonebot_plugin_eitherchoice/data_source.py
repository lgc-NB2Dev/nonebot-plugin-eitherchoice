import time
import urllib.parse
from pathlib import Path
from typing import Optional

import jinja2
from bs4 import BeautifulSoup, Tag
from httpx import AsyncClient
from nonebot import logger
from nonebot_plugin_htmlrender.data_source import get_new_page, read_tpl

from .config import config

RES_PATH = Path(__file__).parent / "res"
HTML_TEMPLATE = jinja2.Template((RES_PATH / "template.html.jinja").read_text("u8"))

TEMPLATE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 "
        "Safari/537.36"
    ),
    "Origin": "https://eitherchoice.com",
    "Cookie": "ec_ask=1",
}


async def render_image(thing_a: str, thing_b: str, content: str) -> bytes:
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
        table=content,
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


async def get_from_page(
    thing_a: str,
    thing_b: str,
    referer: Optional[str] = None,
) -> str:
    headers = TEMPLATE_HEADERS.copy()
    if referer:
        headers["Referer"] = referer

    async with AsyncClient(
        http2=True,
        timeout=config.either_choice_timeout,
        proxies=config.proxy,
    ) as client:
        resp = await client.get(
            f"https://eitherchoice.com/fight/{url_enc(thing_a)}-vs-{url_enc(thing_b)}",
            follow_redirects=False,
        )
        resp.raise_for_status()
        text = resp.text

    logger.debug(text)
    soup = BeautifulSoup(text, "lxml")
    main = soup.find("main")
    assert isinstance(main, Tag), "main tag not found, or it is not a tag"

    elements = list(main.children)[3:-3]  # 第四个到倒数第四个，剃掉标题和脚注
    assert len(elements), "no elements found"

    return "\n".join(str(x) for x in elements)


async def ask_choice(
    thing_a: str,
    thing_b: str,
    referer: Optional[str] = None,
):
    headers = TEMPLATE_HEADERS.copy()
    if referer:
        headers["Referer"] = referer

    body = {
        "A": thing_a,
        "B": thing_b,
        "allowPublic": config.either_choice_allow_public,
        "lang": config.either_choice_lang,
    }

    async with AsyncClient(
        http2=True,
        timeout=config.either_choice_timeout,
        proxies=config.proxy,
        headers=headers,
    ) as client:
        resp = await client.post("https://eitherchoice.com/api/prompt/ask", json=body)
        if resp.status_code != 524:  # server timeout
            resp.raise_for_status()
        else:
            logger.warning(
                "Server timeout! Maybe the content is not completely generated...",
            )


async def get_choice(thing_a: str, thing_b: str) -> str:
    if not config.either_choice_force_ask:
        try:
            return await get_from_page(thing_a, thing_b)
        except Exception as e:
            logger.info(f"Fight page may not exist, asking now: {e!r}")

    referer = build_referer(thing_a, thing_b)
    logger.info(f"Referer: {referer}")

    # 这傻逼玩意真他妈头疼，搞了半天都没搞清楚这玩意的破逻辑，
    # 不搞了，我急了，摆烂！主打一个能用就行！
    for i in range(config.either_choice_retry + 1):
        try:
            await ask_choice(thing_a, thing_b, referer)
            return await get_from_page(thing_a, thing_b, referer)
        except Exception as e:
            if i == config.either_choice_retry:
                raise
            logger.warning(
                f"Failed to ask or failed to get content! "
                f"retrying ({config.either_choice_retry - i} left): {e!r}",
            )

    raise ValueError


async def get_choice_pic(thing_a: str, thing_b: str) -> bytes:
    return await render_image(thing_a, thing_b, await get_choice(thing_a, thing_b))
