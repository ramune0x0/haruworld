// HUD に出す日付。ビルド時点の日本時間を YYYY.MM.DD で返す
// sv-SE はロケールの中で唯一 ISO 8601 (YYYY-MM-DD) を出すので、区切りを置換するだけで済む
export function formatBuildDateJst(): string {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Tokyo' }).replaceAll('-', '.');
}
