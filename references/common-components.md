# 石墨极简补充组件 —— 代码、图片与标签

按需读取。本技能专用配色已经归一为石墨灰，不需要再换色。主题库有等价组件时优先用主题库；内容边界和正文兼容性约定以 SKILL.md 为准。

---

## 一、代码块组件（Markdown ``` 围栏 → 这里）

文章里的代码、命令、Prompt 提示词、配置等，**必须用代码块组件**，不要塞进普通段落或引用块。代码块内的英文、半角符号、缩进都要原样保留（代码不适用"中文全角标点"规则）。

### 1a. 深色代码块（默认，技术感强，适配所有主题）

```html
<section style="margin:0 0 20px;border-radius:8px;overflow:hidden;background:#27272A;box-shadow:0 4px 16px -8px rgba(15,23,42,0.4);">
  <section style="display:flex;align-items:center;padding:9px 14px;background:#18181B;">
    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#71717A;margin-right:7px;font-size:0px;line-height:0;overflow:hidden;"><span leaf=""><br></span></span>
    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#A1A1AA;margin-right:7px;font-size:0px;line-height:0;overflow:hidden;"><span leaf=""><br></span></span>
    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#D4D4D8;font-size:0px;line-height:0;overflow:hidden;"><span leaf=""><br></span></span>
    <span style="margin-left:12px;font-size:12px;color:#64748B;font-family:Consolas,Monaco,monospace;letter-spacing:1px;"><span leaf="">python</span></span>
  </section>
  <section style="padding:11px 14px;">
    <p style="margin:0;overflow-wrap:anywhere;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf="">def make_skill(name):</span></p>
    <p style="margin:0;overflow-wrap:anywhere;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf="">&nbsp;&nbsp;&nbsp;&nbsp;return f"已生成 {name}"</span></p>
    <p style="margin:0;overflow-wrap:anywhere;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf="">print(make_skill("gzh-design"))</span></p>
  </section>
</section>
```

要点（**关键，避免大段空白**）：① 顶栏灰阶圆点 + 语言名（无语言可删该 span）；② **每行代码用一个 `<p style="margin:0;...">`，不要用 `white-space:pre`**——否则 HTML 源码里 span 前的缩进和行间换行会被原样渲染成大左缩进 + 空行；③ 原始代码先 HTML 转义；空格用 `&nbsp;` 显示，制表符按 4 列展开，空行用 `<br>`；不使用全角空格替换代码；④ 行距只靠 `line-height:1.6` 控制，padding 用 `11px 14px`，保持紧凑；⑤ 长行段落增加 `overflow-wrap:anywhere` 并检查手机预览。

### 1b. 浅色代码块（石墨灰浅色版）

```html
<section style="margin:0 0 20px;border-radius:8px;overflow:hidden;background:#F6F8FA;border:1px solid #E5E7EB;border-left:3px solid #52525B;">
  <section style="padding:7px 14px;border-bottom:1px solid #E5E7EB;">
    <span style="font-size:12px;color:#9CA3AF;font-family:Consolas,Monaco,monospace;letter-spacing:1px;"><span leaf="">bash</span></span>
  </section>
  <section style="padding:11px 14px;">
    <p style="margin:0;overflow-wrap:anywhere;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#24292F;"><span leaf="">npx skills add gzh-design</span></p>
  </section>
</section>
```


### 1c. 行内代码（正文中的 `code` 短片段）

```html
<span style="background:#F1F5F9;color:#52525B;padding:1px 6px;border-radius:4px;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:14px;"><span leaf="">SKILL.md</span></span>
```


---

## 二、图片 / GIF 组件（Markdown `![](...)` → 这里）

文章里**每一处图片、GIF、截图占位都要保留并转成下面的组件**，不得遗漏；最终 src 使用经加载和公众号粘贴实测的 HTTPS 图片地址；原始图片来源保留在 Markdown。相对路径和本地图片需先处理为可复制素材，不能只让预览显示就交付。GIF 动图与普通图片都用 `<img>`（播放效果需实际检查），区别只在加不加"动图"角标说明。

### 2a. 标准图片（带说明）

```html
<section style="background:#FFF;border-radius:12px;padding:6px;border:1px solid #E5E7EB;box-shadow:0 4px 12px -2px rgba(0,0,0,0.08);margin-bottom:8px;">
  <section style="margin:0;border-radius:8px;overflow:hidden;">
    <span leaf=""><img src="图片URL" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
  </section>
</section>
<p style="font-size:12px;color:#9CA3AF;text-align:center;margin:0 0 24px;">
  <span leaf="">— 图片说明文字</span>
</p>
```

无说明文字时删掉下方 `<p>`，并把图片容器 `margin-bottom` 改回 `10px`。

> **图片尺寸自适应**：`<img>` 用 `max-width:100%;height:auto;display:block;margin:0 auto`——按图片自身尺寸显示并居中，大图缩到容器宽、小图保持原尺寸，**不用 `width:100%` 强制铺满**（小图被拉伸会糊）。

### 2b. GIF 动图（同图片，加"GIF 动图"角标）

```html
<section style="background:#FFF;border-radius:12px;padding:6px;border:1px solid #E5E7EB;box-shadow:0 4px 12px -2px rgba(0,0,0,0.08);margin-bottom:8px;">
  <section style="margin:0;border-radius:8px;overflow:hidden;">
    <span leaf=""><img src="动图URL.gif" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
  </section>
</section>
<p style="text-align:center;margin:0 0 24px;">
  <span style="display:inline-block;border:1px solid #52525B;color:#52525B;font-size:11px;font-weight:700;padding:1px 8px;border-radius:4px;margin-right:6px;"><span leaf="">GIF 动图</span></span>
  <span style="color:#9CA3AF;"><span leaf="">动图说明文字</span></span>
</p>
```

