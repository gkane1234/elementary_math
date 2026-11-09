import katex from "katex";
import Link from "next/link";
import { LandingDemo } from "@/components/LandingDemo";
import {
  CATALOG_TYPES_SCORED,
  COURSES,
  DERIVATIVE_SHEET,
  EFFORT_FLOW,
  EFFORT_MODELS,
  FACTORING_SAMPLE,
  GENERATOR_PATH,
  PRODUCT_SHELL,
  QA_CONCERNS,
  formatDifficulty,
} from "@/lib/landing";
import { collapseRedundantLeftGroups } from "@/lib/latex";
import { listGalleryEntries } from "@/lib/worksheet-gallery";
import { formatTopicLabel } from "@/lib/topic-labels";
import {
  WORKSHEET_DIFFICULTY_PRESETS,
  worksheetDifficultyToRamp,
} from "@/lib/worksheet-difficulty";

const derivativeHref = `/gallery/${DERIVATIVE_SHEET.id}`;
const exampleCount = listGalleryEntries().length;
const heroRamp = worksheetDifficultyToRamp(DERIVATIVE_SHEET.level);

function scheduleName(schedule: string): string {
  return schedule.charAt(0).toUpperCase() + schedule.slice(1);
}

function MathLine({ content }: { content: string }) {
  const html = katex.renderToString(collapseRedundantLeftGroups(content), {
    throwOnError: false,
    displayMode: false,
  });
  return <span className="question-prompt" dangerouslySetInnerHTML={{ __html: html }} />;
}

