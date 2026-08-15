# Artifact-tool edit patterns

Read the active presentations skill and its imported-deck references before using these patterns.

```javascript
import fs from "node:fs/promises";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const deck = await PresentationFile.importPptx(
  await FileBlob.load(sourcePptx),
);
```

Search narrowly before editing:

```javascript
const hits = await deck.inspect({
  kind: "slide,textbox,shape,image,table,chart,notes,layout",
  search: "exact old phrase",
  maxChars: 16000,
});
console.log(hits.ndjson);
```

Resolve IDs copied from inspection:

```javascript
const slide = deck.resolve("sl/exact-slide-id");
const target = deck.resolve("sh/exact-shape-id");
target.text.replace("exact old phrase", "replacement phrase");
```

Update notes through the resolved notes object while preserving required sources:

```javascript
const notes = deck.resolve("nt/exact-notes-id");
notes.setText([
  "Updated presenter guidance.",
  "",
  "[Sources]",
  "- Source title - https://example.com/source",
  "[/Sources]",
].join("\n"));
notes.setVisible(true);
```

Render the affected slide before export, then export a new copy:

```javascript
const preview = await deck.export({ slide, format: "png", scale: 1 });
await fs.writeFile(afterPreview, new Uint8Array(await preview.arrayBuffer()));

const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(outputPptx);
```

Render the exported source and output decks with the same PowerPoint renderer and compare every slide. Artifact previews alone are insufficient.