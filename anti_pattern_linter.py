"""
anti_pattern_linter.py

Scans a prompt for the eight anti-patterns documented in
docs/prompt-patterns.md and reports each occurrence with a fix hint.

Unlike prompt_scorer.py, this tool makes no API calls. Detection is
rule-based (regex and lexical heuristics), so it is fast, offline, and
free to run — at the cost of being a blunter instrument than an LLM
judge. It catches surface-level phrasing issues; it will not catch an
anti-pattern expressed in unusual wording, and it can flag a phrase
that is actually fine in context. Treat findings as things to look at,
not verdicts.

Usage:
    python anti_pattern_linter.py --file path/to/prompt.txt
    python anti_pattern_linter.py --text "Kapsamlı bir analiz yap."
    python anti_pattern_linter.py --file prompt.txt --json
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    anti_pattern: str
    excerpt: str
    explanation: str
    fix_hint: str


class Detector:
    """One anti-pattern check. name/doc_ref match docs/prompt-patterns.md exactly."""

    name: str = ""
    doc_ref: str = ""

    def scan(self, text: str) -> list[Finding]:
        raise NotImplementedError


class VagueImperativeDetector(Detector):
    name = "The Vague Imperative"
    doc_ref = "Anti-Pattern 1"

    _PATTERN = re.compile(
        r"\b(iyi|kapsamlı|detaylı)\s+bir\s+\w*\s*(yaz|hazırla|yap|oluştur|üret)",
        re.IGNORECASE,
    )

    def scan(self, text: str) -> list[Finding]:
        findings = []
        for match in self._PATTERN.finditer(text):
            findings.append(
                Finding(
                    anti_pattern=self.name,
                    excerpt=match.group(0),
                    explanation=(
                        "\"İyi\", \"kapsamlı\", \"detaylı\" modele göre "
                        "tanımsız — kendi standardını kullanır."
                    ),
                    fix_hint=(
                        "Ölçülebilir bir kısıt ekle: uzunluk, yapı, "
                        "veya bir örnek çıktı."
                    ),
                )
            )
        return findings


class LoadedQuestionDetector(Detector):
    name = "The Loaded Question"
    doc_ref = "Anti-Pattern 2"

    _PATTERN = re.compile(
        r"neden (harika|mükemmel|başarılı|üstün)|üstünlük(lerini)?\s+(listele|say|anlat)|"
        r"avantaj(larını)?\s+(listele|say|anlat)",
        re.IGNORECASE,
    )

    def scan(self, text: str) -> list[Finding]:
        findings = []
        for match in self._PATTERN.finditer(text):
            findings.append(
                Finding(
                    anti_pattern=self.name,
                    excerpt=match.group(0),
                    explanation=(
                        "Sonuç modele önceden söyleniyor; model o yönde "
                        "argüman üretir, zayıf yönleri görmez."
                    ),
                    fix_hint=(
                        "Tarafsız çerçevele: \"değerlendir\" + "
                        "güçlü/zayıf yön iste."
                    ),
                )
            )
        return findings


class InfiniteCanvasDetector(Detector):
    name = "The Infinite Canvas"
    doc_ref = "Anti-Pattern 3"

    _UNBOUNDED = re.compile(
        r"\b(her şeyi|tüm seçenekleri|eksiksiz|kapsamlı bir rehber)\b",
        re.IGNORECASE,
    )
    _HAS_SCOPE_LIMIT = re.compile(
        r"\b(en fazla|en çok|ilk|sadece|yalnızca)\s+\d+\b", re.IGNORECASE
    )

    def scan(self, text: str) -> list[Finding]:
        findings = []
        for match in self._UNBOUNDED.finditer(text):
            window = text[match.start(): match.start() + 200]
            if self._HAS_SCOPE_LIMIT.search(window):
                continue
            findings.append(
                Finding(
                    anti_pattern=self.name,
                    excerpt=match.group(0),
                    explanation=(
                        "Sınırsız görev — model ne kadar yazacağını bilmiyor."
                    ),
                    fix_hint="Kapsamı sayıyla sınırla: \"en kritik N ...\".",
                )
            )
        return findings


class PhantomConstraintDetector(Detector):
    name = "The Phantom Constraint"
    doc_ref = "Anti-Pattern 4"

    _VAGUE_LENGTH = re.compile(r"\b(kısa|uzun|hızlı)\s+(olsun|yaz|tut)\b", re.IGNORECASE)
    _HAS_NUMBER_NEARBY = re.compile(r"\d+\s*(kelime|cümle|paragraf|saniye|dakika)")

    def scan(self, text: str) -> list[Finding]:
        findings = []
        for match in self._VAGUE_LENGTH.finditer(text):
            window = text[max(0, match.start() - 60): match.start() + 60]
            if self._HAS_NUMBER_NEARBY.search(window):
                continue
            findings.append(
                Finding(
                    anti_pattern=self.name,
                    excerpt=match.group(0),
                    explanation=(
                        "\"Kısa\"/\"uzun\" belirsiz — model için 5 cümle de "
                        "kısadır, 15 cümle de."
                    ),
                    fix_hint="Sayısal veya yapısal kısıt ver: \"3 paragraf, 120 kelime\".",
                )
            )
        return findings


class AssumedExpertDetector(Detector):
    name = "The Assumed Expert"
    doc_ref = "Anti-Pattern 5"

    _EXPLAIN_VERB = re.compile(r"\b(açıkla|anlat)\b", re.IGNORECASE)
    _AUDIENCE_MARKER = re.compile(
        r"\b(kitle|okuyucu|hedef kitle|seviyesinde|için yaz|kimin için)\b",
        re.IGNORECASE,
    )

    def scan(self, text: str) -> list[Finding]:
        if not self._EXPLAIN_VERB.search(text):
            return []
        if self._AUDIENCE_MARKER.search(text):
            return []
        match = self._EXPLAIN_VERB.search(text)
        return [
            Finding(
                anti_pattern=self.name,
                excerpt=match.group(0),
                explanation=(
                    "Hedef kitle belirtilmemiş — model \"ortalama okuyucu\" "
                    "varsayıyor, bu genelde siz değilsiniz."
                ),
                fix_hint="Kitleyi davranışsal olarak tanımla (bkz. Pattern 8: Audience Calibration).",
            )
        ]


class HallucinationInvitationDetector(Detector):
    name = "The Hallucination Invitation"
    doc_ref = "Anti-Pattern 6"

    _PATTERN = re.compile(
        r"en (başarılı|iyi)\s+\d+|"
        r"\b(20\d{2})'(teki|deki)\s+en\b|"
        r"son çeyrek (geliri|karı)|"
        r"\bDr\.\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+'?\w*\s+(görüşü|düşüncesi)",
        re.IGNORECASE,
    )
    _HEDGE_MARKER = re.compile(
        r"emin değilsen|erişimin yoksa|belirt|doğrulama gerekir", re.IGNORECASE
    )

    def scan(self, text: str) -> list[Finding]:
        findings = []
        for match in self._PATTERN.finditer(text):
            if self._HEDGE_MARKER.search(text):
                continue
            findings.append(
                Finding(
                    anti_pattern=self.name,
                    excerpt=match.group(0),
                    explanation=(
                        "Bu tarz sorular modeli bilmediği şeyi üretmeye "
                        "(halüsinasyona) davet ediyor."
                    ),
                    fix_hint=(
                        "Veriyi sen sağla, bir arama aracı bağla, ya da "
                        "modele bilgisini sorgulatacak bir hedge ekle."
                    ),
                )
            )
        return findings


class ContextDumpDetector(Detector):
    name = "The Context Dump"
    doc_ref = "Anti-Pattern 7"

    _FILTER_MARKER = re.compile(
        r"sadece .*ile ilgili|bu bağlamdan|yalnızca .*kısmı", re.IGNORECASE
    )
    WORD_THRESHOLD = 800

    def scan(self, text: str) -> list[Finding]:
        word_count = len(text.split())
        if word_count < self.WORD_THRESHOLD:
            return []
        if self._FILTER_MARKER.search(text):
            return []
        return [
            Finding(
                anti_pattern=self.name,
                excerpt=f"[{word_count} kelimelik bağlam]",
                explanation=(
                    "Uzun bağlam metni + filtre yönergesi yok — model hangi "
                    "kısmın önemli olduğunu tahmin etmek zorunda kalıyor."
                ),
                fix_hint="\"Bu bağlamdan sadece X ile ilgili kısmı kullan\" gibi bir filtre ekle.",
            )
        ]


class RecursiveVaguenessDetector(Detector):
    name = "The Recursive Vagueness"
    doc_ref = "Anti-Pattern 8"

    _VAGUE_WORDS = re.compile(
        r"\b(güzel|iyi|kapsamlı|detaylı|harika|hitap etsin|iyi anlatsın)\b",
        re.IGNORECASE,
    )
    MIN_OCCURRENCES = 3

    def scan(self, text: str) -> list[Finding]:
        matches = self._VAGUE_WORDS.findall(text)
        if len(matches) < self.MIN_OCCURRENCES:
            return []
        return [
            Finding(
                anti_pattern=self.name,
                excerpt=", ".join(sorted(set(m if isinstance(m, str) else m[0] for m in matches))),
                explanation=(
                    f"Prompt'ta {len(matches)} adet belirsiz kelime var — "
                    "belirsizlik üstüne belirsizlik birikiyor."
                ),
                fix_hint="Her belirsiz kelimeyi tek tek somutlaştır (bkz. Anti-Pattern 8 örneği).",
            )
        ]


DETECTORS: list[Detector] = [
    VagueImperativeDetector(),
    LoadedQuestionDetector(),
    InfiniteCanvasDetector(),
    PhantomConstraintDetector(),
    AssumedExpertDetector(),
    HallucinationInvitationDetector(),
    ContextDumpDetector(),
    RecursiveVaguenessDetector(),
]


class PromptLinter:
    def __init__(self, detectors: list[Detector] | None = None):
        self._detectors = detectors if detectors is not None else DETECTORS

    def lint(self, text: str) -> list[Finding]:
        findings: list[Finding] = []
        for detector in self._detectors:
            findings.extend(detector.scan(text))
        return findings


def _load_prompt(args: argparse.Namespace) -> str:
    if args.file:
        if not os.path.isfile(args.file):
            raise FileNotFoundError(f"File not found: {args.file}")
        with open(args.file, encoding="utf-8") as fh:
            return fh.read()
    if args.text:
        return args.text
    raise ValueError("Provide --file or --text.")


def _render_human(findings: list[Finding]) -> str:
    if not findings:
        return "Bulunan anti-pattern yok. (Bu bir kalite garantisi değil — bkz. dosya başındaki not.)"

    lines = [f"{len(findings)} olası anti-pattern bulundu:\n"]
    for i, f in enumerate(findings, start=1):
        lines.append(f"{i}. [{f.anti_pattern}]")
        lines.append(f"   Yakalanan: \"{f.excerpt}\"")
        lines.append(f"   Neden: {f.explanation}")
        lines.append(f"   Öneri: {f.fix_hint}\n")
    return "\n".join(lines)


def _render_json(findings: list[Finding]) -> str:
    payload = [
        {
            "anti_pattern": f.anti_pattern,
            "excerpt": f.excerpt,
            "explanation": f.explanation,
            "fix_hint": f.fix_hint,
        }
        for f in findings
    ]
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anti_pattern_linter",
        description="docs/prompt-patterns.md içindeki 8 anti-pattern için kural tabanlı, offline tarama.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", metavar="PATH", help="Prompt metni içeren dosya.")
    source.add_argument("--text", metavar="TEXT", help="Prompt doğrudan metin olarak.")
    parser.add_argument(
        "--json", action="store_true", dest="output_json",
        help="Okunabilir çıktı yerine JSON üret.",
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

    findings = PromptLinter().lint(prompt_text)

    if args.output_json:
        print(_render_json(findings))
    else:
        print(_render_human(findings))


if __name__ == "__main__":
    main()
