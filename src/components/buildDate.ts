// HUD に出す日付。ビルド時点の日本時間を YYYY.MM.DD で返す
// sv-SE は toLocaleDateString が YYYY-MM-DD を返すので、区切りの置換だけで済む
export function formatBuildDateJst(): string {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Tokyo' }).replaceAll('-', '.');
}
