#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "ruamel.yaml>=0.18.14",
#   "jinja2>=3.1.6",
# ]
# ///


import argparse
import pathlib
from typing import Any

from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML


def get_action_path(action_input: pathlib.Path) -> str:
    action_input = action_input.resolve()
    action_dir = action_input.parent
    relative_path = action_dir.relative_to(pathlib.Path(__file__).parents[1])
    return f"mozilla-it/deploy-actions/{relative_path.as_posix()}"


def validate_inputs(inputs: dict[str, Any]) -> None:
    for key, spec in inputs.items():
        if spec.get("required") and not spec.get("example"):
            raise ValueError(f"Required input '{key}' does not provide an example")


def format_input_lines(inputs: dict[str, Any]):
    for key, spec in inputs.items():
        value = str(spec["example"] if spec.get("required") else spec["default"])
        if "\n" in value:
            yield f"    {key}: |"
            yield from (f"      {line}" for line in value.splitlines())
        else:
            yield f"    {key}: {value}"


def generate_example_usage(action_path: str, inputs: dict[str, Any]) -> str:
    input_usage = [
        "```yaml",
        f"- uses: {action_path}",
        "  with:",
        *format_input_lines(inputs),
        "```",
    ]
    return "\n".join(input_usage)


def load_custom_usage_examples(usage_examples_dir: pathlib.Path) -> str:
    if not usage_examples_dir.is_dir():
        raise ValueError(f"Usage dir '{usage_examples_dir}' does not exist")

    usage_files = sorted(usage_examples_dir.glob("*.md"))
    examples = []

    for file_path in usage_files:
        content = file_path.read_text().strip()
        if content:
            examples.append(content)

    return "\n\n".join(examples)


def generate_minimal_usage_example(action_path: str, inputs: dict[str, Any]):
    inputs = {key: spec for key, spec in inputs.items() if spec.get("required")}
    return generate_example_usage(action_path, inputs)


def generate_defaults_usage_example(action_path: str, inputs: dict[str, Any]):
    inputs = {
        key: spec
        for key, spec in inputs.items()
        if spec.get("required") or spec.get("default")
    }
    return generate_example_usage(action_path, inputs)


def parse_args():
    p = argparse.ArgumentParser(
        description="Generate README.md from GitHub Actions action.yml"
    )
    p.add_argument(
        "-i",
        "--input",
        default="action.yml",
        type=pathlib.Path,
        help="Path to action.yml (default: %(default)s)",
    )
    p.add_argument(
        "-o",
        "--output",
        default="README.md",
        type=pathlib.Path,
        help="Path for generated README (default: %(default)s)",
    )
    p.add_argument(
        "-u",
        "--usage-examples-dir",
        required=False,
        type=pathlib.Path,
        help="Path to directory containing custom usage examples to include in generated README",
    )
    return p.parse_args()


def main():
    args = parse_args()

    yaml = YAML()
    data = yaml.load(args.input.read_text())

    # get inputs and generate example usage
    inputs = data.get("inputs")
    validate_inputs(inputs)
    action_path = get_action_path(args.input)
    minimal_usage_example = generate_minimal_usage_example(action_path, inputs)
    defaults_usage_example = generate_defaults_usage_example(action_path, inputs)

    # load custom usage examples
    custom_usage_examples = None
    if args.usage_examples_dir:
        custom_usage_examples = load_custom_usage_examples(args.usage_examples_dir)

    # build template and write out README
    env = Environment(loader=FileSystemLoader("scripts"))
    template = env.get_template("README.md.jinja2")
    output = template.render(
        name=data["name"],
        description=data["description"],
        inputs=inputs,
        outputs=data.get("outputs"),
        minimal_usage_example=minimal_usage_example,
        defaults_usage_example=defaults_usage_example,
        custom_usage_examples=custom_usage_examples,
    )
    args.output.write_text(output)


if __name__ == "__main__":
    main()
