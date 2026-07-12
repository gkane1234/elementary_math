"""Generate Grade 6 Ready-type E/M/H examples PDF.

Thin wrapper around generate_all_types_examples_pdf.py.

Output:
  scripts/output/grade6_all_types_examples.pdf
  scripts/output/grade6_all_types_examples.html
"""

from __future__ import annotations

from generate_all_types_examples_pdf import main

if __name__ == "__main__":
    main(["--course", "grade_6"])
