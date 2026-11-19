// gta6-meme-x-01 — entrypoint, rewritten by the build agent for this entry.
//
// The whole job of this program is a single hand-off: the repository root
// holds POST.json, a tiny file naming the X post where Dani published the
// meme, and the grader expects to find that same file inside the output
// directory. So I read the bytes in and write them back out, untouched —
// parsing and re-serialising could only risk changing them.
//
// Where the two directories are comes from the environment when the
// grader's container layout is being mimicked locally:
//   MAKEFUN_BOT_DIR    where POST.json is read from   (default: /bot)
//   MAKEFUN_OUTPUT_DIR where POST.json is delivered  (default: /output)
// Success is silent and exits 0; if POST.json cannot be read (or the copy
// cannot be written) the program reports it on stderr and exits 1.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

function envDir(name: string, fallback: string): string {
  const value = process.env[name];
  return value === undefined || value === "" ? fallback : value;
}

function deliverPost(): number {
  const fromDir = envDir("MAKEFUN_BOT_DIR", "/bot");
  const toDir = envDir("MAKEFUN_OUTPUT_DIR", "/output");
  const sourcePath = join(fromDir, "POST.json");
  const targetPath = join(toDir, "POST.json");

  let payload: Buffer;
  try {
    payload = readFileSync(sourcePath);
  } catch {
    console.error(`deliverPost: no readable POST.json at ${sourcePath}`);
    return 1;
  }

  try {
    mkdirSync(toDir, { recursive: true });
    writeFileSync(targetPath, payload);
  } catch {
    console.error(`deliverPost: could not write ${targetPath}`);
    return 1;
  }

  return 0;
}

process.exit(deliverPost());
