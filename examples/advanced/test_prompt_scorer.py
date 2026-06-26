"""
test_prompt_scorer.py

Unit tests for PromptScorer. The Anthropic API is mocked throughout;
no network calls are made during testing.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from prompt_scorer import (
    Dimension,
    PromptScorer,
    ScoreResult,
    ScorerError,
    _render_human,
    _render_json,
)


def _make_api_response(payload: dict) -> MagicMock:
    message = MagicMock()
    message.content = [MagicMock(text=json.dumps(payload))]
    return message


VALID_PAYLOAD = {
    "score": 6,
    "dimensions": {
        "clarity": 8,
        "context_sufficiency": 4,
        "output_specification": 7,
        "constraint_definition": 5,
    },
    "issues": ["Output format not specified"],
    "suggestions": ["Add an explicit output schema"],
}


class TestPromptScorerParsing(unittest.TestCase):

    def _scorer(self) -> PromptScorer:
        return PromptScorer()

    @patch("prompt_scorer.anthropic.Anthropic")
    def test_valid_response_produces_correct_result(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value = _make_api_response(VALID_PAYLOAD)

        result = self._scorer().score("Summarize the document.")

        self.assertIsInstance(result, ScoreResult)
        self.assertEqual(result.score, 6)
        self.assertEqual(result.dimensions.clarity, 8)
        self.assertEqual(result.dimensions.context_sufficiency, 4)
        self.assertEqual(result.dimensions.output_specification, 7)
        self.assertEqual(result.dimensions.constraint_definition, 5)
        self.assertEqual(result.issues, ["Output format not specified"])
        self.assertEqual(result.suggestions, ["Add an explicit output schema"])

    @patch("prompt_scorer.anthropic.Anthropic")
    def test_invalid_json_raises_scorer_error(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        message = MagicMock()
        message.content = [MagicMock(text="not json at all")]
        mock_client.messages.create.return_value = message

        with self.assertRaises(ScorerError) as ctx:
            self._scorer().score("Some prompt.")

        self.assertIn("invalid JSON", str(ctx.exception))

    @patch("prompt_scorer.anthropic.Anthropic")
    def test_missing_dimension_key_raises_scorer_error(self, mock_anthropic):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        broken = {**VALID_PAYLOAD, "dimensions": {"clarity": 5}}
        mock_client.messages.create.return_value = _make_api_response(broken)

        with self.assertRaises(ScorerError):
            self._scorer().score("Some prompt.")

    def test_empty_prompt_raises_scorer_error(self):
        with self.assertRaises(ScorerError) as ctx:
            PromptScorer().score("   ")
        self.assertIn("empty", str(ctx.exception))


class TestResultRendering(unittest.TestCase):

    def _result(self) -> ScoreResult:
        return ScoreResult(
            score=6,
            dimensions=Dimension(
                clarity=8,
                context_sufficiency=4,
                output_specification=7,
                constraint_definition=5,
            ),
            issues=["Output format not specified"],
            suggestions=["Add an explicit output schema"],
        )

    def test_human_render_contains_score(self):
        output = _render_human(self._result())
        self.assertIn("6/10", output)

    def test_human_render_contains_all_dimension_names(self):
        output = _render_human(self._result())
        self.assertIn("Clarity", output)
        self.assertIn("Context sufficiency", output)
        self.assertIn("Output specification", output)
        self.assertIn("Constraint definition", output)

    def test_human_render_contains_issues(self):
        output = _render_human(self._result())
        self.assertIn("Output format not specified", output)

    def test_human_render_contains_suggestions(self):
        output = _render_human(self._result())
        self.assertIn("Add an explicit output schema", output)

    def test_human_render_no_issues_section_when_empty(self):
        result = ScoreResult(
            score=9,
            dimensions=Dimension(9, 9, 9, 9),
            issues=[],
            suggestions=[],
        )
        output = _render_human(result)
        self.assertNotIn("Issues found", output)

    def test_json_render_is_valid_json(self):
        output = _render_json(self._result())
        parsed = json.loads(output)
        self.assertEqual(parsed["score"], 6)

    def test_json_render_contains_all_dimensions(self):
        output = _render_json(self._result())
        parsed = json.loads(output)
        dims = parsed["dimensions"]
        self.assertIn("clarity", dims)
        self.assertIn("context_sufficiency", dims)
        self.assertIn("output_specification", dims)
        self.assertIn("constraint_definition", dims)


if __name__ == "__main__":
    unittest.main()
