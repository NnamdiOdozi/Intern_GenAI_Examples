"""Inspect response model fields used by the LlamaCloud proof of concept."""

from __future__ import annotations

import importlib.metadata
import inspect
import types
import typing
from pathlib import Path

from llama_cloud import LlamaCloud
from llama_cloud.types.beta.retrieval_retrieve_response import ResultStaticFields
from llama_cloud.types.parsing_get_response import (
    MarkdownPageFailedMarkdownPage,
    MarkdownPageMarkdownResultPage,
    ResultContentMetadata,
)
from pydantic import BaseModel


METHODS = {
    "parse_response": "parsing.parse",
    "extract_response": "extract.run",
    "index_response": "beta.indexes.get",
    "retrieval_response": "beta.retrieval.retrieve",
}


def resolve_attribute(root: object, dotted: str) -> object:
    """Resolve a dotted attribute path from an object."""
    value = root
    for part in dotted.split("."):
        value = getattr(value, part)
    return value


def model_lines(model: type[BaseModel], depth: int = 0) -> list[str]:
    """Return a bounded recursive field summary for a Pydantic model."""
    lines = [f"{'  ' * depth}{model.__module__}.{model.__name__}"]
    if depth >= 3:
        return lines
    for name, field in model.model_fields.items():
        annotation = field.annotation
        lines.append(f"{'  ' * (depth + 1)}{name}: {annotation}")
        candidates = typing.get_args(annotation) or (annotation,)
        for candidate in candidates:
            origin = typing.get_origin(candidate)
            if origin in (list, tuple, typing.Sequence) or origin is types.UnionType:
                candidates = (*candidates, *typing.get_args(candidate))
            if inspect.isclass(candidate) and issubclass(candidate, BaseModel):
                lines.extend(model_lines(candidate, depth + 2))
                break
    return lines


version = importlib.metadata.version("llama-cloud")
client = LlamaCloud(api_key="inspection-only-placeholder")
sections = [f"# LlamaCloud response models ({version})", ""]
for topic, method_path in METHODS.items():
    method = resolve_attribute(client, method_path)
    return_type = typing.get_type_hints(method)["return"]
    sections.extend([f"## {topic}", "", "```", *model_lines(return_type), "```", ""])

for model in (
    MarkdownPageMarkdownResultPage,
    MarkdownPageFailedMarkdownPage,
    ResultContentMetadata,
    ResultStaticFields,
):
    sections.extend([f"## {model.__name__}", "", "```", *model_lines(model), "```", ""])

target = Path("scratch/api/llama_cloud") / version / "response_models.md"
target.write_text("\n".join(sections), encoding="utf-8")
print(target.read_text(encoding="utf-8"))
