#!/usr/bin/env python3
"""Dependency-free structural validation for the draft Capability Requirements Document (CRD) schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "crd.schema.json"
EXAMPLES_DIR = ROOT / "examples"


def load_json(path: Path) -> object:
    try:
        with path.open(encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{path.relative_to(ROOT)}: {error}") from error


def assert_fields(value: dict[str, object], fields: list[str], location: str) -> None:
    missing = [field for field in fields if field not in value]
    if missing:
        raise ValueError(f"{location}: missing required fields: {', '.join(missing)}")


def validate_example(schema: dict[str, object], path: Path) -> None:
    instance = load_json(path)
    if not isinstance(instance, dict):
        raise ValueError(f"{path.relative_to(ROOT)}: root must be an object")

    required = schema["required"]
    assert isinstance(required, list)
    assert_fields(instance, required, str(path.relative_to(ROOT)))

    definitions = schema["$defs"]
    assert isinstance(definitions, dict)
    contract_required = definitions["interactionContract"]["required"]
    statement_classes = set(definitions["statement"]["properties"]["semanticClass"]["enum"])
    evidence_statuses = set(definitions["statement"]["properties"]["evidenceStatus"]["enum"])
    realization_schema = definitions["realization"]
    execution_modes = set(realization_schema["properties"]["executionMode"]["enum"])
    shared_schema = definitions["sharedElement"]
    shared_kinds = set(shared_schema["properties"]["kind"]["enum"])
    mapping_schema = definitions["agenticMapping"]
    mapping_kinds = set(mapping_schema["properties"]["kind"]["enum"])
    mapping_relationships = set(mapping_schema["properties"]["relationship"]["enum"])
    projection_schema = definitions["audienceProjection"]
    audiences = set(projection_schema["properties"]["audience"]["enum"])

    contracts = instance["interactionContracts"]
    if not isinstance(contracts, list) or not contracts:
        raise ValueError(f"{path.relative_to(ROOT)}: interactionContracts must be a non-empty array")
    for index, contract in enumerate(contracts):
        if not isinstance(contract, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: interaction contract {index} must be an object")
        assert_fields(contract, contract_required, f"{path.relative_to(ROOT)} contract {index}")

    realizations = instance.get("realizations", [])
    if not isinstance(realizations, list):
        raise ValueError(f"{path.relative_to(ROOT)}: realizations must be an array")
    for realization in realizations:
        if not isinstance(realization, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: realization must be an object")
        if "executionMode" in realization and realization["executionMode"] not in execution_modes:
            raise ValueError(f"{path.relative_to(ROOT)}: unsupported execution mode")

    for element in instance.get("sharedElements", []):
        if not isinstance(element, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: shared element must be an object")
        assert_fields(element, shared_schema["required"], str(path.relative_to(ROOT)))
        if element["kind"] not in shared_kinds:
            raise ValueError(f"{path.relative_to(ROOT)}: unsupported shared-element kind")

    for mapping in instance.get("agenticMappings", []):
        if not isinstance(mapping, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: agentic mapping must be an object")
        assert_fields(mapping, mapping_schema["required"], str(path.relative_to(ROOT)))
        if mapping["kind"] not in mapping_kinds or mapping["relationship"] not in mapping_relationships:
            raise ValueError(f"{path.relative_to(ROOT)}: unsupported agentic mapping")

    for projection in instance.get("audienceProjections", []):
        if not isinstance(projection, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: audience projection must be an object")
        assert_fields(projection, projection_schema["required"], str(path.relative_to(ROOT)))
        if projection["audience"] not in audiences:
            raise ValueError(f"{path.relative_to(ROOT)}: unsupported audience projection")

    statement_groups = [
        instance["rulesInvariants"],
        instance["recommendedDefaults"],
        instance.get("provenance", []),
        *(contract["policiesInvariants"] for contract in contracts),
        *(realization.get("operationalConstraints", []) for realization in realizations),
        *(realization.get("implementationRequirements", []) for realization in realizations),
    ]
    for group in statement_groups:
        if not isinstance(group, list):
            raise ValueError(f"{path.relative_to(ROOT)}: statement group must be an array")
        for statement in group:
            if not isinstance(statement, dict):
                raise ValueError(f"{path.relative_to(ROOT)}: statement must be an object")
            assert_fields(statement, ["text", "semanticClass", "evidenceStatus"], str(path.relative_to(ROOT)))
            if statement["semanticClass"] not in statement_classes:
                raise ValueError(f"{path.relative_to(ROOT)}: unsupported semantic class")
            if statement["evidenceStatus"] not in evidence_statuses:
                raise ValueError(f"{path.relative_to(ROOT)}: unsupported evidence status")


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    if not isinstance(schema, dict):
        raise ValueError("schema root must be an object")
    examples = sorted(EXAMPLES_DIR.glob("*.json"))
    if not examples:
        raise ValueError("no JSON examples found")
    for example in examples:
        validate_example(schema, example)
        print(f"validated {example.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(f"validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
