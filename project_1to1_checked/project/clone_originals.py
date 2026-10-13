#!/usr/bin/env python3
"""Mirror both reference pages and their page resources into the local project.

Run from this directory with:  py clone_originals.py
Only Python's standard library is required. The website itself stays HTML/CSS/JS.
"""
from __future__ import annotations
import hashlib
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITES = [
    ("site-1", "https://dexxpress.uz/Snake.3-4/"),
    ("site-2", "https://dexxpress.uz/Snake.1.1-4/"),
]
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
RESOURCE_TAGS = {"img", "script", "source", "video", "audio", "track", "iframe", "embed", "object"}
LINK_RELS = {"stylesheet", "icon", "shortcut", "preload", "modulepreload", "manifest", "apple-touch-icon"}
ATTR_RE = re.compile(r'''(?P<name>[\w:-]+)\s*=\s*(?P<q>["'])(?P<value>.*?)(?P=q)''', re.I | re.S)
TAG_RE = re.compile(r'<(?P<tag>[a-z][\w:-]*)\b(?P<attrs>[^<>]*?)>', re.I | re.S)
STYLE_TAG_RE = re.compile(r'(<style\b[^>]*>)(.*?)(</style\s*>)', re.I | re.S)
CSS_URL_RE = re.compile(r'''url\(\s*(?P<q>["']?)(?P<url>.*?)(?P=q)\s*\)''', re.I | re.S)
CSS_IMPORT_RE = re.compile(r'''@import\s+(?P<q>["'])(?P<url>.*?)(?P=q)''', re.I | re.S)
SRCSET_RE = re.compile(r'''(?P<url>[^,\s]+)(?P<descriptor>\s+(?:\d+(?:\.\d+)?x|\d+w))?''')

