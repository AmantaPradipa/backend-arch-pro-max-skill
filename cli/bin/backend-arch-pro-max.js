#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const CLI_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const ASSET_ROOT = path.join(CLI_ROOT, "assets", "skill");
const REPO_TEMPLATE_SOURCE = path.join(REPO_ROOT, "templates", "platforms", "source.json");
const SOURCE_ROOT = fs.existsSync(REPO_TEMPLATE_SOURCE)
  ? REPO_ROOT
  : fs.existsSync(path.join(ASSET_ROOT, "SKILL.md"))
    ? ASSET_ROOT
    : REPO_ROOT;
const TEMPLATE_DIR = path.join(SOURCE_ROOT, "templates", "platforms");

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

function usage() {
  console.log(`Backend Arch Pro Max CLI

Usage:
  backend-arch-pro-max init --ai <platform> [--target <dir>] [--dry-run] [--force]
  backend-arch-pro-max list

Examples:
  backend-arch-pro-max list
  backend-arch-pro-max init --ai codex --target .
  backend-arch-pro-max init --ai claude --target D:\\work\\my-project --dry-run

Platforms are loaded from templates/platforms/*.json.
`);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    if (key === "dry-run" || key === "force" || key === "help") {
      args[key] = true;
    } else {
      args[key] = argv[index + 1];
      index += 1;
    }
  }
  return args;
}

function loadPlatform(name) {
  const file = path.join(TEMPLATE_DIR, `${name}.json`);
  if (!fs.existsSync(file)) {
    throw new Error(`Unknown platform "${name}". Run "backend-arch-pro-max list".`);
  }
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function listPlatforms() {
  const files = fs
    .readdirSync(TEMPLATE_DIR)
    .filter((file) => file.endsWith(".json") && file !== "source.json");
  for (const file of files) {
    const platform = JSON.parse(fs.readFileSync(path.join(TEMPLATE_DIR, file), "utf8"));
    if (!platform.platform || !platform.displayName) {
      continue;
    }
    console.log(`${platform.platform.padEnd(10)} ${platform.displayName}`);
  }
}

function ensureInsideTarget(targetRoot, destination) {
  const relative = path.relative(targetRoot, destination);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`Refusing to install outside target directory: ${destination}`);
  }
}

function copyEntry(entry, destinationRoot, dryRun) {
  const source = path.join(SOURCE_ROOT, entry);
  if (!fs.existsSync(source)) {
    return;
  }
  const destination = path.join(destinationRoot, entry);
  if (dryRun) {
    console.log(`[dry-run] copy ${entry} -> ${destination}`);
    return;
  }
  fs.cpSync(source, destination, { recursive: true });
}

function install(args) {
  const platformName = args.ai || args.platform;
  if (!platformName) {
    throw new Error("Missing --ai <platform>.");
  }

  const platform = loadPlatform(platformName);
  const targetRoot = path.resolve(args.target || process.cwd());
  const skillPath = platform.folderStructure.skillPath;
  const destinationRoot = path.join(targetRoot, platform.folderStructure.root, skillPath.replace(/^skills[\\/]/, "skills/"));

  ensureInsideTarget(targetRoot, destinationRoot);

  if (fs.existsSync(destinationRoot) && !args.force && !args["dry-run"]) {
    throw new Error(`Destination already exists: ${destinationRoot}. Use --force to overwrite.`);
  }

  console.log(`Platform: ${platform.displayName}`);
  console.log(`Target:   ${targetRoot}`);
  console.log(`Install:  ${destinationRoot}`);

  if (!args["dry-run"]) {
    fs.mkdirSync(destinationRoot, { recursive: true });
  }

  for (const entry of COPY_ENTRIES) {
    copyEntry(entry, destinationRoot, Boolean(args["dry-run"]));
  }

  console.log(args["dry-run"] ? "Dry run complete." : "Install complete.");
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  try {
    if (!command || args.help || command === "help") {
      usage();
      return;
    }
    if (command === "list") {
      listPlatforms();
      return;
    }
    if (command === "init" || command === "install") {
      install(args);
      return;
    }
    throw new Error(`Unknown command: ${command}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exitCode = 1;
  }
}

main();
