"""Check repository Markdown local file links and image sources (no network)."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import subprocess
import sys

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        self.links.extend(value for key, value in attrs if key in ("href", "src") and value)


def main():
    files = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    ).decode().split("\0")
    parser = MarkdownIt("commonmark")
    errors = []
    count = 0
    for filename in sorted(set(files)):
        if not filename.endswith(".md"):
            continue
        path = ROOT / filename
        if not path.exists():
            continue
        count += 1
        links = []
        tokens = list(parser.parse(path.read_text()))
        while tokens:
            token = tokens.pop()
            tokens.extend(token.children or [])
            if token.type in ("link_open", "image"):
                links.append(token.attrGet("href") or token.attrGet("src"))
            elif token.type in ("html_inline", "html_block"):
                html = HTMLLinks()
                html.feed(token.content)
                links.extend(html.links)
        for link in links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (path.parent / unquote(url.path)).resolve()
            if not target.exists():
                errors.append(f"{filename}: missing local target {link}")
    for error in errors:
        print(error)
    print(f"Checked local file/image links in {count} Markdown files; {len(errors)} errors.")
    print("Remote URLs and heading fragments are not checked by this command.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
