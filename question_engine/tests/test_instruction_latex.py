import unittest

from question_engine.catalogs.algebra_1 import CATALOG as ALGEBRA_1_CATALOG
from question_engine.utils.instruction_latex import (
    repair_instruction_latex,
    resolve_instruction_latex,
    wrap_instruction_text,
)


class InstructionLatexTests(unittest.TestCase):
    def test_repair_tab_corrupted_text_command(self):
        corrupted = "\text{Evaluate.}"
        repaired = repair_instruction_latex(corrupted)
        self.assertEqual(repaired, r"\text{Evaluate.}")
        self.assertTrue(repaired.startswith("\\"))

    def test_repair_ext_prefix_without_tab(self):
        self.assertEqual(repair_instruction_latex("ext{Solve.}"), r"\text{Solve.}")

    def test_resolve_wraps_instruction_text(self):
        self.assertEqual(
            resolve_instruction_latex("", "Find the measure."),
            r"\text{Find the measure.}",
        )

    def test_algebra_1_catalog_entries_use_text_command(self):
        for entry in ALGEBRA_1_CATALOG:
            latex = entry.instruction_latex
            self.assertTrue(
                latex.startswith(r"\text{"),
                f"{entry.id} instruction_latex must start with \\text{{}}: {latex!r}",
            )
            self.assertNotIn("\t", latex)

    def test_wrap_instruction_text(self):
        self.assertEqual(wrap_instruction_text("Simplify."), r"\text{Simplify.}")


if __name__ == "__main__":
    unittest.main()
