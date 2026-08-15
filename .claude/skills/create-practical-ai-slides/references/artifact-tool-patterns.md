# Artifact-tool patterns

Use these only after reading the active presentations skill and its required API references. Create deck-specific code in the task's temporary presentation workspace rather than editing this reference.

## Imports

```javascript
import fs from "node:fs/promises";
import path from "node:path";
import {
  FileBlob,
  Presentation,
  PresentationFile,
} from "@oai/artifact-tool";
```

## Create a presentation

```javascript
const deck = Presentation.create({
  slideSize: { width: 1280, height: 720 },
});
const slide = deck.slides.add();
slide.background.fill = "#FFFFFF";
```

## Import an existing presentation

```javascript
const deck = await PresentationFile.importPptx(
  await FileBlob.load(sourcePptx),
);
const hits = await deck.inspect({
  kind: "slide,textbox,shape,image,table,chart,notes,layout",
  search: "target phrase",
  maxChars: 12000,
});
console.log(hits.ndjson);
```

Resolve exact inspection IDs before making a focused edit:

```javascript
const target = deck.resolve("sh/exact-id-from-inspect");
target.text.replace("old text", "new text");
```

Never guess IDs or rebuild an existing manually edited deck from an older generator.

## Hyperlinks

```javascript
const linkShape = slide.shapes.add({
  geometry: "textbox",
  position: { left: 72, top: 620, width: 700, height: 28 },
  fill: "none",
  line: { style: "solid", fill: "none", width: 0 },
});
linkShape.text = "Readable resource title";
linkShape.text.get("Readable resource title").link = {
  uri: "https://example.com/resource",
  isExternal: true,
};
```

## Speaker notes

```javascript
slide.speakerNotes.textFrame.setText([
  "Presenter guidance.",
  "",
  "[Sources]",
  "- Source title - https://example.com/source",
  "[/Sources]",
].join("\n"));
slide.speakerNotes.setVisible(true);
```

## Render and export

```javascript
const png = await deck.export({ slide, format: "png", scale: 1 });
await fs.writeFile(previewPath, new Uint8Array(await png.arrayBuffer()));

const layout = await slide.export({ format: "layout" });
await fs.writeFile(layoutPath, await layout.text());

const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(finalPptx);
```

Render the exported PPTX again with the presentations skill's renderer. An artifact preview alone is not final QA.