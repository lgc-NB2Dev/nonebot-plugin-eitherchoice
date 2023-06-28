<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-EitherChoice

_✨ 让 AI 帮你对比两件事物 ✨_

<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/aee0950c-6290-4b95-ab49-c0982bd7e27d">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/aee0950c-6290-4b95-ab49-c0982bd7e27d.svg" alt="wakatime">
</a>

<br />

<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-eitherchoice.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-eitherchoice">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-eitherchoice.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-eitherchoice">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-eitherchoice" alt="pypi download">
</a>

</div>

## 📖 介绍

~~让 AI 帮你一本正经地胡说八道~~

服务来自 [EitherChoice](https://eitherchoice.com/)

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-eitherchoice
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-eitherchoice
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-eitherchoice
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-eitherchoice
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-eitherchoice
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_eitherchoice"
]
```

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|            配置项            | 必填 | 默认值  |               说明                |
| :--------------------------: | :--: | :-----: | :-------------------------------: |
|           `PROXY`            |  否  |   无    |        访问接口使用的代理         |
|   `EITHER_CHOICE_TIMEOUT`    |  否  |  `90`   |       访问接口超时，单位秒        |
|     `EITHER_CHOICE_LANG`     |  否  | `zh-CN` |             目标语言              |
| `EITHER_CHOICE_ALLOW_PUBLIC` |  否  | `True`  |   是否允许 AI 上网搜索相关信息    |
|  `EITHER_CHOICE_PIC_WIDTH`   |  否  | `1280`  |     生成图片的宽度，单位像素      |
|  `EITHER_CHOICE_MAIN_FONT`   |  否  |   ...   |  生成图片的主字体，使用 CSS 格式  |
|  `EITHER_CHOICE_CODE_FONT`   |  否  |   ...   | 生成图片的代码字体，使用 CSS 格式 |

## 🎉 使用

### 指令

- 指令：对比 要顶的事物 和 要踩的事物
- 别名：比较、比较一下、锐评、如何评价
- 例：
  - 对比 Python 和 JavaScript
  - 比较一下 C# 和 Java

### 效果图

![Alt text](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/eitherchoice/example.png)

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

### [EitherChoice](https://eitherchoice.com/)

- 服务提供

## 💰 赞助

感谢大家的赞助！你们的赞助将是我继续创作的动力！

- [爱发电](https://afdian.net/@lgc2333)
- <details>
    <summary>赞助二维码（点击展开）</summary>

  ![讨饭](https://raw.githubusercontent.com/lgc2333/ShigureBotMenu/master/src/imgs/sponsor.png)

  </details>

## 📝 更新日志

芝士刚刚发布的插件，还没有更新日志的说 qwq~
