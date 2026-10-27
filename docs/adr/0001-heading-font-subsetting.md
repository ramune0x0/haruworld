# ADR 0001: 見出しフォントのサブセット生成方式

## 状況

見出し用の DotGothic16 / Silkscreen を、外部 CDN に頼らずセルフホストしたい。
フォント全体は大きく、トップは「1 リクエスト」を保つため、使う文字だけに絞った woff2 を生成し、トップには data URI で埋め込む必要がある。

## 比較

| 軸 | (a) Astro `fonts` (local) | (b) fonttools + 手書き @font-face | (c) 併用 (生成 b、配信 a) |
|---|---|---|---|
| グリフのサブセット化 | 不可。別途 b が必要 | 可 | 可 (b 由来) |
| トップへの data URI 埋め込み | 不可 | 可 | トップだけ手書きになり二重管理 |
| 自前で持つコード量 | config + 生成スクリプト | スクリプト + @font-face 3 行の component | a + b |
| AI 習熟度 / API 安定性 | Astro 6 で stable だが事例が少ない | fonttools は十年以上の定番で CLI が安定 | 両方 |
| 機械検証のしやすさ | グリフ網羅は検証不能 | `--check` で woff2 の cmap が dist の文字を網羅するか検証できる | b と同じ |

## 決定

(b) を採用する。
Astro `fonts` のローカルプロバイダはサブセット化をしないため、採用しても生成スクリプトと手書き @font-face は残る。

## 影響

- unicode-range の分割を `scripts/subset-fonts.py` と `src/components/FontFaces.astro` の 2 箇所で持つ。双方に相互参照コメントを置く
- 文言を変えたら `pnpm build` → `pnpm fonts` → `pnpm build` で再生成する。`pnpm fonts:check` で不足を検出できる
- 元フォントは Google Fonts リポジトリから取得し、sha256 をスクリプトに固定する。ライセンス (OFL) は `src/assets/fonts/` に同梱する