export function LandingPage() {
  return (
    <div className="landing">
      <section className="landing-hero">
        <div>
          <p className="landing-kicker">Grade 6 through Calculus</p>
          <h1 className="landing-title">A worksheet generator that knows how hard the question is.</h1>
          <p className="landing-lede">
            {CATALOG_TYPES_SCORED} question types, a continuous difficulty scale, and sheets that
            start at one topic and walk into the next.
          </p>
          <div className="landing-actions">
            <Link className="landing-button" href={GENERATOR_PATH}>
              Open the generator
            </Link>
            <Link className="landing-button landing-button-secondary" href={derivativeHref}>
              View a calculus sheet
            </Link>
          </div>
        </div>

        <LandingDemo />
      </section>

      <section className="landing-spine" aria-label="Courses">
        <ul className="landing-courses">
          {COURSES.map((course) => (
            <li key={course}>{course}</li>
          ))}
        </ul>
        <p className="landing-caption">
          Each course is a tree of topics you can assign, from a ratio introduction through
          derivative rules. Every catalog type has a continuous difficulty parameter and an effort
          scorer.
        </p>
      </section>

      <section className="landing-section">
        <div className="landing-story">
          <div>
            <h2>Build a sheet</h2>
            <p>
              Settings sit on the left: manual topics or a progressive ramp, a worksheet level, a
              target page count, and print. The preview in the middle is the sheet itself, in
              KaTeX, with diagrams when the topic has them. The topic browser on the right is the
              curriculum, from course to chapter to a single question type.
            </p>
            <p>
              <Link href={GENERATOR_PATH}>Open the generator</Link>
            </p>
          </div>
          <div className="landing-columns" aria-label="Generator layout">
            <article>
              <h3>Settings</h3>
              <ul>
                <li>Manual topics or progressive practice</li>
                <li>Worksheet level 0–4</li>
                <li>Target page count and page-break guides</li>
                <li>Answer key and browser print</li>
              </ul>
            </article>
            <article>
              <h3>Preview</h3>
              <ul>
                <li>KaTeX prompts</li>
                <li>Diagrams on topics that have them</li>
                <li>Answer key after unlock</li>
              </ul>
            </article>
            <article>
              <h3>Topics</h3>
              <ul>
                <li>Course, then chapter, then a leaf</li>
                <li>Add a topic or change the seed</li>
                <li>Related topics stay on the same sheet</li>
              </ul>
            </article>
          </div>
        </div>
      </section>

      <section className="landing-section">
        <h2>Difficulty changes the problem</h2>
        <p>
          Each question type takes a difficulty from 0 to 25. Raising it changes the problem the
          student sees. A worksheet level then spreads a band of those values across one sheet.
        </p>
        <div className="landing-samples">
          <p className="landing-sample-instruction">{FACTORING_SAMPLE.instruction}</p>
          <div className="landing-sample-grid">
            {FACTORING_SAMPLE.samples.map((sample) => (
              <article key={sample.difficulty} className="landing-sample">
                <h3>D {sample.difficulty}</h3>
                <MathLine content={sample.promptLatex} />
              </article>
            ))}
          </div>
          <p className="landing-caption">
            {formatTopicLabel(FACTORING_SAMPLE.typeId, FACTORING_SAMPLE.name)}, seed{" "}
            {FACTORING_SAMPLE.seed}. D 0 is a monic trinomial, D 8 has a leading coefficient other
            than 1, and D 22 is unsorted and still needs like terms combined.
          </p>
        </div>
        <div className="landing-table-wrap">
          <table className="landing-table">
            <caption>Worksheet level to difficulty ramp</caption>
            <thead>
              <tr>
                <th scope="col">Level</th>
                <th scope="col">Schedule</th>
                <th scope="col">What the band is for</th>
              </tr>
            </thead>
            <tbody>
              {WORKSHEET_DIFFICULTY_PRESETS.map((level) => {
                const ramp = worksheetDifficultyToRamp(level);
                return (
                  <tr key={level}>
                    <td>
                      <span className={`gallery-badge gallery-badge--${ramp.schedule}`}>
                        {ramp.label}
                        <span className="gallery-badge-range">
                          D {ramp.d_min}–{ramp.d_max}
                        </span>
                      </span>
                    </td>
                    <td>{scheduleName(ramp.schedule)}</td>
                    <td>{ramp.description}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="landing-section">
        <div className="landing-story">
          <div>
            <h2>One sheet, several topics</h2>
            <p>
              Progressive mode seeds one topic and fills the sheet with that topic and its
              neighbors. Difficulty climbs from the first question to the last. The table is the
              saved derivatives sheet: {DERIVATIVE_SHEET.questions.length} questions,{" "}
              {heroRamp.label}, D {heroRamp.d_min} to {heroRamp.d_max}.
            </p>
            <p className="landing-inline-links">
              <Link href={derivativeHref}>View this example</Link>
              <Link href="/gallery">
                Browse {exampleCount} {exampleCount === 1 ? "example" : "examples"}
              </Link>
            </p>
          </div>
          <div className="landing-table-wrap">
            <table className="landing-table">
              <caption>{DERIVATIVE_SHEET.title}, in sheet order</caption>
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Topic</th>
                  <th scope="col">D</th>
                </tr>
              </thead>
              <tbody>
                {DERIVATIVE_SHEET.questions.map((question) => (
                  <tr key={question.number}>
                    <td>{question.number}</td>
                    <td>{formatTopicLabel(question.typeId, question.name)}</td>
                    <td>{formatDifficulty(question.difficulty)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="landing-engineering">
        <h2>How difficulty is learned</h2>
        <p>
          Every catalog type is scored. A forward model predicts effort from the parameters that
          built the question. Inverse search, where it is shipped, looks for parameters that hit a
          target effort.
        </p>
        <ol className="landing-flow">
          {EFFORT_FLOW.map((step, index) => (
            <li key={step}>
              <span>{step}</span>
              {index < EFFORT_FLOW.length - 1 ? (
                <span className="landing-flow-arrow" aria-hidden="true">
                  →
                </span>
              ) : null}
            </li>
          ))}
        </ol>
        <p className="landing-stat">
          <strong>{CATALOG_TYPES_SCORED}</strong>
          <span>catalog types with an effort scorer</span>
        </p>
        <div className="landing-table-wrap">
          <table className="landing-table">
            <caption>Forward models on labeled exports</caption>
            <thead>
              <tr>
                <th scope="col">Course</th>
                <th scope="col">Labeled export</th>
                <th scope="col">Correlation</th>
              </tr>
            </thead>
            <tbody>
              {EFFORT_MODELS.map((model) => (
                <tr key={model.course}>
                  <td>{model.course}</td>
                  <td>{model.labeled}</td>
                  <td>r ≈ {model.correlation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="landing-caption">
          Grade 6 ratios and Pre-Algebra have forward models too. Inverse search is in place for
          Grade 6 ratios, Pre-Algebra, and Algebra 2. Precalculus and Calculus inverse search is
          not shipped yet.
        </p>
        <div className="landing-qa">
          {QA_CONCERNS.map((item) => (
            <article key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-section">
        <h2>A worksheet you can unlock and print</h2>
        <div className="landing-shell">
          {PRODUCT_SHELL.map((item) => (
            <article key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </section>

      <footer className="landing-footer">
        <p>Next.js, a Python question engine, KaTeX, Auth.js, and Stripe.</p>
        <p className="landing-inline-links">
          <Link href={GENERATOR_PATH}>Generator</Link>
          <Link href="/gallery">Examples</Link>
        </p>
      </footer>
    </div>
  );
}
