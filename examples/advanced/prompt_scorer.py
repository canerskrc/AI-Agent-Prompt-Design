"""
prompt_scorer.py

Evaluates the structural quality of an LLM prompt across four dimensions:
clarity, context sufficiency, output specification, and constraint definition.

Usage:
    python prompt_scorer.py --file path/to/prompt.txt
    python prompt_scorer.py --text "Your prompt here"
    python prompt_scorer.py --file prompt.txt --json
"""

import argparse
import json
import os
import sys
import textwrap
from dataclasses import dataclass
from typing import Optional

import anthropic


SCORER_SYSTEM_PROMPT = textwrap.dedent("""
    You are a prompt quality auditor. You evaluate LLM prompts against four
    structural dimensions. You do not comment on the subject matter of the prompt;
    you only assess its engineering quality.

    Respond with a single valid JSON object. No preamble. No explanation outside
    the JSON. No markdown fences.

    The JSON schema is exactly:
    {
        "score": <integer 1-10>,
        "dimensions": {
            "clarity": <integer 1-10>,
            "context_sufficiency": <integer 1-10>,
            "output_specification": <integer 1-10>,
            "constraint_definition": <integer 1-10>
        },
        "issues": [<string>, ...],
        "suggestions": [<string>, ...]
    }

    Scoring rubric for each dimension:

    clarity (1-10)
        Does the prompt express a single, unambiguous intent?
        Are instructions phrased so that only one interpretation is natural?
        Deduct for vague verbs (e.g. "handle", "deal with"), compound goals in
        one sentence, or instructions that contradict each other.

    context_sufficiency (1-10)
        Does the prompt supply enough background for the model to act without
        inference? Deduct for missing persona, absent domain framing, or
        assumptions that the model must guess at.

    output_specification (1-10)
        Does the prompt define the expected output format, length, structure,
        or tone? Deduct for any ambiguity about what a correct response looks like.

    constraint_definition (1-10)
        Does the prompt state what the model must NOT do?
        Are edge cases, refusal conditions, or scope boundaries explicit?
        Deduct for open-ended permission ("you can do anything needed").

    score is the rounded mean of the four dimension scores.

    issues: a list of concrete defects found. Each issue names the problem
    without suggesting a fix. Maximum six items. Empty list if none.

    suggestions: a list of concrete, actionable improvements. Each suggestion
    is one specific change. Maximum six items. Empty list if none.
""").strip()


@dataclass(frozen=True)
class Dimension:
    clarity: int
    context_sufficiency: int
    output_specification: int
    constraint_definition: int


@dataclass(frozen=True)
class ScoreResult:
    score: int
    dimensions: Dimension
    issues: list[str]
    suggestions: list[str]


class ScorerError(Exception):
    pass


class PromptScorer:
    def __init__(self, model: str = "claude-sonnet-4-6"):
        self._client = anthropic.Anthropic()
        self._model = model

    def score(self, prompt_text: str) -> ScoreResult:
        if not prompt_text.strip():
            raise ScorerError("Prompt text is empty.")

        raw = self._call_api(prompt_text)
        return self._parse_response(raw)

    def _call_api(self, prompt_text: str) -> str:
        try:
            message = self._client.messages.create(
                model=self._model,
                max_tokens=1024,
                system=SCORER_SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"Evaluate this prompt:\n\n{prompt_text}",
                    }
                ],
            )
        except anthropic.APIConnectionError as exc:
            raise ScorerError(f"Connection failed: {exc}") from exc
        except anthropic.APIStatusError as exc:
            raise ScorerError(
                f"API returned {exc.status_code}: {exc.message}"
            ) from exc

        return message.content[0].text

    def _parse_response(self, raw: str) -> ScoreResult:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ScorerError(
                f"Model returned invalid JSON. Raw response:\n{raw}"
            ) from exc

        try:
            return ScoreResult(
                score=int(data["score"]),
                dimensions=Dimension(
                    clarity=int(data["dimensions"]["clarity"]),
                    context_sufficiency=int(
                        data["dimensions"]["context_sufficiency"]
                    ),
                    output_specification=int(
                        data["dimensions"]["output_specification"]
                    ),
                    constraint_definition=int(
                        data["dimensions"]["constraint_definition"]
                    ),
                ),
                issues=list(data.get("issues", [])),
                suggestions=list(data.get("suggestions", [])),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ScorerError(
                f"Unexpected response structure: {exc}\nRaw:\n{raw}"
            ) from exc


def _load_prompt(args: argparse.Namespace) -> str:
    if args.file:
        path = args.file
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    if args.text:
        return args.text
    raise ValueError("Provide --file or --text.")


def _render_human(result: ScoreResult) -> str:
    bar_width = 20
    lines = []

    def bar(value: int) -> str:
        filled = round(value / 10 * bar_width)
        return "[" + "#" * filled + "." * (bar_width - filled) + "]"

    lines.append(f"Overall score: {result.score}/10\n")
    lines.append("Dimensions:")
    lines.append(
        f"  Clarity                {bar(result.dimensions.clarity)}"
        f"  {result.dimensions.clarity}/10"
    )
    lines.append(
        f"  Context sufficiency    {bar(result.dimensions.context_sufficiency)}"
        f"  {result.dimensions.context_sufficiency}/10"
    )
    lines.append(
        f"  Output specification   {bar(result.dimensions.output_specification)}"
        f"  {result.dimensions.output_specification}/10"
    )
    lines.append(
        f"  Constraint definition  {bar(result.dimensions.constraint_definition)}"
        f"  {result.dimensions.constraint_definition}/10"
    )

    if result.issues:
        lines.append("\nIssues found:")
        for issue in result.issues:
            lines.append(f"  {issue}")

    if result.suggestions:
        lines.append("\nSuggestions:")
        for suggestion in result.suggestions:
            lines.append(f"  {suggestion}")

    return "\n".join(lines)


def _render_json(result: ScoreResult) -> str:
    payload = {
        "score": result.score,
        "dimensions": {
            "clarity": result.dimensions.clarity,
            "context_sufficiency": result.dimensions.context_sufficiency,
            "output_specification": result.dimensions.output_specification,
            "constraint_definition": result.dimensions.constraint_definition,
        },
        "issues": result.issues,
        "suggestions": result.suggestions,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt_scorer",
        description="Evaluate prompt engineering quality.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            examples:
              python prompt_scorer.py --file my_prompt.txt
              python prompt_scorer.py --text "Summarize the following article."
              python prompt_scorer.py --file my_prompt.txt --json
        """).strip(),
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", metavar="PATH", help="Path to a .txt prompt file.")
    source.add_argument("--text", metavar="TEXT", help="Prompt passed as a string.")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Emit machine-readable JSON instead of formatted output.",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        prompt_text = _load_prompt(args)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
        return

    scorer = PromptScorer()

    try:
        result = scorer.score(prompt_text)
    except ScorerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output_json:
        print(_render_json(result))
    else:
        print(_render_human(result))


if __name__ == "__main__":
    main()
