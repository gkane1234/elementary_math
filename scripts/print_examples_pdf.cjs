/**
 * Print an examples HTML file → PDF via Playwright.
 * Waits for KaTeX (data-math-ready) so math is not blank.
 *
 * Usage:
 *   node print_examples_pdf.cjs [htmlPath] [pdfPath]
 *
 * Defaults:
 *   scripts/output/all_types_examples.html
 *   scripts/output/all_types_examples.pdf
 */
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

async function main() {
  const outDir = path.join(__dirname, "output");
  const htmlPath = path.resolve(
    process.argv[2] || path.join(outDir, "all_types_examples.html"),
  );
  const pdfPath = path.resolve(
    process.argv[3] || path.join(outDir, "all_types_examples.pdf"),
  );
  if (!fs.existsSync(htmlPath)) {
    throw new Error(`HTML not found: ${htmlPath}`);
  }
  fs.mkdirSync(path.dirname(pdfPath), { recursive: true });
  const fileUrl = "file:///" + htmlPath.replace(/\\/g, "/");

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  page.setDefaultTimeout(180_000);
  await page.goto(fileUrl, { waitUntil: "networkidle" });
  await page.waitForFunction(
    () => document.documentElement.getAttribute("data-math-ready") === "1",
    null,
    { timeout: 120_000 },
  );
  await page.waitForTimeout(500);

  // Margins come from the HTML @page rule so CSS page-breaks line up with print.
  await page.pdf({
    path: pdfPath,
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: "0", right: "0", bottom: "0", left: "0" },
  });

  // Spot-checks only for the default all-types doc (keeps Grade 6 runs quieter).
  const isDefaultAll =
    path.basename(htmlPath) === "all_types_examples.html";
  if (isDefaultAll) {
    const shots = path.join(outDir, "_pdf_spotchecks");
    fs.mkdirSync(shots, { recursive: true });

    const ids = [
      "pa_plotting_points",
      "graphing_linear_equations",
      "graphing_single_variable_inequalities",
      "more_on_slope",
      "geo_basics_basic_angle_terminology",
    ];
    for (const id of ids) {
      const handle = await page.$(`section.type-section:has(code:text-is("${id}"))`);
      if (handle) {
        await handle.screenshot({ path: path.join(shots, `${id}.png`) });
        console.log("shot", id);
      } else {
        console.log("missing section", id);
      }
    }
    const first = await page.$("section.type-section");
    if (first) await first.screenshot({ path: path.join(shots, "first_section.png") });
    console.log(`Spot-checks: ${shots}`);
  }

  await browser.close();
  const size = fs.statSync(pdfPath).size;
  console.log(`PDF written: ${pdfPath} (${size} bytes)`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
