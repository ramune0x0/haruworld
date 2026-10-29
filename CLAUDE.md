# haruworld

nymphaea.dev のポートフォリオサイト。ゲームのタイトル画面・セーブデータ画面をモチーフにした 5 ページ構成。

## 技術スタック

- **フレームワーク**: Astro 6.x (静的サイト)
- **スタイル**: Vanilla CSS (`src/styles/` のグローバル CSS を各ページに inline。Astro のスコープド CSS は使わない)
- **フォント**: DotGothic16 / Silkscreen のサブセットをセルフホスト (`src/assets/fonts/`)。本文は OS フォント
- **ホスティング**: Vercel (GitHub 連携で main を自動デプロイ)。ドメインと DNS は Cloudflare
- **パッケージマネージャ**: pnpm / Python スクリプトは uv

## コマンド

```bash
pnpm dev          # 開発サーバー起動 (http://localhost:4321)
pnpm build        # 本番ビルド (dist/ に出力)
pnpm preview      # ビルド結果のプレビュー
pnpm fonts        # dist/ の文字から見出しフォントを再生成
pnpm fonts:check  # フォントが dist/ の文字を網羅しているか検証
```

## ディレクトリ構成

```
src/
├── assets/fonts/ # サブセット済み woff2 (scripts/subset-fonts.py の生成物。手で編集しない)
├── components/   # FontFaces, TopBar, Screen (.astro)
├── layouts/      # 共通レイアウト (Layout.astro)
├── pages/        # index, about, projects, skills, contact
└── styles/       # global.css (共通) / title.css (トップ) / screen.css (画面 4 ページ)
scripts/          # フォント生成 (subset-fonts.py) / 速度計測 (perf/)
```

## 守ること

- 実行時 JS を足さない。例外は Contact の Email 組み立て (inline script) のみ
- 外部オリジンへのリクエストを足さない
- 文言を変えたら push 前に `pnpm build` → `pnpm fonts` → `pnpm build` → `pnpm fonts:check`

## デザイン

- カラー: 紫 `#674D9E` + 蛍光黄緑 `#ACFF09` on ダーク `#0a0a0f`
- フォント: DotGothic16 (見出し) / Silkscreen (HUD ラベル)
