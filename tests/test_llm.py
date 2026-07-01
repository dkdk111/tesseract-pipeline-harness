"""The live-model seam: it parses model JSON, and it fails loudly without a key.
No network is touched here."""

import os
import unittest

from tesseract_pipeline import llm


class ParseTests(unittest.TestCase):
    def test_parses_bare_json(self):
        self.assertEqual(llm._parse_json('{"goal": "x"}'), {"goal": "x"})

    def test_strips_code_fence(self):
        raw = '```json\n{"goal": "x", "iterative": true}\n```'
        self.assertEqual(llm._parse_json(raw), {"goal": "x", "iterative": True})

    def test_extracts_object_amid_prose(self):
        raw = 'Here it is: {"goal": "x"} hope that helps'
        self.assertEqual(llm._parse_json(raw), {"goal": "x"})


class NoKeyTests(unittest.TestCase):
    _VARS = ("TESSERACT_LLM_PROVIDER", "ANTHROPIC_API_KEY")

    def setUp(self):
        self._saved = {k: os.environ.pop(k, None) for k in self._VARS}

    def tearDown(self):
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v

    def test_planner_raises_without_key(self):
        # Default provider is anthropic; with no ANTHROPIC_API_KEY it must fail loudly.
        with self.assertRaises(RuntimeError):
            llm.LLMPlanner().infer("do something")

    def test_worker_raises_without_key(self):
        with self.assertRaises(RuntimeError):
            llm.LLMWorker().run("do something")

    def test_unknown_provider_raises(self):
        os.environ["TESSERACT_LLM_PROVIDER"] = "nope"
        with self.assertRaises(RuntimeError):
            llm.call_model("s", "u")


if __name__ == "__main__":
    unittest.main()