石墨极简中 GIF 角标用透明底和细线描边。若没有经验证的真实地址，标记素材阻塞，不生成失效 img，不编造图床链接。示例地址必须替换为真实素材并实测粘贴。

---

### 2c. 待补素材占位（**居中板块**，用于 GIF / 录屏 / 视频 / 成果图待补处）

**仅草稿使用，不能作为可直接复制的最终图片交付。**文章里 `【插入xxx】`、待录屏、待补 GIF/视频/截图等占位，用这个**居中**板块，不要用左对齐的提示块。所有排版风格通用，浅底柔虚线框 + 居中图标与说明，一眼看出"此处待补"。

```html
<section style="margin:0 0 24px;padding:30px 20px;border:1.5px dashed #DAD7D2;border-radius:14px;background:#FAFAF8;text-align:center;">
  <p style="margin:0 0 10px;font-size:24px;line-height:1;"><span leaf="">🎬</span></p>
  <p style="margin:0;font-size:14px;font-weight:700;color:#9CA3AF;letter-spacing:1px;"><span leaf="">待补素材</span></p>
  <p style="margin:8px 0 0;font-size:13px;color:#B8B5B0;line-height:1.7;"><span leaf="">此处插入：创建 skill 的录屏演示</span></p>
</section>
```

- 图标按素材类型换：🎬 视频/录屏、🖼 图片、📊 信息图、📎 附件。
- 这是**唯一允许用虚线框（dashed）的场景**——因为它表达"占位/待补"语义，与正文强调用的小标签不冲突。
- 各主题可把虚线色/底色微调成主题中性色，但保持居中、留白、柔和。

---

## 三、小标签标题组件（突出标题/强调，**替代虚线框**）

> **设计取向**：强调一段内容或起一个小标题时，优先用下面的"小标签 / 左竖条"形式，**不要用四周虚线框（dashed）包一个标题**——虚线框笨重、抢戏。小标签更轻、更现代。
>
> **使用优先级**：先查所选主题库的映射规则——主题库有等价语义组件（自己的金句块/提示块/小标题）就用主题库版本保持气质一致；没有时才用本节组件保持当前石墨配色。
>

### 3a. 左竖条小标题（最推荐，干净）

```html
<p style="margin:28px 0 14px;font-size:16px;font-weight:800;color:#1C1917;line-height:1.5;border-left:4px solid #52525B;padding-left:12px;">
  <span leaf="">小标题文字</span>
</p>
```

### 3b. 药丸标签小标题（实色底，最醒目）

```html
<p style="margin:28px 0 14px;">
  <span style="display:inline-block;background:#52525B;color:#FFFFFF;font-size:14px;font-weight:700;padding:5px 16px;border-radius:6px;"><span leaf="">小标题文字</span></span>
</p>
```

### 3c. 序号药丸 + 标题（清单/步骤）

```html
<p style="margin:24px 0 12px;font-size:15px;font-weight:800;color:#1C1917;line-height:1.6;">
  <span style="display:inline-block;background:#F4F4F5;color:#27272A;border-radius:5px;padding:1px 9px;margin-right:8px;font-weight:900;"><span leaf="">01</span></span>
  <span leaf="">要点标题</span>
</p>
```

### 3d. 金句引用（左竖条版，取代旧的虚线框金句）

```html
<section style="margin:0 0 24px;background:#FAFAFA;border-radius:0 10px 10px 0;border-left:4px solid #52525B;padding:16px 20px;">
  <p style="font-size:16px;font-weight:800;color:#27272A;margin:0;line-height:1.8;">
    <span leaf="">「这里是核心观点或关键金句」</span>
  </p>
</section>
```

### 3e. 提示 / 旁注块（左竖条 + 类型小标签，取代旧的虚线提示框）

```html
<section style="margin:0 0 24px;background:#FAFAFA;border-radius:0 8px 8px 0;border-left:4px solid #52525B;padding:14px 18px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;background:#52525B;color:#FFFFFF;font-size:11px;font-weight:700;padding:2px 10px;border-radius:4px;letter-spacing:1px;"><span leaf="">提示</span></span>
  </p>
  <p style="font-size:14px;color:#374151;margin:0;line-height:1.8;">
    <span leaf="">提示或旁注的正文内容</span>
  </p>
</section>
```

类型小标签文字可换：`提示` / `注意` / `重点` / `Prompt` / `旁注` 等。整块**没有任何 dashed 边框**，靠左竖条 + 浅底 + 小标签区分层次。

---

## 选用速记

| 文章里出现 | 用哪个组件 |
|---|---|
| ` ``` 代码 / 命令 / Prompt 围栏 ``` ` | 1a 深色（默认）或 1b 浅色代码块 |
| 行内 `` `code` `` | 1c 行内代码 |
| `![](图片)` | 2a 标准图片 |
| `![](xxx.gif)` 或注明动图 | 2b GIF 动图 |
| 想给一段起小标题 / 强调 | 3a 左竖条（首选）/ 3b 药丸 / 3c 序号 |
| `> 金句` | 3d 金句左竖条块 |
| 提示 / 注意 / 旁注 | 3e 提示左竖条块（**不要用虚线框**） |
