import { constants } from "node:fs";
import {
  access,
  copyFile,
  mkdir,
  readFile,
  rename,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const projectDirectory = path.resolve(scriptDirectory, "..");
const configPath = path.join(projectDirectory, ".content-source");
const destinationPath = path.join(
  projectDirectory,
  "docs",
  "handwritten-code",
  "attention-blocks.md",
);

async function configuredSource() {
  const argument = process.argv[2]?.trim();
  if (argument) {
    return {
      path: path.resolve(process.cwd(), argument),
      remember: true,
    };
  }

  const environmentPath = process.env.CONTENT_SOURCE?.trim();
  if (environmentPath) {
    return {
      path: path.resolve(process.cwd(), environmentPath),
      remember: false,
    };
  }

  try {
    const savedPath = (await readFile(configPath, "utf8")).trim();
    if (savedPath) return { path: savedPath, remember: false };
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }

  throw new Error(
    "No source is configured. Run: npm run sync:content -- /absolute/path/to/article.md",
  );
}

async function filesMatch(firstPath, secondPath) {
  try {
    const [first, second] = await Promise.all([
      readFile(firstPath),
      readFile(secondPath),
    ]);
    return first.equals(second);
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

async function syncContent() {
  const source = await configuredSource();
  const sourcePath = source.path;
  await access(sourcePath, constants.R_OK);

  const sourceStats = await stat(sourcePath);
  if (!sourceStats.isFile()) {
    throw new Error(`Content source is not a file: ${sourcePath}`);
  }

  if (path.resolve(sourcePath) === path.resolve(destinationPath)) {
    throw new Error("The external source and repository destination are the same file.");
  }

  if (source.remember) {
    await writeFile(configPath, `${sourcePath}\n`, "utf8");
  }

  if (await filesMatch(sourcePath, destinationPath)) {
    console.log(`Content is already current:\n${destinationPath}`);
    return;
  }

  await mkdir(path.dirname(destinationPath), { recursive: true });
  const temporaryPath = `${destinationPath}.tmp-${process.pid}`;

  try {
    await copyFile(sourcePath, temporaryPath);
    await rename(temporaryPath, destinationPath);
  } finally {
    await rm(temporaryPath, { force: true });
  }

  console.log(`Updated content from:\n${sourcePath}\n\nRepository copy:\n${destinationPath}`);
}

syncContent().catch((error) => {
  console.error(`Content sync failed: ${error.message}`);
  process.exitCode = 1;
});
