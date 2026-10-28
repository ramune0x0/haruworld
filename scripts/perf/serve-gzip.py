"""
本番 (Cloudflare Pages) に近い条件で計測するための静的サーバー。HTML を gzip -9 で返し、全応答に no-store を付ける。
使い方: python3 scripts/perf/serve-gzip.py <dir> <port>
"""

import gzip
import io
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class GzipHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        if path.suffix != ".html":
            return super().send_head()
        try:
            raw = path.read_bytes()
        except OSError:
            self.send_error(404)
            return None
        body = gzip.compress(raw, 9)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return io.BytesIO(body)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main() -> None:
    directory, port = sys.argv[1], int(sys.argv[2])
    handler = lambda *args: GzipHandler(*args, directory=directory)
    ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    main()
