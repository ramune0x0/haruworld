# Haruworld

ポートフォリオサイト [haruworld.nymphaea.dev](https://haruworld.nymphaea.dev)

## Tech Stack

- [Astro](https://astro.build/) - 静的サイトジェネレーター
- Vanilla CSS (グローバル CSS + CSS Variables。ビルド時に各ページへ inline)
- Cloudflare Pages (Hosting)

## Fonts

見出しだけセルフホストし、本文は OS のフォントを使う。

- [DotGothic16](https://fonts.google.com/specimen/DotGothic16) - 日本語・英数字の見出し
- [Silkscreen](https://fonts.google.com/specimen/Silkscreen) - HUD の英字ラベル

サイトに現れる文字だけにサブセット化した woff2 を `src/assets/fonts/` に置く。文言を変えたら `pnpm build` → `pnpm fonts` → `pnpm build` で再生成する。
経緯は [ADR 0001](docs/adr/0001-heading-font-subsetting.md)。

## Commands

| Command | Action |
|:--|:--|
| `pnpm install` | 依存関係のインストール |
| `pnpm dev` | 開発サーバー起動 (`localhost:4321`) |
| `pnpm build` | 本番ビルド (`./dist/`) |
| `pnpm preview` | ビルド結果のプレビュー |
| `pnpm fonts` | `dist/` の文字から見出しフォントを再生成 (要 uv) |
| `pnpm fonts:check` | 生成済みフォントが `dist/` の文字を網羅しているか検証 |
