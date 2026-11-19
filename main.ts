// gta6-meme-x-01 entry (Node 22, standard library only).
//
// Contract: this program does exactly one thing — it copies POST.json from
// the repository root to /output/POST.json, where the gate reads it. The
// entry IS the X post itself, not this code: the post must be public, from
// an account kept public until the results are out, and its text must carry
// the make.fun bounty link and/or an @makefunai tag AND the play code the
// competition issued. POST.json names that post by its status URL, and the
// house fetches the post from X (its first picture and its text) and hands
// it to the judge. Nothing this program prints about the post is judged.
//
// A placeholder URL in POST.json is refused by the gate, so the file must
// hold the real status address before you submit.
//
// Local test (MAKEFUN_BOT_DIR / MAKEFUN_OUTPUT_DIR stand in for /bot and
// /output outside the grader's container):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Fail fast on a placeholder or malformed POST.json instead of letting the
// gate refuse the entry later: the url must be a real public X status URL,
// https://x.com/<handle>/status/<digits>. This only reads the file; the
// copy below is still the whole job.
const postPath = join(BOT_DIR, 'POST.json');
const postUrl = (JSON.parse(readFileSync(postPath, 'utf8')) as { url?: unknown }).url;
if (typeof postUrl !== 'string' || !/^https:\/\/x\.com\/[^/]+\/status\/\d+$/.test(postUrl)) {
  console.error(
    `POST.json must hold a real post address like https://x.com/<handle>/status/<id>, got: ${String(postUrl)}`,
  );
  process.exit(1);
}
console.log(`Submitting post: ${postUrl}`);

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
} catch (err) {
  console.error(`POST.json could not be copied from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}
