// Entry program for the news-image-20261122 bounty.
//
// The finished newspaper page ships in this repository as entry.png
// (drawn by draw_news.py with Python's PIL). This program's only job is to
// place an exact copy of those bytes at /output/entry.png, where the
// judges look for it.
//
// It uses no network and no randomness, so every run writes identical
// bytes: the file is read as-is and written as-is.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const bundledImage = join(repoDir, "entry.png");
const outputDir = "/output";
const outputImage = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });

const imageBytes = readFileSync(bundledImage);
writeFileSync(outputImage, imageBytes);

console.log(`wrote ${outputImage} (${imageBytes.length} bytes)`);
