"""Regression checks for article preservation and validation boundaries."""
import html
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_gzh_html import validate
from wrap_preview import render_preview


def fragment(text='正文。'):
    return '<section><p><span leaf="">' + text + '</span></p></section>'


class ValidationTests(unittest.TestCase):
    def test_valid_chinese_english_numbers_and_entities(self):
        self.assertEqual(validate(fragment('中文。Hello, world! 3.14 &amp; &lt;script&gt;'))[:2], ([], []))

    def test_every_language_requires_leaf(self):
        for text in ['中文', 'English', '01', '·']:
            with self.subTest(text=text):
                self.assertTrue(validate('<section><p>' + text + '</p></section>')[0])

    def test_void_elements_do_not_leak_leaf_or_code_context(self):
        valid = '<section><span leaf=""><img src="https://example.com/a.png"><br></span><p>裸文本</p></section>'
        self.assertTrue(any('未用' in e for e in validate(valid)[0]))
        valid = '<section><span style="font-family:monospace"><span leaf="">代码,</span><br></span><span leaf="">正文,</span></section>'
        self.assertTrue(validate(valid)[1])

    def test_code_literals_are_not_html_or_css_violations(self):
        code = html.escape('<script> position:fixed; class="x" 中文, a = 1 < 2')
        source = '<section><p style="font-family:monospace"><span leaf="">' + code + '</span></p></section>'
        self.assertEqual(validate(source)[:2], ([], []))

    def test_nested_code_preserves_punctuation(self):
        source = '<section><p style="font-family:Consolas"><strong><span leaf="">print("中文,")</span></strong></p></section>'
        self.assertEqual(validate(source)[:2], ([], []))

    def test_english_and_version_punctuation_is_not_a_warning(self):
        self.assertEqual(validate(fragment("英文 don't、版本3.13、数字1.2。"))[1], [])

    def test_bad_attributes_and_urls(self):
        for attr in ['class="a"', 'id="a"', 'onclick="x()"', 'href="java&#x73;cript:alert(1)"', 'href="data:text/html,x"', 'srcset="x"']:
            with self.subTest(attr=attr):
                self.assertTrue(validate('<section><span leaf="" ' + attr + '>正文</span></section>')[0])

    def test_invalid_fragment_and_nesting(self):
        for source in ['', '<!DOCTYPE html>' + fragment(), fragment() + fragment(), '<section><p><span leaf="">正文</p></span></section>', '<section><span leaf="">正文</span>']:
            with self.subTest(source=source):
                self.assertTrue(validate(source)[0])

    def test_style_profile_and_strong(self):
        for style in ['font-size:32px', 'font-size:2rem', 'display:grid', 'float:left', 'position:absolute', 'color:var(--a)', 'background:url(https://example.com/a.png)']:
            with self.subTest(style=style):
                self.assertTrue(validate(fragment().replace('<p>', '<p style="' + style + '">'))[0])
        self.assertTrue(validate('<section><strong style="font-size:14px"><span leaf="">正文</span></strong></section>')[0])

    def test_orange_counts_elements_not_properties(self):
        item = '<span leaf="" style="color:#F97316;border:1px solid #F97316">重点</span>'
        self.assertFalse(validate('<section>' + item * 3 + '</section>')[0])
        self.assertTrue(validate('<section>' + item * 4 + '</section>')[0])

    def test_missing_and_local_images(self):
        self.assertTrue(validate('<section><img src="待补"></section>')[0])
        for src in ['./a.png', 'file:///a.png', 'blob:example', 'data:image/png;base64,abc', 'http://example.com/a.png']:
            with self.subTest(src=src):
                self.assertTrue(validate('<section><img src="' + src + '"></section>')[0])
        self.assertTrue(validate('<section><img src="https://example.com/a.png"></section>')[1])

    def test_cli_strict_mode_and_read_error(self):
        script = str(ROOT / 'scripts/validate_gzh_html.py')
        for flags, expected in [([], 0), (['--strict'], 1)]:
            result = subprocess.run([sys.executable, script, '--stdin', *flags], input=fragment('中文,'), text=True, encoding='utf-8', capture_output=True)
            self.assertEqual(result.returncode, expected, result.stdout)
        self.assertEqual(subprocess.run([sys.executable, script, 'missing.html'], capture_output=True).returncode, 2)


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.template = (ROOT / 'assets/preview-template.html').read_text(encoding='utf-8-sig')

    def test_title_escaped_and_body_preserved(self):
        content = fragment('字面量 {{TITLE}} &amp; 原文。')
        page, _ = render_preview(content, '<img onerror="x">', self.template)
        self.assertIn(content, page)
        self.assertIn('&lt;img onerror=&quot;x&quot;&gt;', page)
        article = page.split('<div id="gzh-content">', 1)[1].split('</div>', 1)[0].strip()
        self.assertEqual(article, content)

    def test_invalid_body_refused(self):
        with self.assertRaises(ValueError):
            render_preview('<section><script>alert(1)</script></section>', 'x', self.template)

    def test_images_require_explicit_paste_verification(self):
        content = '<section><img src="https://example.com/image.png"></section>'
        with self.assertRaises(ValueError):
            render_preview(content, 'x', self.template)
        page, warnings = render_preview(content, 'x', self.template, images_verified=True)
        self.assertIn(content, page)
        self.assertTrue(warnings)
        with self.assertRaises(ValueError):
            render_preview('<section><img src="./a.png"></section>', 'x', self.template, images_verified=True)

    def test_output_never_overwrites_source_or_existing_preview(self):
        script = str(ROOT / 'scripts/wrap_preview.py')
        with tempfile.TemporaryDirectory(dir=ROOT / 'tests') as directory:
            src = Path(directory) / 'article.html'
            src.write_text(fragment(), encoding='utf-8')
            def run(*args):
                return subprocess.run([sys.executable, script, str(src), *args], capture_output=True)
            self.assertNotEqual(run(str(src)).returncode, 0)
            self.assertEqual(run().returncode, 0)
            preview = src.with_name('article_预览.html')
            previous = preview.read_bytes()
            self.assertNotEqual(run().returncode, 0)
            self.assertEqual(preview.read_bytes(), previous)
            self.assertEqual(src.read_text(encoding='utf-8'), fragment())

    def test_component_font_sizes_and_leaf_text(self):
        for filename in ['theme-graphite-minimal.md', 'common-components.md']:
            text = (ROOT / 'references' / filename).read_text(encoding='utf-8-sig')
            for block in re.findall(r'```html\s*\n(.*?)\n```', text, re.S):
                self.assertFalse(re.search(r'font-size:\s*(?:2[5-9]|[3-9]\d|\d{3,})px', block), filename)
                # Blocks with slots for whole subcomponents are checked on assembly.
                if '{{' not in block and '<!--' not in block:
                    block = block.replace('图片URL', 'https://example.com/image.png').replace('动图URL.gif', 'https://example.com/image.gif')
                    errors, _, _ = validate('<section>' + block + '<span leaf="">示例正文</span></section>')
                    self.assertEqual(errors, [], filename)


if __name__ == '__main__':
    unittest.main()
