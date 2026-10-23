# 公众号写作 + 图表制作 + 石墨极简排版

本仓库提供 `weiqing-graphite-writer` Skill，包含写作与图表制作指南、石墨极简组件库、HTML 校验器和预览生成脚本。

新写文章默认生成并嵌入实际图表：常规长文约 3–5 张，至少 1 张信息型图表。AI 生图适合封面、场景和概念插图；Python 适合数据图、流程图及精确中文标签。数据须有依据，成图须检查字体与手机端可读性；仅排版已有稿件时保留原图。

交付包含独立图片，以及 Python 制图脚本、输入数据或 AI 提示词。本地图片需上传公众号素材库并在对应位置插入，复制正文不代表图片已上传。

## 安装

Windows PowerShell：

```powershell
git clone https://github.com/weiqing010305-art/weiqing-graphite-writer-skill.git "$env:USERPROFILE\.agents\skills\weiqing-graphite-writer"
```

目标已存在时先备份，避免覆盖已有修改。其他系统可将仓库放入 `~/.agents/skills/weiqing-graphite-writer`。

## 使用

```text
用 $weiqing-graphite-writer 写一篇公众号文章，主题是……
用 $weiqing-graphite-writer 将这份稿件排成石墨极简风。
```

详细流程与规则见 [SKILL.md](SKILL.md)。

## 预览

`assets/preview-template.html` 是预览外壳，单独打开没有文章正文。生成正文 HTML 后运行：

```powershell
python scripts/validate_gzh_html.py article.html
python scripts/wrap_preview.py article.html
```

需要 Python 3。Windows 中 `python` 不可用时可改用 `py -3`。

生成的 `article_预览.html` 可在浏览器打开，并通过“复制到公众号”按钮复制正文。实际粘贴效果需在目标编辑器检查。

[示例预览](examples/石墨极简_效果示例_预览.html) 使用原版预览外壳；示例正文仅用于展示，并非原版 Skill 的组成文件。

## 来源与许可

组件库改编自 gzh-design（甲木 × 摸鱼小李），原 AGPL-3.0 许可证见 [LICENSE-gzh-design.txt](LICENSE-gzh-design.txt)。
