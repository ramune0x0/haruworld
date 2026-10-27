// キャッシュ無しの初回読み込みを 3 回計測して中央値を出す。毎回新しいコンテキスト (空キャッシュ) で開き、CDP で回線を絞る。
// favicon は計測対象から除外する。
// 使い方: node scripts/perf/measure-cold.mjs <url> <label> [latencyMs] [downMbps]
import { chromium } from 'playwright-core';

const [url, label, latencyMs = '0', downMbps = '0'] = process.argv.slice(2);
const browser = await chromium.launch({ channel: 'chrome' });
const runs = [];
for (let i = 0; i < 3; i++) {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  if (+latencyMs > 0 || +downMbps > 0) {
    await cdp.send('Network.emulateNetworkConditions', {
      offline: false, latency: +latencyMs,
      downloadThroughput: +downMbps > 0 ? (+downMbps * 1024 * 1024) / 8 : -1,
      uploadThroughput: +downMbps > 0 ? (+downMbps * 1024 * 1024) / 16 : -1,
    });
  }
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  const m = await page.evaluate(() => {
    const nav = performance.getEntriesByType('navigation')[0];
    const paints = Object.fromEntries(performance.getEntriesByType('paint').map((p) => [p.name, Math.round(p.startTime)]));
    const res = performance.getEntriesByType('resource').filter((r) => !/\/favicon\./.test(r.name));
    const bytes = res.reduce((a, r) => a + (r.transferSize || 0), 0) + (nav.transferSize || 0);
    const fontsReady = document.fonts.status;
    return {
      requests: res.length + 1,
      kb: Math.round(bytes / 1024),
      ttfb: Math.round(nav.responseStart),
      fp: paints['first-paint'] ?? null,
      fcp: paints['first-contentful-paint'] ?? null,
      dcl: Math.round(nav.domContentLoadedEventEnd),
      load: Math.round(nav.loadEventEnd),
      fontsReady,
    };
  });
  runs.push(m);
  await ctx.close();
}
await browser.close();
const med = (k) => { const v = runs.map((r) => r[k]).filter((x) => x !== null).sort((a, b) => a - b); return v[Math.floor(v.length / 2)]; };
console.log(JSON.stringify({ label, url, latencyMs: +latencyMs, downMbps: +downMbps, requests: med('requests'), kb: med('kb'), ttfb: med('ttfb'), fp: med('fp'), fcp: med('fcp'), dcl: med('dcl'), load: med('load'), runs }));
