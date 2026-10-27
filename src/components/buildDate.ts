// HUD に出す日付。ビルド時点の日本時間を YYYY.MM.DD で返す
export function formatBuildDateJst(): string {
  return new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Tokyo' }).replaceAll('-', '.');
}