class Mirror:
    def __init__(self, site_dir: Path, start_url: str):
        self.site_dir = site_dir
        self.start_url = start_url
        self.cache: dict[str, Path] = {}
        self.errors: list[str] = []
        self.count = 0
        self.site_dir.mkdir(parents=True, exist_ok=True)
        (self.site_dir / "assets").mkdir(exist_ok=True)

    def resolve(self, value: str, base: str) -> str | None:
        value = value.strip().strip("\"'")
        if not value or value.startswith(("#", "data:", "blob:", "javascript:", "mailto:", "tel:")):
            return None
        absolute = urllib.parse.urljoin(base, value)
        parsed = urllib.parse.urlsplit(absolute)
        if parsed.scheme not in ("http", "https"):
            return None
        return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", parsed.query, ""))

    def local_path(self, url: str) -> Path:
        p = urllib.parse.urlsplit(url)
        host = p.netloc.lower().replace(":", "_")
        decoded = urllib.parse.unquote(p.path or "/")
        parts = [x for x in decoded.replace("\\", "/").split("/") if x not in ("", ".", "..")]
        if not parts or decoded.endswith("/"):
            parts.append("index.html")
        path = self.site_dir / "assets" / "_mirror" / host
        for part in parts:
            # Avoid special Windows path characters while keeping normal asset names intact.
            part = re.sub(r'[<>:"|?*]', "_", part)
            path = path / part
        if p.query:
            suffix = path.suffix
            path = path.with_name(path.stem + "_q" + hashlib.md5(p.query.encode()).hexdigest()[:8] + suffix)
        return path

    def rel_path(self, dest: Path, from_dir: Path | None = None) -> str:
        base = from_dir or self.site_dir
        return Path(os.path.relpath(dest, base)).as_posix()

    def fetch(self, url: str) -> tuple[bytes, str, str]:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=30) as res:
            data = res.read(35 * 1024 * 1024 + 1)
            if len(data) > 35 * 1024 * 1024:
                raise ValueError("resource larger than 35 MB; skipped")
            content_type = res.headers.get("Content-Type", "")
            final_url = res.geturl()
            charset = res.headers.get_content_charset() or "utf-8"
        return data, content_type, final_url

    def save_resource(self, url: str, base_url: str) -> Path | None:
        absolute = self.resolve(url, base_url)
        if not absolute:
            return None
        if absolute in self.cache:
            return self.cache[absolute]
        dest = self.local_path(absolute)
        self.cache[absolute] = dest  # break CSS import cycles
        try:
            data, content_type, final_url = self.fetch(absolute)
            dest.parent.mkdir(parents=True, exist_ok=True)
            self.count += 1
            is_css = "text/css" in content_type.lower() or urllib.parse.urlsplit(final_url).path.lower().endswith(".css")
            if is_css:
                charset_match = re.search(r"charset=([\w.-]+)", content_type, re.I)
                charset = charset_match.group(1) if charset_match else "utf-8"
                css = data.decode(charset, errors="replace")
                css = self.rewrite_css(css, final_url, dest.parent)
                dest.write_text(css, encoding="utf-8")
            else:
                # Keep original image/font/script bytes unchanged.
                if not dest.suffix:
                    ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) if content_type else None
                    if ext:
                        dest = dest.with_suffix(ext)
                        self.cache[absolute] = dest
                dest.write_bytes(data)
            return dest
        except Exception as exc:
            self.errors.append(f"{absolute} — {exc}")
            self.cache[absolute] = None  # type: ignore[assignment]
            return None

    def rewrite_css(self, css: str, base_url: str, css_dir: Path) -> str:
        def url_repl(m: re.Match) -> str:
            raw = m.group("url").strip()
            local = self.save_resource(raw, base_url)
            if not local:
                return m.group(0)
            rel = self.rel_path(local, css_dir)
            quote = m.group("q") or ""
            return f"url({quote}{rel}{quote})"
        css = CSS_URL_RE.sub(url_repl, css)

        def import_repl(m: re.Match) -> str:
            raw = m.group("url").strip()
            local = self.save_resource(raw, base_url)
            if not local:
                return m.group(0)
            return '@import "' + self.rel_path(local, css_dir) + '"'
        css = CSS_IMPORT_RE.sub(import_repl, css)
        return css

    def rewrite_srcset(self, value: str, base_url: str) -> str:
        # The references on these pages use standard URL + width/density descriptors.
        pieces = []
        for item in value.split(","):
            tokens = item.strip().split()
            if not tokens:
                continue
            local = self.save_resource(tokens[0], base_url)
            if local:
                tokens[0] = self.rel_path(local)
            pieces.append(" ".join(tokens))
        return ", ".join(pieces)

    def rewrite_html(self, html: str, base_url: str) -> str:
        # Localize URL() assets in inline <style> blocks and style attributes.
        html = STYLE_TAG_RE.sub(lambda m: m.group(1) + self.rewrite_css(m.group(2), base_url, self.site_dir) + m.group(3), html)

        def tag_repl(match: re.Match) -> str:
            tag = match.group("tag").lower()
            attrs_text = match.group("attrs")
            attrs = {m.group("name").lower(): m.group("value") for m in ATTR_RE.finditer(attrs_text)}
            rels = set(attrs.get("rel", "").lower().split())
            allowed = set()
            if tag in RESOURCE_TAGS:
                allowed.update({"src", "poster", "data-src", "data-lazy-src", "data-original", "data-original-src"})
            if tag == "input" and attrs.get("type", "").lower() == "image":
                allowed.add("src")
            if tag == "link" and rels.intersection(LINK_RELS):
                allowed.add("href")
            if tag in ("img", "source"):
                allowed.add("srcset")
            if tag == "meta" and attrs.get("property", "").lower() in ("og:image", "twitter:image"):
                allowed.add("content")
            if "style" in attrs:
                allowed.add("style")
            if not allowed:
                return match.group(0)
            tag_text = match.group(0)
            for a_match in list(ATTR_RE.finditer(tag_text))[::-1]:
                name = a_match.group("name").lower()
                if name not in allowed:
                    continue
                value = a_match.group("value")
                new_value = value
                if name == "style":
                    new_value = self.rewrite_css(value, base_url, self.site_dir)
                elif name == "srcset":
                    new_value = self.rewrite_srcset(value, base_url)
                else:
                    local = self.save_resource(value, base_url)
                    if local:
                        new_value = self.rel_path(local)
                if new_value != value:
                    start, end = a_match.span("value")
                    tag_text = tag_text[:start] + new_value + tag_text[end:]
            return tag_text
        html = TAG_RE.sub(tag_repl, html)
        # A base element would cause local relative paths to resolve against the original website.
        html = re.sub(r'<base\b[^>]*>', '', html, flags=re.I)
        return html

    def run(self) -> None:
        print(f"\n[{self.site_dir.name}] Получаю исходную страницу: {self.start_url}")
        try:
            data, content_type, final_url = self.fetch(self.start_url)
        except Exception as exc:
            print(f"ОШИБКА: не удалось получить страницу: {exc}")
            self.errors.append(f"PAGE {self.start_url} — {exc}")
            return
        charset_match = re.search(r"charset=([\w.-]+)", content_type, re.I)
        charset = charset_match.group(1) if charset_match else "utf-8"
        html = data.decode(charset, errors="replace")
        html = self.rewrite_html(html, final_url)
        target = self.site_dir / "index.html"
        target.write_text(html, encoding="utf-8")
        # Record the snapshot source and downloaded resources in each project folder.
        (self.site_dir / "MIRROR_INFO.txt").write_text(
            f"Source: {self.start_url}\nDownloaded date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n" 
            f"Resources downloaded: {self.count}\nFailed requests: {len(self.errors)}\n",
            encoding="utf-8"
        )
        print(f"Готово: {target} | ресурсов: {self.count} | ошибок: {len(self.errors)}")


def main() -> int:
    all_errors: list[str] = []
    for folder, url in SITES:
        mirror = Mirror(ROOT / folder, url)
        mirror.run()
        all_errors.extend(mirror.errors)
    report = ROOT / "clone_report.txt"
    if all_errors:
        report.write_text("Не удалось скачать эти ресурсы:\n" + "\n".join(all_errors) + "\n", encoding="utf-8")
        print(f"\nЕсть ошибки загрузки. Подробности: {report}")
    else:
        report.write_text("All page resources downloaded successfully.\n", encoding="utf-8")
        print("\nВсе страницы и найденные ресурсы сохранены локально.")
    return 0 if not all_errors else 2

if __name__ == "__main__":
    raise SystemExit(main())
