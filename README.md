# 公众号写作与石墨极简排版

一个用于微信公众号的新写、润色与排版 Skill：生成 Markdown 源稿、纯正文 HTML，以及带富文本复制按钮的浏览器预览页。

## 能力

- 区分新写、润色和纯排版，纯排版保留原文内容。
- 石墨灰、白底、细线与留白，按需强调关键词。
- 提供引言、章节、引用、列表、表格、代码及图片组件。
- 静态校验正文，预览复制只包含文章区域。
- 图片必须经过逐图加载和公众号粘贴实测；不把本地路径、失效链接或占位图当作完成。

## 安装到 Codex

Windows PowerShell 示例：

```powershell
git clone https://github.com/weiqing010305-art/weiqing-graphite-writer-skill.git "$env:USERPROFILE\.agents\skills\weiqing-graphite-writer"
```

目标目录已存在时，先备份并比较内容。其他系统可将整个仓库放在 `~/.agents/skills/weiqing-graphite-writer`，保留目录结构。

调用示例：

```text
用 $weiqing-graphite-writer 写一篇公众号文章，主题是……
用 $weiqing-graphite-writer 把这份 Markdown 排成石墨极简风，保留原文内容。
```

## 查看效果

下载仓库后，用浏览器打开 [完整示例预览](examples/石墨极简_效果示例_预览.html)。`assets/preview-template.html` 是空模板，不是示例成品。

点击右上角“复制到公众号”，再粘贴到微信公众号编辑器。自动复制失败时，正文会保持选中，直接按 Ctrl/⌘+C。静态校验和逻辑测试不能保证所有浏览器及编辑器的实际粘贴效果。

## 脚本

需要 Python 3，运行脚本不需要第三方依赖。Windows 的 `python` 无法运行时可改用 `py -3`。

```powershell
python scripts/validate_gzh_html.py article.html
python scripts/wrap_preview.py article.html
```

含图片的文章只有在逐图加载及公众号粘贴实测通过后，才使用：

```powershell
python scripts/wrap_preview.py article.html --images-verified
```

该参数记录实际验证，不自动完成验证；HTTPS 图片地址也不能单独证明粘贴可用。脚本拒绝覆盖现有预览，重复生成时请指定新的输出路径。

## 测试

```powershell
python -m unittest discover -s tests -v
node tests/test_clipboard.cjs
```

第二条为可选 Node.js 测试，用 DOM 替身验证复制分支，不是浏览器端测试。

## 文件

- `SKILL.md`：入口与流程。
- `references/`：写作指南与组件库。
- `scripts/`：HTML 校验及预览生成。
- `assets/`：预览模板。
- `tests/`：回归检查。
- `examples/`：示例源稿、正文及预览。

## 来源与许可

组件库改编自 gzh-design（甲木 × 摸鱼小李），保留 AGPL-3.0 许可证，见 [LICENSE-gzh-design.txt](LICENSE-gzh-design.txt)。
