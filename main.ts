// main.ts — entrypoint for news-image-20261125-v3.
// Verifies the rendered front page and copies it to output/.
// Run: node main.ts   (after: python3 draw_news25_v3.py)
import { readFileSync, existsSync, mkdirSync, copyFileSync, statSync } from "node:fs";
import { join } from "node:path";

const ROOT = process.cwd();
const ENTRY = join(ROOT, "entry.png");
const DEBUG = join(ROOT, "pin_debug.txt");

function fail(message: string): never {
  console.error(`ENTRYPOINT FAIL: ${message}`);
  process.exit(1);
}

if (!existsSync(ENTRY)) {
  fail("entry.png is missing — run python3 draw_news25_v3.py first");
}
if (!existsSync(DEBUG)) {
  fail("pin_debug.txt is missing — run python3 draw_news25_v3.py first");
}

const bytes = readFileSync(ENTRY);
if (bytes.length < 8 || bytes[0] !== 0x89 || bytes[1] !== 0x50) {
  fail("entry.png is not a PNG file");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`entry.png is ${width}x${height}, expected 1024x1024`);
}

const debug = readFileSync(DEBUG, "utf8");
const landLines = debug.split("\n").filter((l) => l.includes("| True"));
if (landLines.length !== 13) {
  fail(`pin debug shows ${landLines.length}/13 pins on land`);
}
if (!debug.includes("total stories: 38")) {
  fail("pin debug does not confirm 38 stories");
}
if (!debug.includes("last also: 38")) {
  fail("pin debug does not confirm last ALSO number 38");
}
// Re-add the region counts from the debug line and demand the same total.
const regionMatch = debug.match(/regions: \{([^}]*)\}/);
if (!regionMatch) {
  fail("pin debug does not carry region counts");
}
const regionSum = regionMatch[1]
  .split(",")
  .map((part) => Number(part.split(":")[1]))
  .reduce((a, b) => a + b, 0);
if (regionSum !== 38) {
  fail(`region counts add to ${regionSum}, expected 38`);
}
const regionMax = Math.max(
  ...regionMatch[1].split(",").map((part) => Number(part.split(":")[1])),
);
if (regionMax > 7) {
  fail(`a region tops 7 stories (max ${regionMax})`);
}

mkdirSync(join(ROOT, "output"), { recursive: true });
copyFileSync(ENTRY, join(ROOT, "output", "entry.png"));
const outSize = statSync(join(ROOT, "output", "entry.png")).size;

console.log(`ENTRYPOINT OK: entry.png ${width}x${height}, ${bytes.length} bytes`);
console.log(`Pins on land: 13/13, stories: 38, regions add to 38`);
console.log(`Copied to output/entry.png (${outSize} bytes)`);
