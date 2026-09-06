"""Inspect the installed LlamaCloud workflow methods without making API calls."""

from __future__ import annotations

import datetime
import importlib.metadata
import inspect
import io
import pydoc
from pathlib import Path

from llama_cloud import LlamaCloud


TOPIC = "workflow_methods"
METHODS = (
    "files.create",
    "parsing.parse",
    "extract.validate_schema",
    "extract.run",
    "beta.directories.create",
    "beta.directories.files.add",
    "beta.indexes.list",
    "beta.indexes.create",
    "beta.indexes.get",
    "beta.retrieval.retrieve",
)


def resolve_attribute(root: object, dotted: str) -> object:
    """Resolve a dotted attribute path from an object."""
    value = root
    for part in dotted.split("."):
        value = getattr(value, part)
    return value


version = importlib.metadata.version("llama-cloud")
client = LlamaCloud(api_key="inspection-only-placeholder")
output = io.StringIO()
output.write(f"# {TOPIC}\n\n")
output.write(f"Source: inspect: llama_cloud.LlamaCloud methods @ {version}\n")
output.write(f"Probed: {datetime.date.today():%Y-%m-%d}\n\n")

for method_path in METHODS:
    output.write(f"## {method_path}\n\n")
    try:
        method = resolve_attribute(client, method_path)
    except AttributeError as error:
        output.write(f"Missing: {error}\n\n")
        continue
    output.write(f"### Signature\n\n```\n{inspect.signature(method)}\n```\n\n")
    output.write("### help()\n\n```\n")
    output.write(pydoc.render_doc(method, renderer=pydoc.plaintext))
    output.write("\n```\n\n")

output.write(
    "## Usage (agent synthesis)\n\n"
    "- **Call:** TODO\n"
    "- **Don't call:** TODO\n"
    "- **Trap:** TODO\n"
    "- **Returns:** TODO\n"
)

cache_directory = Path("scratch/api/llama_cloud") / version
cache_directory.mkdir(parents=True, exist_ok=True)
(cache_directory / f"{TOPIC}.md").write_text(output.getvalue(), encoding="utf-8")
print(output.getvalue())
