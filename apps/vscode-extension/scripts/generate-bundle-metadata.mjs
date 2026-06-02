#!/usr/bin/env node
/**
 * Writes bundle-metadata.json for GitHub Releases (invoked from release-binaries CI).
 * Usage: node generate-bundle-metadata.mjs <version> [output-path]
 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const version = process.argv[2];
if (!version) {
  console.error("usage: node generate-bundle-metadata.mjs <version> [output-path]");
  process.exit(1);
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const assetMap = JSON.parse(readFileSync(join(scriptDir, "asset-map.json"), "utf8"));
const outputPath = process.argv[3] || join(scriptDir, "..", "resources", "bundle-metadata.json");

const payload = {
  version,
  repository: "Abhigyan-Shekhar/Waggle-mcp",
  assets: assetMap
};

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
console.log(`wrote ${outputPath}`);
