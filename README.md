# 公众号写作 + 石墨极简排版

本仓库保存优化前的原版 `weiqing-graphite-writer` Skill，包含原始入口、写作指南、组件库、HTML 校验器和预览生成脚本。

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
