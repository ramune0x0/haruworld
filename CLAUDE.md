# haruworld

nymphaea.dev のポートフォリオサイト。

## 技術スタック

- **フレームワーク**: Astro 5.x (静的サイト)
- **スタイル**: Vanilla CSS (Astro スコープド CSS + CSS 変数)
- **アイコン**: astro-icon + Iconify (simple-icons, mdi)
- **ホスティング**: Cloudflare Pages
- **パッケージマネージャ**: pnpm

## コマンド

```bash
pnpm dev      # 開発サーバー起動 (http://localhost:4321)
pnpm build    # 本番ビルド (dist/ に出力)
pnpm preview  # ビルド結果のプレビュー
```

## ディレクトリ構成

```
src/
├── components/   # セクション別コンポーネント (.astro)
├── layouts/      # 共通レイアウト (Layout.astro)
├── pages/        # ルーティング (index.astro)
└── styles/       # グローバル CSS (変数・リセット)
```

## デザイン

- カラー: 紫 `#674D9E` + 蛍光黄緑 `#ACFF09` on ダーク `#0a0a0f`
- フォント: Zen Kaku Gothic New (見出し) / Noto Sans JP (本文)
