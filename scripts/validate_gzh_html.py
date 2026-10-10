#!/usr/bin/env python3
"""Validate this skill's HTML profile, not official WeChat behavior.

Exit 1 on errors, or on warnings with --strict; exit 2 on input failure.
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

for stream in (sys.stdin, sys.stdout, sys.stderr):
    if hasattr(stream, 'reconfigure'):
        stream.reconfigure(encoding='utf-8', errors='replace')

ALLOWED = set('section p span strong em b i u s del br img h2 h3 h4 a ul ol li table thead tbody tfoot tr th td caption colgroup col'.split())
VOID = {'br', 'img', 'col'}
CJK = re.compile(r'[\u3400-\u9fff]')
HALF_PUNCT = re.compile(r'[\u3400-\u9fff][,;!?]|[\u3400-\u9fff]\.(?!\d)')
CODE_STYLE = re.compile(r'monospace|courier|consolas|sf mono', re.I)
BAD_STYLE = re.compile(r'position\s*:\s*(?:fixed|absolute|sticky)\b|(?:^|;)\s*float\s*:|display\s*:\s*(?:inline-)?grid\b|@(?:media|keyframes|import)|var\s*\(|expression\s*\(|url\s*\(|/\*|\\', re.I)

class LeafChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, leaf, code)
        self.errors = []
        self.warnings = []
        self.roots = []
        self.span_leaf_count = 0
        self.orange_count = 0
        self.visible = False
        self.image_count = 0

    def error(self, message):
        self.errors.append(f'行 {self.getpos()[0]}：{message}')

    def handle_decl(self, decl):
        self.error('正文不得包含 DOCTYPE 或其他声明')

    def handle_pi(self, data):
        self.error('正文不得包含处理指令')

    def handle_starttag(self, tag, attrs):
        if not self.stack:
            self.roots.append(tag)
        if tag not in ALLOWED:
            self.error(f'正文不允许 <{tag}>')
        ad = dict(attrs)
        if len(ad) != len(attrs):
            self.error('重复属性')
        for key, value in attrs:
            value = value or ''
            if key in {'class', 'id', 'srcdoc', 'srcset', 'xmlns'} or key.startswith('on'):
                self.error(f'正文不允许属性 {key}')
            if key in {'href', 'src', 'background', 'action', 'xlink:href'}:
                compact = re.sub(r'[\s\x00-\x20\x7f]+', '', value)
                if compact.startswith('//') or (re.match(r'^[\w+.-]+:', compact) and not re.match(r'^https?://', compact, re.I)):
                    self.error(f'{key} 仅允许 http(s) 或相对路径')
            if key == 'style':
                if BAD_STYLE.search(value):
                    self.error('使用了本技能禁用的样式')
                for declaration in value.split(';'):
                    prop, sep, val = declaration.partition(':')
                    if sep and prop.strip().lower() == 'font-size':
                        font = re.fullmatch(r'\s*(\d+(?:\.\d+)?)px\s*(?:!important\s*)?', val, re.I)
                        if not font or float(font[1]) > 24:
                            self.error('font-size 必须为不超过 24px 的像素值')
                if tag == 'strong' and re.search(r'(?:^|;)\s*(?:font-size|border-bottom)\s*:', value, re.I):
                    self.error('strong 上不要设置字号或下划线')
                if '#f97316' in value.lower():
                    self.orange_count += 1
        if tag == 'img':
            self.image_count += 1
            self.visible = True
            src = ad.get('src', '') or ''
            if not src or '{{' in src or src in {'待补', '图片URL', '动图URL.gif'}:
                self.error('图片缺少真实地址，请使用待补素材组件')
            elif not re.match(r'^https://[^/\s]+(?:/|$)', src, re.I):
                self.error('图片必须使用可访问的 HTTPS 地址；本地、相对路径和临时地址不能作为可复制交付')
        is_leaf = tag == 'span' and 'leaf' in ad
        if is_leaf:
            self.span_leaf_count += 1
        if tag not in VOID:
            self.stack.append((tag, is_leaf, tag in {'code', 'pre'} or bool(CODE_STYLE.search(ad.get('style') or ''))))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1][0] != tag:
            self.error(f'标签闭合不匹配：</{tag}>')
            return
        self.stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        self.visible = True
        if not any(leaf for _, leaf, _ in self.stack):
            self.error(f'文字未用 span leaf 包裹：{text[:32]}')
        if not any(code for _, _, code in self.stack) and CJK.search(text):
            if HALF_PUNCT.search(text):
                self.warnings.append(f'行 {self.getpos()[0]}：疑似中文半角标点：{text[:32]}')
            if '{{' in text or re.search(r'待补|待核实|【插入', text):
                self.warnings.append(f'行 {self.getpos()[0]}：待补内容：{text[:32]}')


def validate(html, name='<input>'):
    checker = LeafChecker()
    try:
        checker.feed(html)
        checker.close()
    except Exception as exc:
        checker.errors.append(f'HTML 解析失败：{exc}')
    if checker.roots != ['section']:
        checker.errors.append('正文必须只有一个根 section，不能校验预览整页')
    if checker.stack:
        checker.errors.append('存在未闭合标签')
    if not checker.visible:
        checker.errors.append('正文为空')
    if checker.orange_count > 3:
        checker.errors.append(f'暖橙使用了 {checker.orange_count} 个元素，最多 3 个')
    if checker.image_count:
        checker.warnings.append('图片地址静态检查不能证明可复制；必须逐图检查加载并实测粘贴到公众号后显示正常')
    return checker.errors, checker.warnings, checker.span_leaf_count


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('file', nargs='?')
    ap.add_argument('--stdin', action='store_true')
    ap.add_argument('--strict', action='store_true', help='警告也返回非零退出码')
    args = ap.parse_args()
    if args.stdin and args.file:
        ap.error('file 与 --stdin 不能同时使用')
    try:
        html = sys.stdin.read() if args.stdin or not args.file else Path(args.file).read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as exc:
        print(f'无法读取输入：{exc}', file=sys.stderr)
        return 2
    errors, warnings, count = validate(html)
    print(f'正文静态校验：{args.file or "<stdin>"}；leaf={count}；ERROR={len(errors)}；WARNING={len(warnings)}')
    for kind, items in [('ERROR', errors), ('WARNING', warnings)]:
        for item in items:
            print(f'{kind}: {item}')
    if not errors:
        print('静态检查通过；实际粘贴效果仍需检查。')
    return int(bool(errors or (args.strict and warnings)))

if __name__ == '__main__':
    sys.exit(main())
