# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools[woff]>=4.55"]
# ///
"""
見出し用フォント (DotGothic16 / Silkscreen) を、サイトの本文テキストに現れる文字だけに
サブセット化して woff2 を生成する。unicode-range の分割は src/components/FontFaces.astro と一致させること。
"""

import argparse
import hashlib
import sys
import urllib.request
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

from fontTools.subset import main as subset_main
from fontTools.ttLib import TTFont

FONTS_RAW_URL = "https://github.com/google/fonts/raw/main/ofl"
# 初回ダウンロード時に記録した値。上流の差し替えを検知してビルドの再現性を保つ
SOURCES: dict[str, dict[str, str]] = {
    "dotgothic16": {
        "ttf": "DotGothic16-Regular.ttf",
        "ttf_sha256": "3ad9af88726d42b40f7f365f0dcac785af73cf20ea6f1d5b44e57cc21150b8f1",
        "ofl_sha256": "b6630c61ea078cacd7fabe37d14ffe557a0b45b06683374a9aa9e24262993e33",
    },
    "silkscreen": {
        "ttf": "Silkscreen-Regular.ttf",
        "ttf_sha256": "c845473330b94c2079ce9af01c51ac8ba2d99c24f4d14c039843bbb8e642ebd8",
        "ofl_sha256": "86c5e9c9382cdcc5948704fdfe60f2aa164a719746931219a42736ecd9cefbd3",
    },
}
# 本文に現れなくても欠けると困る文字 (英数字・URL 記号・ダッシュ・カーソル・実行時に組み立てる Email の @)
FIXED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789./-—&▶:@"
SKIPPED_TAGS = {"style", "script", "title"}
LATIN_EXTRA = "—▶"
LATIN_MAX_CODEPOINT = 0xFF

# (出力 woff2, 元フォント, 対象面)
OUTPUTS = [
    ("dotgothic16-latin.woff2", "dotgothic16", "latin"),
    ("dotgothic16-jp.woff2", "dotgothic16", "jp"),
    ("silkscreen-latin.woff2", "silkscreen", "latin"),
]


class TextCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIPPED_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIPPED_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth == 0:
            self.chunks.append(data)

    def handle_entityref(self, name: str) -> None:
        self.handle_data(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.handle_data(f"&#{name};")


def is_latin(char: str) -> bool:
    return ord(char) <= LATIN_MAX_CODEPOINT or char in LATIN_EXTRA


def collect_charset(html_dir: Path) -> tuple[str, str]:
    chars: set[str] = set(FIXED_CHARS)
    for html_path in sorted(html_dir.rglob("*.html")):
        collector = TextCollector()
        collector.feed(html_path.read_text(encoding="utf-8"))
        text = unescape("".join(collector.chunks))
        chars.update(c for c in text if not c.isspace() and c.isprintable())
    latin = "".join(sorted(c for c in chars if is_latin(c)))
    jp = "".join(sorted(c for c in chars if not is_latin(c)))
    return latin, jp


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        dest.write_bytes(response.read())


def ensure_source(family: str, cache_dir: Path) -> tuple[Path, Path]:
    spec = SOURCES[family]
    ttf_path = cache_dir / spec["ttf"]
    ofl_path = cache_dir / f"OFL-{family}.txt"
    if not ttf_path.exists():
        download(f"{FONTS_RAW_URL}/{family}/{spec['ttf']}", ttf_path)
    if not ofl_path.exists():
        download(f"{FONTS_RAW_URL}/{family}/OFL.txt", ofl_path)
    for label, path, key in (("TTF", ttf_path, "ttf_sha256"), ("OFL", ofl_path, "ofl_sha256")):
        expected = spec[key]
        actual = sha256_of(path)
        if not expected:
            print(f"{family} {label} sha256: {actual} (SOURCES に記録すること)", file=sys.stderr)
        elif actual != expected:
            sys.exit(f"{path} の sha256 が一致しない: {actual} != {expected}")
    return ttf_path, ofl_path


def charset_of(face: str, latin: str, jp: str) -> str:
    return latin if face == "latin" else jp


def generate(html_dir: Path, out_dir: Path, cache_dir: Path) -> None:
    latin, jp = collect_charset(html_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "charset-latin.txt").write_text(latin + "\n", encoding="utf-8")
    (out_dir / "charset-jp.txt").write_text(jp + "\n", encoding="utf-8")
    for family in SOURCES:
        _, ofl_path = ensure_source(family, cache_dir)
        (out_dir / f"OFL-{family}.txt").write_bytes(ofl_path.read_bytes())
    for output_name, family, face in OUTPUTS:
        ttf_path, _ = ensure_source(family, cache_dir)
        charset_path = out_dir / f"charset-{face}.txt"
        output_path = out_dir / output_name
        subset_main(
            [
                str(ttf_path),
                f"--text-file={charset_path}",
                "--flavor=woff2",
                "--layout-features=*",
                f"--output-file={output_path}",
            ]
        )
        print(f"{output_path}: {output_path.stat().st_size} B")


def check(html_dir: Path, out_dir: Path, cache_dir: Path) -> bool:
    latin, jp = collect_charset(html_dir)
    is_ok = True
    for output_name, family, face in OUTPUTS:
        ttf_path, _ = ensure_source(family, cache_dir)
        source_cmap = set(TTFont(ttf_path).getBestCmap())
        output_path = out_dir / output_name
        if not output_path.exists():
            print(f"{output_path} が無い", file=sys.stderr)
            is_ok = False
            continue
        output_cmap = set(TTFont(output_path).getBestCmap())
        # 元フォントが持たない字はサブセット化でも出せないので除外する
        missing = [c for c in charset_of(face, latin, jp) if ord(c) in source_cmap and ord(c) not in output_cmap]
        if missing:
            print(f"{output_name} に不足: {''.join(missing)}", file=sys.stderr)
            is_ok = False
    return is_ok


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-dir", type=Path, default=Path("dist"))
    parser.add_argument("--out-dir", type=Path, default=Path("src/assets/fonts"))
    parser.add_argument("--source-cache", type=Path, default=Path("node_modules/.cache/font-sources"))
    parser.add_argument("--check", action="store_true", help="生成済み woff2 が dist の文字を網羅しているか検証する")
    args = parser.parse_args()
    if not args.html_dir.is_dir():
        sys.exit(f"{args.html_dir} が無い。先に pnpm build を実行すること")
    if args.check:
        sys.exit(0 if check(args.html_dir, args.out_dir, args.source_cache) else 1)
    generate(args.html_dir, args.out_dir, args.source_cache)


if __name__ == "__main__":
    main()
