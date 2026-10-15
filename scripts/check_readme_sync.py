"""检查中文 README 入口与旧中文链接兼容页，保留原检查命令名。"""
import argparse
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def compatibility_page(text):
    title = text.splitlines()[0]
    lines = [title, '', '文档已统一使用中文，正文请查看 [当前文档](README.md)。', '']
    for anchor, heading in re.findall(r'<a id="([^"]+)"></a>\s*\n\s*## ([^\n]+)', text):
        lines.extend([f'<a id="{anchor}"></a>', '', f'[查看：{heading}](README.md#{anchor})', ''])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-redirects', action='store_true', help='更新已有 README.zh.md 兼容页')
    args = parser.parse_args()
    pages = [p for p in sorted(ROOT.rglob('README.md'))
             if not any(part.startswith('.') for part in p.relative_to(ROOT).parts)]
    errors = []
    for path in pages:
        text = path.read_text()
        relative = path.relative_to(ROOT)
        if not re.search(r'[\u4e00-\u9fff]', text) or '<sub>**简体中文**</sub>' not in text:
            errors.append(f'{relative}: 缺少中文内容或中文标识')
        links = re.findall(r'\]\(([^)]+)\)', text)
        old_local_links = any(not urlsplit(link).scheme and not urlsplit(link).netloc
                              and 'README.zh.md' in urlsplit(link).path for link in links)
        if re.search(r'\[English\]|\*\*English\*\*', text) or old_local_links:
            errors.append(f'{relative}: 存在旧语言切换或非规范正文链接')
        if path.parent != ROOT and not re.search(r'^\[← [^\]]+\]\(\.\./README\.md\)', text, re.M):
            errors.append(f'{relative}: 缺少直接上级导航')
        zh = path.with_name('README.zh.md')
        if zh.exists():
            expected = compatibility_page(text)
            if args.write_redirects:
                zh.write_text(expected)
            elif zh.read_text() != expected:
                errors.append(f'{zh.relative_to(ROOT)}: 兼容页需更新（--write-redirects）')
    for zh in ROOT.rglob('README.zh.md'):
        if not zh.with_name('README.md').exists():
            errors.append(f'{zh.relative_to(ROOT)}: 缺少中文正文入口')
    for error in errors:
        print(error)
    print(f'已检查 {len(pages)} 个中文 README 入口；{len(errors)} 个错误。')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
