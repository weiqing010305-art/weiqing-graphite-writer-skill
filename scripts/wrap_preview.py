#!/usr/bin/env python3
"""Wrap a validated section fragment in the local copy preview."""
import argparse
import html
import sys
from pathlib import Path
from validate_gzh_html import validate


def render_preview(content, title, template, *, images_verified=False):
    errors, warnings, _ = validate(content)
    if errors:
        raise ValueError('正文校验失败：' + '；'.join(errors))
    if any('图片地址静态检查' in warning for warning in warnings) and not images_verified:
        raise ValueError('含图片的正文尚未完成公众号粘贴实测，不能交付可复制预览；实测通过后使用 --images-verified')
    if template.count('<!--GZH_CONTENT-->') != 1 or '{{TITLE}}' not in template:
        raise ValueError('预览模板缺少或重复插槽')
    # Replace template slots before inserting user content: literal {{TITLE}}
    # inside the article must never be rewritten.
    page = template.replace('{{TITLE}}', html.escape(title, quote=True))
    return page.replace('<!--GZH_CONTENT-->', content), warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('file', type=Path)
    ap.add_argument('output', nargs='?', type=Path)
    ap.add_argument('--images-verified', action='store_true', help='仅在逐图加载及公众号粘贴实测通过后使用，不能凭 HTTPS 地址判断')
    args = ap.parse_args()
    src = args.file.resolve()
    out = (args.output or src.with_name(src.stem + '_预览.html')).resolve()
    if src == out:
        ap.error('预览路径不能覆盖正文文件')
    if out.exists():
        ap.error('预览文件已存在，请指定新的输出路径')
    try:
        content = src.read_text(encoding='utf-8-sig').strip()
        template = (Path(__file__).resolve().parent.parent / 'assets' / 'preview-template.html').read_text(encoding='utf-8-sig')
        page, warnings = render_preview(content, src.stem, template, images_verified=args.images_verified)
        # Relative images and links resolve relative to their original article.
        if out.parent != src.parent:
            raise ValueError('预览须与正文位于同一目录，以保留相对图片和链接')
        with out.open('x', encoding='utf-8') as handle:
            handle.write(page)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'生成失败：{exc}', file=sys.stderr)
        return 1
    print(f'已生成预览：{out}')
    for warning in warnings:
        print('WARNING: ' + warning)
    print('打开预览，复制正文，再粘贴到公众号。')
    return 0

if __name__ == '__main__':
    sys.exit(main())
