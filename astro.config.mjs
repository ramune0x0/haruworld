// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://haruworld.nymphaea.dev',
  output: 'static',
  build: { inlineStylesheets: 'always' },
  // 旧 URL の救済。ホスティング固有の _redirects ではなく Astro に持たせ、配信先を変えても同じ挙動にする (静的ビルドでは meta refresh ページになる)
  redirects: { '/works': '/projects/' },
});
