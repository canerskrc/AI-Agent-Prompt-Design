"""
test_anti_pattern_linter.py

Unit tests for PromptLinter. No network calls — every detector is
pure regex/lexical logic.
"""

import unittest

from anti_pattern_linter import (
    AssumedExpertDetector,
    ContextDumpDetector,
    HallucinationInvitationDetector,
    InfiniteCanvasDetector,
    LoadedQuestionDetector,
    PhantomConstraintDetector,
    PromptLinter,
    RecursiveVaguenessDetector,
    VagueImperativeDetector,
    _render_human,
    _render_json,
)


class TestVagueImperativeDetector(unittest.TestCase):
    def test_flags_kapsamli_bir_analiz_yap(self):
        findings = VagueImperativeDetector().scan("Kapsamlı bir analiz yap.")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].anti_pattern, "The Vague Imperative")

    def test_does_not_flag_specific_instruction(self):
        findings = VagueImperativeDetector().scan(
            "Yönetici için yazı: 200 kelime, 3 paragraf."
        )
        self.assertEqual(findings, [])


class TestLoadedQuestionDetector(unittest.TestCase):
    def test_flags_neden_harika(self):
        findings = LoadedQuestionDetector().scan(
            "Bu stratejinin neden harika olduğunu açıkla."
        )
        self.assertEqual(len(findings), 1)

    def test_does_not_flag_neutral_evaluation(self):
        findings = LoadedQuestionDetector().scan(
            "Bu stratejiyi değerlendir: güçlü yönler, zayıf yönler, riskler."
        )
        self.assertEqual(findings, [])


class TestInfiniteCanvasDetector(unittest.TestCase):
    def test_flags_unbounded_scope(self):
        findings = InfiniteCanvasDetector().scan("Tüm seçenekleri listele.")
        self.assertEqual(len(findings), 1)

    def test_does_not_flag_when_scope_limited_nearby(self):
        findings = InfiniteCanvasDetector().scan(
            "Tüm seçenekleri değerlendir ama en fazla 3 tanesini listele."
        )
        self.assertEqual(findings, [])


class TestPhantomConstraintDetector(unittest.TestCase):
    def test_flags_kisa_olsun_without_number(self):
        findings = PhantomConstraintDetector().scan("Bana bir e-posta yaz. Kısa olsun.")
        self.assertEqual(len(findings), 1)

    def test_does_not_flag_when_word_count_given(self):
        findings = PhantomConstraintDetector().scan(
            "Kısa yaz: 120 kelime, tek paragraf."
        )
        self.assertEqual(findings, [])


class TestAssumedExpertDetector(unittest.TestCase):
    def test_flags_explain_without_audience(self):
        findings = AssumedExpertDetector().scan("Yapay zeka etik meselesini açıkla.")
        self.assertEqual(len(findings), 1)

    def test_does_not_flag_when_audience_given(self):
        findings = AssumedExpertDetector().scan(
            "Yapay zeka etik meselesini açıkla. "
            "Okuyucu: teknik altyapısı olmayan bir şirket yöneticisi."
        )
        self.assertEqual(findings, [])

    def test_does_not_flag_prompts_without_explain_verb(self):
        findings = AssumedExpertDetector().scan("Bu kodu refactor et.")
        self.assertEqual(findings, [])


class TestHallucinationInvitationDetector(unittest.TestCase):
    def test_flags_en_basarili_n_listesi(self):
        findings = HallucinationInvitationDetector().scan(
            "2024'teki en başarılı 10 Türk AI startup'ını listele."
        )
        self.assertEqual(len(findings), 1)

    def test_does_not_flag_when_hedge_present(self):
        findings = HallucinationInvitationDetector().scan(
            "En başarılı 10 startup'ı listele. Emin değilsen belirt."
        )
        self.assertEqual(findings, [])


class TestContextDumpDetector(unittest.TestCase):
    def test_flags_long_context_without_filter(self):
        long_text = "kelime " * 850 + "Şimdi özet ver."
        findings = ContextDumpDetector().scan(long_text)
        self.assertEqual(len(findings), 1)

    def test_does_not_flag_short_context(self):
        findings = ContextDumpDetector().scan("Kısa bağlam. Özet ver.")
        self.assertEqual(findings, [])

    def test_does_not_flag_long_context_with_filter_marker(self):
        long_text = "kelime " * 850 + "Bu bağlamdan sadece fiyatlandırma ile ilgili kısmı kullan."
        findings = ContextDumpDetector().scan(long_text)
        self.assertEqual(findings, [])


class TestRecursiveVaguenessDetector(unittest.TestCase):
    def test_flags_three_or_more_vague_words(self):
        findings = RecursiveVaguenessDetector().scan(
            "Güzel bir pazarlama metni yaz, hitap etsin, iyi anlatsın."
        )
        self.assertEqual(len(findings), 1)

    def test_does_not_flag_below_threshold(self):
        findings = RecursiveVaguenessDetector().scan("Güzel bir gün.")
        self.assertEqual(findings, [])


class TestPromptLinterIntegration(unittest.TestCase):
    def test_lints_across_all_detectors(self):
        prompt = "Kapsamlı bir analiz yap. Tüm seçenekleri listele."
        findings = PromptLinter().lint(prompt)
        anti_patterns = {f.anti_pattern for f in findings}
        self.assertIn("The Vague Imperative", anti_patterns)
        self.assertIn("The Infinite Canvas", anti_patterns)

    def test_clean_prompt_returns_no_findings(self):
        prompt = (
            "Yönetici için 200 kelimelik özet yaz. 3 paragraf. "
            "Okuyucu: finans bilgisi olmayan bir departman müdürü."
        )
        findings = PromptLinter().lint(prompt)
        self.assertEqual(findings, [])


class TestRendering(unittest.TestCase):
    def test_human_render_no_findings(self):
        output = _render_human([])
        self.assertIn("anti-pattern yok", output)

    def test_human_render_lists_finding_count(self):
        findings = VagueImperativeDetector().scan("Detaylı bir plan hazırla.")
        output = _render_human(findings)
        self.assertIn("1 olası anti-pattern", output)

    def test_json_render_is_valid_and_matches_findings(self):
        import json
        findings = VagueImperativeDetector().scan("İyi bir yazı yaz.")
        output = _render_json(findings)
        parsed = json.loads(output)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["anti_pattern"], "The Vague Imperative")


if __name__ == "__main__":
    unittest.main()
