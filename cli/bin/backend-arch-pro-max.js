#!/usr/bin/env node
"use strict";
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");
 
const CLI_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(__dirname, "..", "..");
const ASSET_ROOT = path.join(CLI_ROOT, "assets", "skill");
const REPO_TEMPLATE_SOURCE = path.join(REPO_ROOT, "templates", "platforms", "source.json");
 
// Detect if we are running from source repo or from installed npm package
const IS_REPO = fs.existsSync(REPO_TEMPLATE_SOURCE);
const SOURCE_ROOT = IS_REPO ? REPO_ROOT : ASSET_ROOT;
const TEMPLATE_DIR = path.join(SOURCE_ROOT, "templates", "platforms");
const COPY_ENTRIES = ["SKILL.md", "skill.json", "agents", "docs", "scripts", "src", "templates", "examples/use-cases"];
 
function usage() {
  console.log(`
Backend Arch Pro Max CLI
 
Usage:
  backend-arch-pro-max init [--ai <platform>] [--target <dir>] [--force]
  backend-arch-pro-max search <query> [options]
  backend-arch-pro-max list
  backend-arch-pro-max help
 
Options:
  --ai <platform>   Platform: codex, claude, cursor, windsurf, antigravity (auto-detected if omitted)
  --target <dir>    Target directory (default: current)
  --force           Overwrite existing installation
 
Search Options (passed to python engine):
  --architecture, -a  Generate architecture recommendation
  --domain, -d        Filter by domain (logic, integration, infrastructure, etc.)
  --stack, -s         Filter by technology stack
  --persist           Save output to WORKFLOW.md
  --json              Output in JSON format
 
Examples:
  backend-arch-pro-max init
  backend-arch-pro-max search "microservices event-driven" --architecture
  backend-arch-pro-max search "nestjs auth" --stack nextjs
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
    if (["force", "help", "architecture", "persist", "json"].includes(key)) {
      args[key] = true;
    } else {
      args[key] = argv[index + 1];
      index += 1;
    }
  }
  return args;
}
 
function detectPlatform(targetRoot) {
  if (fs.existsSync(path.join(targetRoot, ".cursor"))) return "cursor";
  if (fs.existsSync(path.join(targetRoot, ".claude"))) return "claude";
  if (fs.existsSync(path.join(targetRoot, ".windsurf"))) return "windsurf";
  if (fs.existsSync(path.join(targetRoot, ".codex"))) return "codex";
  return "antigravity";
}
 
function loadPlatform(name) {
  const file = path.join(TEMPLATE_DIR, `${name}.json`);
  if (!fs.existsSync(file)) {
    throw new Error(`Unknown platform "${name}". Run "backend-arch-pro-max list".`);
  }
  return JSON.parse(fs.readFileSync(file, "utf8"));
}
 
function listPlatforms() {
  const files = fs.readdirSync(TEMPLATE_DIR).filter((file) => file.endsWith(".json") && file !== "source.json");
  console.log("Available AI Platforms:");
  for (const file of files) {
    const platform = JSON.parse(fs.readFileSync(path.join(TEMPLATE_DIR, file), "utf8"));
    if (platform.platform && platform.displayName) {
      console.log(`  ${platform.platform.padEnd(15)} ${platform.displayName}`);
    }
  }
}
 
function install(args) {
  const targetRoot = path.resolve(args.target || process.cwd());
  const platformName = args.ai || args.platform || detectPlatform(targetRoot);
  const platform = loadPlatform(platformName);
  
  const destinationRoot = path.join(
    targetRoot, 
    platform.folderStructure.root, 
    platform.folderStructure.skillPath.replace(/^skills[\\/]/, "skills/")
  );
 
  if (fs.existsSync(destinationRoot) && !args.force) {
    throw new Error(`Destination already exists: ${destinationRoot}. Use --force to overwrite.`);
  }
 
  console.log(`Platform detected: ${platform.displayName}`);
  console.log(`Target path:       ${destinationRoot}`);
 
  fs.mkdirSync(destinationRoot, { recursive: true });
  for (const entry of COPY_ENTRIES) {
    const source = path.join(SOURCE_ROOT, entry);
    if (!fs.existsSync(source)) continue;
    const destination = path.join(destinationRoot, entry);
    fs.cpSync(source, destination, { recursive: true });
  }
 
  // Add npm script if package.json exists
  const pkgPath = path.join(targetRoot, "package.json");
  if (fs.existsSync(pkgPath)) {
    try {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
      pkg.scripts = pkg.scripts || {};
      if (!pkg.scripts.arch) {
        pkg.scripts.arch = "backend-arch-pro-max search --architecture";
        fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2), "utf8");
        console.log("Updated package.json with 'arch' script.");
      }
    } catch (e) {
      console.warn("Could not update package.json scripts.");
    }
  }
 
  console.log("\nInstall complete! You can now use:");
  console.log("  npx backend-arch-pro-max search \"your query\"");
  if (fs.existsSync(pkgPath)) console.log("  npm run arch -- \"your query\"");
}
 
function search(argv) {
  const pythonPath = process.platform === "win32" ? "python" : "python3";
  const scriptPath = path.join(SOURCE_ROOT, "scripts", "search.py");
  
  const result = spawnSync(pythonPath, [scriptPath, ...argv], { stdio: "inherit" });
  if (result.error) {
    if (result.error.code === "ENOENT") {
      console.error("Error: Python not found. Please install Python to use the search engine.");
    } else {
      console.error(`Error executing search: ${result.error.message}`);
    }
    process.exit(1);
  }
}
 
function main() {
  const argv = process.argv.slice(2);
  const args = parseArgs(argv);
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
    if (command === "search") {
      search(argv.slice(1));
      return;
    }
    
    // Default: try search if no command matches
    search(argv);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exitCode = 1;
  }
}
 
main();
