#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const CLI_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const OUT_ROOT = path.join(CLI_ROOT, "assets", "skill");

const COPY_ENTRIES = [
  "SKILL.md",
  "skill.json",
  "agents",
  "docs",
  "scripts",
  "src",
  "templates",
  "examples/use-cases"
];

function ensurePathInside(root, target) {
  const relative = path.relative(root, target);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`Refusing to write outside output root: ${target}`);
  }
}

function copyEntry(entry) {
  const source = path.join(REPO_ROOT, entry);
  if (!fs.existsSync(source)) {
    return;
  }

  const destination = path.join(OUT_ROOT, entry);
  ensurePathInside(OUT_ROOT, destination);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.cpSync(source, destination, { recursive: true });
}

function main() {
  fs.rmSync(OUT_ROOT, { recursive: true, force: true });
  fs.mkdirSync(OUT_ROOT, { recursive: true });

  for (const entry of COPY_ENTRIES) {
    copyEntry(entry);
  }

  console.log(`Prepared npm assets in ${OUT_ROOT}`);
}

main();
