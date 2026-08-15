#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

function argsOf(argv) {
  const result = {};
  for (let i = 2; i < argv.length; i++) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
    result[key.slice(2)] = value;
  }
  return result;
}

const args = argsOf(process.argv);
if (!args.pptx) {
  console.error("Usage: node inspect_deck.mjs --pptx deck.pptx [--search text] [--slide N] [--out-dir dir]");
  process.exit(2);
}
const requireFromWorkspace = createRequire(path.join(process.cwd(), "package.json"));
const artifactEntry = requireFromWorkspace.resolve("@oai/artifact-tool");
const { FileBlob, PresentationFile } = await import(pathToFileURL(artifactEntry).href);
const deck = await PresentationFile.importPptx(await FileBlob.load(path.resolve(args.pptx)));
const snapshot = await deck.inspect({
  kind: "slide,textbox,shape,image,table,chart,notes,layout",
  ...(args.search ? { search: String(args.search) } : {}),
  maxChars: 30000,
});
console.log(snapshot.ndjson);
if (args["out-dir"]) {
  const out = path.resolve(args["out-dir"]);
  await fs.mkdir(out, { recursive: true });
  await fs.writeFile(path.join(out, "inspect.ndjson"), snapshot.ndjson, "utf8");
  if (args.slide) {
    const number = Number(args.slide);
    if (!Number.isInteger(number) || number < 1 || number > deck.slides.items.length) {
      throw new Error(`Invalid slide number: ${args.slide}`);
    }
    const slide = deck.slides.getItem(number - 1);
    const preview = await deck.export({ slide, format: "png", scale: 1 });
    await fs.writeFile(path.join(out, `slide-${number}.png`), new Uint8Array(await preview.arrayBuffer()));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(out, `slide-${number}.layout.json`), await layout.text(), "utf8");
  }
}