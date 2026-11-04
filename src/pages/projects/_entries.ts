// Projects の掲載データ。並び順は index.astro が date の降順で決めるので、追加は順不同でよい。
// サムネイルは src/assets/projects/ に 16:9 前後の PNG を置いて import する。WebP 化と縮小はビルド時に astro:assets が行う。
import type { ImageMetadata } from 'astro';
import cleanroboticsSite from '../../assets/projects/cleanrobotics-site.png';
import galaxySurvival from '../../assets/projects/galaxy-survival.png';

export interface ProjectEntry {
  org: string;
  /** YYYY.MM。文字列の降順比較で新しい順になる */
  date: string;
  title: string;
  description: string;
  tech: string;
  links: { label: string; href: string }[];
  /** 省略時は NO IMAGE YET の既定サムネ */
  thumb?: ImageMetadata;
}

export const projectEntries: ProjectEntry[] = [
  {
    org: '42 Tokyo',
    date: '2026.06',
    title: 'Inception',
    description:
      'Docker で nginx / WordPress / MariaDB を別コンテナに分けた 3 層構成。リバースプロキシ経由の公開だけを許可し、アプリと DB は内部ネットワークに隔離。',
    tech: 'Docker / nginx / MariaDB',
    links: [{ label: 'REPO', href: 'https://github.com/ramune0x0/inception' }],
  },
  {
    org: '42 Tokyo',
    date: '2026.07',
    title: 'ft_irc',
    description:
      'マルチクライアント対応の IRC サーバーを C++ で 2 名で実装。poll で複数接続を管理し、JOIN / KICK / INVITE / PRIVMSG / TOPIC に対応。',
    tech: 'C++ / Linux',
    links: [],
  },
  {
    org: 'Progate 58 ハッカソン',
    date: '2025.09',
    title: 'Galaxy Survival',
    description:
      'Progate 58 ハッカソンで 5 名で制作した 3D オンライン対戦ゲーム。ルーム作成・参加のマッチング処理と UI を担当。最優秀賞・企業賞。',
    tech: 'C# / Unity / Photon Fusion',
    links: [
      { label: 'POST', href: 'https://x.com/_58hack/status/1969732435245224145' },
      { label: 'TOPAZ', href: 'https://topaz.dev/projects/be299aa8d1619240c394' },
    ],
    thumb: galaxySurvival,
  },
  {
    org: 'CleanRobotics',
    date: '2026.02',
    title: 'コーポレートサイト',
    description:
      '受託でフロントエンドを設計・実装して納品。スクロール連動アニメーションなどの動的 UI とロゴ制作を担当。',
    tech: 'Next.js / React / Figma',
    links: [{ label: 'SITE', href: 'https://cleanrobotics.jp/' }],
    thumb: cleanroboticsSite,
  },
];
