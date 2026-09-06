"""Lookup the installed LlamaCloud Extract configuration type."""

from __future__ import annotations

import datetime
import inspect
import io
import pydoc
from pathlib import Path

import llama_cloud
from llama_cloud.types.extract_configuration_param import ExtractConfigurationParam


try:
    signature = str(inspect.signature(ExtractConfigurationParam))
except (TypeError, ValueError):
    signature = "<TypedDict; see annotations and help below>"

output = io.StringIO()
output.write("# extract_configuration_param\n\n")
output.write(
    "Source: inspect: llama_cloud.types.ExtractConfigurationParam "
    f"@ {llama_cloud.__version__}\n"
)
output.write(f"Probed: {datetime.date.today():%Y-%m-%d}\n\n")
output.write(f"## Signature\n\n```\n{signature}\n```\n\n")
output.write("## Annotations\n\n```\n")
for name, annotation in ExtractConfigurationParam.__annotations__.items():
    output.write(f"{name}: {annotation}\n")
output.write("```\n\n")
output.write("## help()\n\n```\n")
output.write(pydoc.render_doc(ExtractConfigurationParam, renderer=pydoc.plaintext))
output.write("\n```\n\n")
output.write(
    "## Usage\n\n"
    "- **Call:** Pass this mapping as `configuration` to `client.extract.run`.\n"
    "- **Don't call:** Do not pass v1-only fields absent from these annotations.\n"
    "- **Trap:** `target_pages` is the installed v2 page-window control; "
    "`num_pages_context` is not supported in SDK 2.15.0.\n"
    "- **Returns:** The mapping configures the Extract job; `run` returns an "
    "`ExtractV2Job`.\n"
)

cache = Path("scratch/api/llama_cloud/2.15.0/extract_configuration_param.md")
cache.write_text(output.getvalue(), encoding="utf-8")
print(output.getvalue())
