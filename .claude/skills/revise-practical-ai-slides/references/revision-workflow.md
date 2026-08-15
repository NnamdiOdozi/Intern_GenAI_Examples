# Focused revision workflow

## 1. Locate the correct deck

Search for matching PPTX files and sort by modification time. Exclude PowerPoint lock files beginning with `~$`. Compare filename, time, size, and the user's description. If two candidates are effectively tied, ask the user rather than guessing.

Never regenerate from an earlier JavaScript builder when the user has edited the PowerPoint manually.

## 2. Preserve the source

Create a new output filename that describes the revision. Do not overwrite the source unless the user explicitly requests it. Keep temporary scripts, renders, and inspection output outside the deliverable folder.

## 3. Inspect the target

Import the source PPTX through artifact-tool. Search for exact text and notes, capture stable slide and object IDs, inspect the complete slide, and render a before image. Check whether the user moved the slide, leaving visible manual footer numbers that differ from physical slide positions.

## 4. Apply a focused edit

Edit the resolved objects only. Preserve the source slide geometry and typography where possible. If longer text requires a layout change, adjust the smallest relevant frame and render immediately. Update notes and citations when the claim changes.

Do not rebuild the whole slide simply because recreating it seems easier.

## 5. Export and compare

Export a new PPTX. Render both source and output through the same renderer. Compare every slide pixel-for-pixel. For a one-slide request, every other slide should remain visually identical.

If import/export changes unrelated slides, investigate before delivery. Do not dismiss broad differences as harmless.

## 6. Validate the package

Run overflow tests and package audits. Confirm slide count, notes count, external hyperlinks, source blocks, required new text, and absence of replaced text. Remove generated inspection sidecars from the deliverable folder.

## 7. Report precisely

State the actual slide position changed and distinguish it from any visible footer number. Give the user the revised copy and a concise QA summary.