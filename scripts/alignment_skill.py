"""Decide whether a published item is the same skill as a generated question.

A hit on one generic word (fraction, number, equation, problem, with, and)
is not enough. The item has to share a distinctive word with the topic or
the generated stems, or the same expression shape (a quotient, an absolute
value equation, a trinomial to factor). Spiral review, "Be Prepared",
applications, and a neighboring heading stay out.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Filename and type-id debris. Not a skill word.
NOISE = {
    "pdf", "png", "jpg", "svg",
    "hsg", "hsa", "hsf", "hss", "hsn", "hsm",
    "geo", "calc", "app", "alg",
    "cong", "overline", "mathrm", "mathit", "operatorname",
}

# Words that never identify a skill, even in a pair.
GENERIC_NEVER = {
    "fraction", "fractions", "fractional",
    "number", "numbers",
    "equation", "equations",
    "problem", "problems",
    "value", "values",
    "expression", "expressions",
    "variable", "variables",
    "integer", "integers",
    "function", "functions",
    "answer", "answers",
    "question", "questions",
    "quantity", "quantities",
    "unknown", "given",
    "using", "use", "used",
    "find", "finding", "write", "writing", "solve", "solving",
    "simplify", "simplifying", "calculate", "calculating",
    "compute", "determine", "evaluate", "evaluating",
    "show", "explain", "explanation", "reasoning", "following", "consider",
    "select", "choose", "true", "false", "correct",
    "practice", "exercise", "example", "review", "section", "chapter", "lesson",
    "student", "students", "math", "mathematics", "algebra", "algebraic",
    "introduction", "basic", "simple", "general", "other", "multi", "step", "steps",
    "word", "words", "real", "world",
    "the", "and", "for", "from", "with", "that", "this", "these", "those", "your", "you",
    "off", "own", "long", "short", "large", "small", "because", "while", "still",
    "take", "takes", "took", "give", "going", "come", "comes", "back", "down", "away",
    "are", "was", "were", "have", "has", "had", "not", "but", "its", "into", "over",
    "under", "than", "then", "also", "only", "all", "each", "any", "some", "such",
    "about", "after", "before", "between", "through", "during", "without", "within",
    "per", "their", "they", "them", "can", "will", "just", "like", "make", "made",
    "does", "did", "both", "same", "much", "many", "out", "how", "what", "which",
    "when", "where", "who", "why", "let", "may", "one", "two", "three", "four",
    "first", "second", "third", "next", "last", "above", "below", "left", "right",
    "onto", "via", "been", "being", "would", "could", "should",
    "more", "most", "less", "least", "very", "here", "there",
    "task", "content", "standard", "standards", "alignment", "alignments",
    "illustrative", "openstax", "text", "mathrm", "textbf", "boldcdot",
    "frac", "left", "right", "begin", "end", "cdot", "quad",
}

# One of these is not enough. Two, or one plus a specific word, can be.
GENERIC_ALONE = {
    "angle", "triangle", "circle", "line", "segment", "point", "side", "length",
    "area", "graph", "measure", "set", "data", "unit", "part", "group", "system",
    "term", "model", "shape", "figure", "diagram", "square", "polygon", "relation",
    "linear", "rule", "factor", "operation", "formula", "property",
    "positive", "negative", "total", "amount", "time", "table",
    "plane", "degree", "mile", "hour", "speed", "minute",
    "width", "base", "height",
}

# Map variants onto one token. The canonical word is the first entry.
_CANON_GROUPS = [
    ("rectangle", ("rectangular", "rectangles")),
    ("hanger", ("balance", "balances", "balanced")),
    ("divide", ("divides", "dividing", "division", "quotient", "quotients", "div")),
    ("multiply", ("multiplies", "multiplying", "multiplication")),
    ("add", ("adding", "addition", "sum", "sums")),
    ("subtract", ("subtracting", "subtraction", "difference", "differences")),
    ("percent", ("percents", "percentage", "percentages")),
    ("exponent", ("exponents", "exponential")),
    ("logarithm", ("logarithms", "log", "ln")),
    ("derivative", ("derivatives", "differentiate", "differentiating", "differentiation")),
    ("integral", ("integrals", "integrate", "integrating", "integration", "antiderivative", "antiderivatives")),
    ("congruent", ("congruence")),
    ("similar", ("similarity")),
    ("pythagorean", ("pythagoras",)),
    ("histogram", ("histograms",)),
    ("triangle", ("triangles", "triangular")),
    ("circle", ("circles", "circular")),
    ("inequality", ("inequalities", "inequal")),
    ("decimal", ("decimals",)),
    ("coordinate", ("coordinates",)),
    ("probability", ("probabilities",)),
    ("matrix", ("matrices",)),
    ("sequence", ("sequences",)),
    ("vector", ("vectors",)),
    ("polynomial", ("polynomials",)),
    ("quadratic", ("quadratics",)),
    ("parabola", ("parabolas",)),
    ("ratio", ("ratios", "proportion", "proportions")),
    ("slope", ("slopes",)),
    ("graph", ("graphs", "graphing", "sketch", "sketching", "plot", "plotting")),
    ("area", ("areas",)),
    ("volume", ("volumes",)),
    ("median", ("medians",)),
    ("concavity", ("concave", "concavities", "inflection")),
    ("extremum", ("extrema", "extreme", "maximum", "minimum", "maxima", "minima")),
    ("trinomial", ("trinomials",)),
    ("binomial", ("binomials",)),
    ("radius", ("radii",)),
    ("diameter", ("diameters",)),
    ("asymptote", ("asymptotes",)),
    ("permutation", ("permutations",)),
    ("combination", ("combinations",)),
]

CANON = {}
for canon, variants in _CANON_GROUPS:
    CANON[canon] = canon
    for variant in variants:
        CANON[variant] = canon

# Section title wording that does not share the topic's word.
SOURCE_HINTS = {
    "concavity": ("shape of a graph", "concav"),
    "extremum": ("maxima and minima", "maxima", "minima"),
    "related_rate": ("related rate",),
    "mean_value": ("mean value",),
    "absolute_value": ("absolute value",),
    "chain_rule": ("chain rule",),
    "product_rule": ("product rule", "differentiation rule"),
    "quotient_rule": ("quotient rule", "differentiation rule"),
    "power_rule": ("power rule", "differentiation rule"),
}

# A published item that says one of these, when the skill does not, is a different task.
ALIEN_WORDS = (
    "hose", "gallon", "histogram", "hypotenuse", "ellipse", "hyperbola",
    "logarithm", "probability", "determinant", "permutation", "factorial",
    "surface", "volume", "prism", "cylinder", "pyramid", "sphere", "cone",
)

REJECT_HEAD = re.compile(
    r"be prepared|writing exercise|self[- ]check|key concept|key term|"
    r"everyday|review exercise|chapter review|practice test|"
    r"^verbal$|verbal exercise",
    re.I,
)
APP_HEAD = re.compile(r"application|everyday|real[- ]world", re.I)
USEFUL_HEAD = re.compile(
    r"practice makes perfect|try it\b|exercises?$|checkpoint|example\b|"
    r"^section \d|algebraic|graphical|technology|numeric|graphical",
    re.I,
)
EXPLAIN_HEAD = re.compile(r"verbal|writing exercise", re.I)
EXPLAIN_START = re.compile(
    r"^(what is the difference|explain\b|in your own words|why do you|"
    r"how do you\b|how can you tell|describe\b|give an example)",
    re.I,
)

RARE_FEATURES = {
    "abs", "log", "trig", "integral", "limit", "matrix", "histogram",
    "congruent", "pythag", "div",
}


@dataclass
class SkillProfile:
    tokens: set[str] = field(default_factory=set)
    specific: set[str] = field(default_factory=set)
    phrases: set[str] = field(default_factory=set)
    features: set[str] = field(default_factory=set)
    required: set[str] = field(default_factory=set)
    task: str = ""
    word_problem: bool = False
    wants_ineq: bool = False
    allow_deg2: bool = False
    allow_higher: bool = False
    generated_text: str = ""
    anchor: set[str] = field(default_factory=set)


def phrase_source(text: str) -> str:
    t = (text or "").lower().replace("_", " ").replace("-", " ")
    t = t.replace("\\", " ")
    t = re.sub(r"\s+", " ", t)
    return t


def phrase_tokens(text: str) -> set[str]:
    low = phrase_source(text)
    found: set[str] = set()
    if "absolute value" in low:
        found.add("absolute_value")
    elif re.search(r"\bextrema\b|\bextremum\b", low) or (
        "absolute" in low and re.search(r"\b(max|min)", low)
    ):
        found.add("extremum")
    if re.search(r"\b(maxima|minima|maximum|minimum)\b", low) and "absolute_value" not in found:
        found.add("extremum")
    if "mean value" in low:
        found.add("mean_value")
    if "related rate" in low:
        found.add("related_rate")
    if "chain rule" in low:
        found.add("chain_rule")
    if "product rule" in low:
        found.add("product_rule")
    if "quotient rule" in low:
        found.add("quotient_rule")
    if "power rule" in low:
        found.add("power_rule")
    if "dot plot" in low:
        found.add("dot_plot")
    if "box plot" in low:
        found.add("box_plot")
    if "number line" in low:
        found.add("number_line")
    if "tape diagram" in low:
        found.add("tape")
    if re.search(r"\b(unit rate|constant rate|miles per|per hour|kilometer per)\b", low):
        found.add("rate")
    if "rate of change" in low and "related_rate" not in found:
        found.add("rate_of_change")
    return found


def norm_word(word: str) -> str:
    if word in CANON:
        return CANON[word]
    if len(word) > 5 and word.endswith("ies"):
        word = word[:-3] + "y"
    elif len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
        word = word[:-1]
    return CANON.get(word, word)


def plain_words(text: str) -> str:
    t = text or ""
    t = t.replace("\\", " ")
    t = re.sub(r"[{}_^$|]", " ", t)
    t = re.sub(
        r"\b(frac|left|right|text|mathrm|textbf|displaystyle|begin|end|cdot|times|quad|hspace|boldcdot)\b",
        " ",
        t,
        flags=re.I,
    )
    return t


def content_tokens(text: str) -> set[str]:
    found = set(phrase_tokens(text))
    raw = plain_words(text).lower()
    raw = re.sub(r"[^a-z0-9 ]", " ", raw)
    # Drop the loose word "absolute" / "value" once the phrase is recorded,
    # so absolute extrema does not match an absolute-value section.
    blocked = set()
    if "absolute_value" in found:
        blocked.update({"absolute", "value"})
    if "extremum" in found:
        blocked.update({"absolute", "extreme", "extrema", "maximum", "minimum", "maxima", "minima"})
    if "related_rate" in found:
        blocked.update({"related", "rate", "rates"})
    if "mean_value" in found:
        blocked.add("mean")
    for part in raw.split():
        if part.isdigit() or len(part) <= 2 or part in blocked:
            continue
        word = norm_word(part)
        if word in GENERIC_NEVER or word in NOISE or word in blocked:
            continue
        found.add(word)
    return found


def has_ineq(text: str) -> bool:
    t = re.sub(r"\\left|\\right|\\langle|\\rangle|\\lvert|\\rvert|\\vert\b|\\mid\b", "", text or "")
    return re.search(r"<|>|\\leq|\\geq|\\le(?![a-zA-Z])|\\ge(?![a-zA-Z])|≤|≥", t) is not None


def has_eq(text: str) -> bool:
    t = re.sub(r"\\neq|\\ne\b|\\nleq|\\ngeq|≠", "", text or "")
    return "=" in t


def has_abs(text: str) -> bool:
    t = text or ""
    if re.search(r"\\left\s*\|", t) or re.search(r"\\lvert|\\rvert", t):
        return True
    if re.search(r"absolute value", t, re.I):
        return True
    return re.search(r"(?<!\\)\|", t) is not None


def has_deg2(text: str) -> bool:
    return re.search(r"\^\s*\{?\s*2|²", text or "") is not None


def has_deg3plus(text: str) -> bool:
    return re.search(r"\^\s*\{?\s*[3-9]", text or "") is not None


def expression_shapes(text: str) -> set[str]:
    """Expression shape, ignoring the d/dx operator itself."""
    t = text or ""
    shapes: set[str] = set()
    for num, den in re.findall(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", t):
        if re.fullmatch(r"\s*d\s*", num) and re.search(r"d", den):
            continue
        if re.search(r"[a-zA-Z]", num) and re.search(r"[a-zA-Z0-9]", den):
            shapes.add("quotient")
    if re.search(r"\\right\)\s*\\left\(|\)\s*\(", t):
        shapes.add("product")
    if re.search(r"f\s*\(\s*x\s*\)\s*g\s*\(|f\\left\(x\\right\)\s*g", t):
        shapes.add("product")
    if re.search(r"(?<![A-Za-z\\])[xt0-9]\s*\\left\(", t):
        shapes.add("product")
    if re.search(r"\\right\)\s*\^|\)\s*\^", t):
        shapes.add("chain")
    if re.search(r"\\sqrt\s*\{|\\sin|\\cos|\\tan|\\sec|\\csc|\\cot|\\ln|\\log|\\exp|(?<![A-Za-z])e\s*\^", t):
        shapes.add("chain")
    if re.search(r"\bu\s*=", t) and re.search(r"\by\s*=", t):
        shapes.add("chain")
    if has_deg2(t) or has_deg3plus(t):
        shapes.add("power")
        shapes.add("poly")
    if has_abs(t):
        shapes.add("abs")
    if has_ineq(t):
        shapes.add("ineq")
    if has_eq(t):
        shapes.add("eqn")
    return shapes


def math_features(text: str) -> set[str]:
    t = text or ""
    low = t.lower()
    feats: set[str] = set()
    shapes = expression_shapes(t)
    if "abs" in shapes or has_abs(t):
        feats.add("abs")
    if "ineq" in shapes:
        feats.add("ineq")
    if "eqn" in shapes:
        feats.add("eqn")
    if re.search(r"\\div|÷", t) or re.search(r"\b(divis|divid|quotient)", low):
        feats.add("div")
    if re.search(r"\\log|\\ln|\blog\b|\bln\b", low):
        feats.add("log")
    if re.search(r"\\sin|\\cos|\\tan|\bsin\b|\bcos\b|\btan\b", low):
        feats.add("trig")
    if re.search(r"\\int|\bintegrat|\bantideriv", low):
        feats.add("integral")
    if re.search(r"\bderiv|\\frac\s*\{\s*d", low):
        feats.add("deriv")
    if re.search(r"\\lim|\blimit\b", low):
        feats.add("limit")
    if re.search(r"matrix|determinant", low):
        feats.add("matrix")
    if re.search(r"histogram", low):
        feats.add("histogram")
    if re.search(r"congruent", low):
        feats.add("congruent")
    if re.search(r"pythag|hypotenuse", low):
        feats.add("pythag")
    if "poly" in shapes:
        feats.add("poly")
    if has_deg2(t):
        feats.add("deg2")
    if "quotient" in shapes:
        feats.add("quotient")
    if "product" in shapes:
        feats.add("product")
    if "chain" in shapes:
        feats.add("chain")
    return feats


def _generated_text(generated: dict | None) -> str:
    parts = []
    for sample in (generated or {}).get("samples") or []:
        if sample.get("error"):
            continue
        instr = sample.get("instruction_latex") or ""
        prompt = sample.get("prompt_latex") or sample.get("prompt_text") or ""
        parts.append(f"{instr} {prompt}")
    return "\n".join(parts)


def _is_word_problem(topic: dict, generated_text: str) -> bool:
    name = f"{topic.get('name', '')} {topic.get('type_id', '')}"
    if re.search(r"word", name, re.I):
        return True
    return re.search(
        r"\b(father|son|daughter|coin|quarter|dime|nickel|ticket|mixture|"
        r"years old|pounds of|miles per hour)\b",
        generated_text,
        re.I,
    ) is not None


def _required_shapes(topic: dict, generated_text: str, word_problem: bool) -> set[str]:
    name = f"{topic.get('name', '')} {topic.get('type_id', '')}".lower()
    if word_problem:
        return set()
    req: set[str] = set()
    if re.search(r"quotient", name):
        req.add("quotient")
    elif re.search(r"product_rule|product rule", name):
        req.add("product")
    elif re.search(r"chain", name):
        req.add("chain")
    elif re.search(r"power_rule|power rule", name):
        req.add("plain_power")
    elif "absolute value" in name and re.search(r"inequal", name):
        req.add("abs_ineq")
    elif "absolute value" in name and re.search(r"equation|equal", name) and "graph" not in name:
        req.add("abs_eqn")
    elif re.search(r"\bgraph", name):
        req.add("graph_rel")
    elif (
        re.search(r"factor", name)
        and not re.search(r"gcf|common factor|prime", name)
        and (has_deg2(generated_text) or has_deg3plus(generated_text) or re.search(r"quadratic|trinomial|polynomial", name))
    ):
        req.add("factor_eqn" if re.search(r"solv", name) else "factor_poly")
    elif "related rate" in name:
        req.add("related_rate")
    elif re.search(r"inequal", name):
        req.add("ineq")
    elif (
        re.search(r"equation", name)
        and not re.search(r"hanger|tape|diagram|word|graph|ratio|percent|rate", name)
        and has_eq(generated_text)
        and not re.search(r"\by\s*=", generated_text)
    ):
        req.add("solve_eqn")
    return req


def skill_profile(topic: dict, generated: dict | None) -> SkillProfile:
    generated_text = _generated_text(generated)
    blob = f"{topic.get('name', '')} {topic.get('type_id', '')} {generated_text}"
    tokens = content_tokens(blob)
    phrases = phrase_tokens(blob)
    tokens |= phrases
    specific = {tok for tok in tokens if tok not in GENERIC_ALONE}
    # Words from the topic name and the easy stems. A hard stem can mention a
    # different method (hypotenuse-leg); that word must not pull in another skill.
    easy_text = " ".join(
        f"{sample.get('instruction_latex') or ''} {sample.get('prompt_latex') or sample.get('prompt_text') or ''}"
        for sample in (generated or {}).get("samples") or []
        if not sample.get("error") and sample.get("tier", "easy") == "easy"
    )
    anchor = {
        tok
        for tok in content_tokens(f"{topic.get('name', '')} {topic.get('type_id', '')} {easy_text}")
        if tok not in GENERIC_ALONE
    }
    word_problem = _is_word_problem(topic, generated_text)
    name = f"{topic.get('name', '')} {topic.get('type_id', '')}".lower()
    wants_ineq = bool(re.search(r"inequal", name)) or (
        has_ineq(generated_text) and "absolute_value" not in phrases and not re.search(r"absolute value", name)
    )
    if re.search(r"inequal", name):
        wants_ineq = True
    required = _required_shapes(topic, generated_text, word_problem)
    task = ""
    if "graph_rel" in required or re.search(r"\bgraph", name):
        task = "graph"
    elif "factor_poly" in required or "factor_eqn" in required:
        task = "factor"
    elif re.search(r"\bsimplif", name):
        task = "simplify"
    elif re.search(r"equation|solve", name) and not word_problem:
        task = "solve"
    return SkillProfile(
        tokens=tokens,
        specific=specific,
        phrases=phrases,
        features=math_features(generated_text),
        required=required,
        task=task,
        word_problem=word_problem,
        wants_ineq=wants_ineq,
        allow_deg2=has_deg2(generated_text) or bool(re.search(r"quadratic|parabola|polynomial", name)),
        allow_higher=has_deg3plus(generated_text) or "polynomial" in name,
        generated_text=generated_text,
        anchor=anchor,
    )


def heading_is_useful(heading: str) -> bool:
    heading = (heading or "").strip()
    if not heading or USEFUL_HEAD.search(heading):
        return False
    if len(heading) < 8:
        return False
    return True


def heading_rejected(heading: str, profile: SkillProfile) -> bool:
    heading = heading or ""
    if not heading:
        return False
    if REJECT_HEAD.search(heading):
        return True
    if APP_HEAD.search(heading) and not profile.word_problem:
        return True
    return False


def is_explain_prompt(text: str, heading: str) -> bool:
    if EXPLAIN_HEAD.search(heading or ""):
        return True
    lead = re.sub(r"^\s*\d+\s*[.)]\s*", "", (text or "").strip())
    if EXPLAIN_START.search(lead):
        return True
    return re.search(
        r"\b(why do you|why does one|explain whether|in your own words|what is the difference between)\b",
        text or "",
        re.I,
    ) is not None


def alien_conflict(text: str, profile: SkillProfile) -> bool:
    low = phrase_source(text)
    have = profile.tokens | profile.specific | profile.phrases
    for word in ALIEN_WORDS:
        if re.search(rf"\b{word}\b", low) and word not in have and CANON.get(word, word) not in have:
            return True
    return False


def contradicts(text: str, profile: SkillProfile) -> bool:
    ineq = has_ineq(text)
    if profile.wants_ineq and "graph_rel" not in profile.required:
        return False
    if ineq and not profile.wants_ineq and "abs_ineq" not in profile.required and "ineq" not in profile.required:
        # A solved inequality is not an equation-solving or graphing-equation item.
        if "solve_eqn" in profile.required or "abs_eqn" in profile.required or "graph_rel" in profile.required or "factor_poly" in profile.required:
            return True
    if "graph_rel" in profile.required:
        if re.search(r"\b(solve|factor|simplify)\b", text or "", re.I) and not re.search(r"\b(graph|sketch|plot)\b", text or "", re.I) and not re.search(r"\by\s*=", text or ""):
            return True
    if "solve_eqn" in profile.required or "abs_eqn" in profile.required:
        if re.search(r"\bgraph (the )?(equation|function|line|parabola|curve)\b", text or "", re.I):
            return True
    return False


def lexical_score(text: str, profile: SkillProfile) -> int:
    shared = content_tokens(text) & profile.tokens
    specific = {tok for tok in shared if tok not in GENERIC_ALONE and tok not in ACTOR}
    generic = shared & GENERIC_ALONE
    return 4 * len(specific) + 2 * len(generic)


def low_prose(text: str) -> bool:
    return len(content_tokens(text)) <= 7


def conflicting_feature(text: str, profile: SkillProfile) -> bool:
    """A fraction lesson's spiral division problem is not rectangle area."""
    feats = math_features(text) & {
        "div", "log", "trig", "integral", "limit", "matrix", "histogram",
        "abs", "congruent", "pythag",
    }
    return bool(feats - profile.features)


def other_task_sentence(text: str) -> bool:
    """Rate and 'how many groups' prompts. 'How many tiles' can still be area."""
    return re.search(
        r"\b(at this rate|at that rate|how long (?:does|will|would)|how many groups|what fraction of)\b",
        text or "",
        re.I,
    ) is not None


def _graph_rel(text: str, profile: SkillProfile) -> bool:
    if has_ineq(text):
        return False
    deg2 = has_deg2(text)
    higher = has_deg3plus(text)
    if not profile.allow_deg2 and (deg2 or higher):
        return False
    if (profile.allow_deg2 or profile.allow_higher) and not deg2 and not higher:
        if not re.search(r"polynomial|quadratic|parabola|cubic|quartic", text or "", re.I):
            return False
    if re.search(r"\b(graph|sketch|plot)\b", text or "", re.I):
        return True
    if re.search(r"\by\s*=", text or ""):
        return True
    # f(x) = ... is the relation to graph when the section does not repeat the verb.
    return re.search(r"\b[a-zA-Z]\s*(?:\\left)?\s*\(\s*x\s*\)\s*=", text or "") is not None


def _solve_eqn(text: str) -> bool:
    if not has_eq(text) or has_ineq(text):
        return False
    if re.search(r"\by\s*=", text or "") and not re.search(r"\bsolve\b", text or "", re.I):
        return False
    stripped = re.sub(r"\\[a-zA-Z]+", " ", text or "")
    return re.search(r"[a-zA-Z]", stripped) is not None


def _related_rate(text: str) -> bool:
    if re.search(r"related rate", text or "", re.I):
        return True
    if re.search(r"d\s*[xy]|\\frac\s*\{\s*d", text or "") and re.search(r"d\s*t", text or ""):
        return True
    return bool(
        re.search(r"\brate\b", text or "", re.I)
        and re.search(r"\b(fast|increasing|decreasing|shrinking|changing|speed|when)\b", text or "", re.I)
    )


def shape_satisfied(text: str, profile: SkillProfile) -> bool:
    shapes = expression_shapes(text)
    req = profile.required
    if "quotient" in req:
        return "quotient" in shapes
    if "product" in req:
        return "product" in shapes and "quotient" not in shapes
    if "chain" in req:
        return "chain" in shapes
    if "plain_power" in req:
        return "power" in shapes and not ({"chain", "product", "quotient"} & shapes)
    if "factor_poly" in req:
        if "poly" not in shapes:
            return False
        if has_eq(text) and not re.search(r"\bfactor", text or "", re.I):
            return False
        return True
    if "factor_eqn" in req:
        return "poly" in shapes and has_eq(text)
    if "abs_eqn" in req:
        return has_abs(text) and has_eq(text) and not has_ineq(text)
    if "abs_ineq" in req:
        return has_abs(text) and has_ineq(text)
    if "ineq" in req:
        return has_ineq(text)
    if "graph_rel" in req:
        return _graph_rel(text, profile)
    if "solve_eqn" in req:
        return _solve_eqn(text)
    if "related_rate" in req:
        return _related_rate(text)
    return False


def source_is_on_skill(source_text: str, profile: SkillProfile) -> bool:
    if not source_text:
        return False
    tokens = content_tokens(source_text)
    if tokens & profile.specific:
        return True
    if len((tokens & profile.tokens) & GENERIC_ALONE) >= 2:
        return True
    low = phrase_source(source_text)
    for token in list(profile.specific) + list(profile.phrases):
        for hint in SOURCE_HINTS.get(token, ()):
            if hint in low:
                return True
    if profile.task == "factor" and re.search(r"\bfactor", low):
        return True
    if profile.task == "graph" and re.search(r"\bgraph", low):
        return True
    return False


def item_matches(
    text: str,
    profile: SkillProfile,
    *,
    heading: str = "",
    source_text: str = "",
    alt: str = "",
) -> bool:
    """True when this published stem is the same skill as the profile."""
    if heading_rejected(heading, profile):
        return False
    blob = f"{text or ''} {alt or ''}".strip()
    if is_explain_prompt(blob, heading):
        return False
    # "At this rate, how long" is a rate problem even when a fraction shows up in it.
    if other_task_sentence(blob) and "rate" not in profile.tokens and "related_rate" not in profile.phrases and "rate_of_change" not in profile.phrases:
        return False
    if heading_is_useful(heading):
        blob = f"{blob} {heading}"
    if contradicts(blob, profile) or alien_conflict(blob, profile):
        return False
    if profile.required:
        if shape_satisfied(blob, profile):
            return True
        # The stem names the rule ("use the chain rule") even when the
        # expression shape is written out in words.
        if profile.phrases & content_tokens(blob):
            return True
        return False
    shared_rare = math_features(blob) & profile.features & RARE_FEATURES
    if shared_rare and not alien_conflict(blob, profile):
        return True
    if lexical_score(blob, profile) >= 4:
        return True
    # A bare exercise in a section that is this skill (OpenStax often prints
    # only the expression). A short fraction or a different operation does not
    # qualify just because the section title matched.
    if (
        not profile.word_problem
        and source_is_on_skill(source_text, profile)
        and low_prose(blob)
        and not other_task_sentence(blob)
        and not conflicting_feature(blob, profile)
        and re.search(
            r"\^|=|\\frac|\\int|\\log|\\sin|\\cos|\\tan|\+|\\cdot|\\times|[a-zA-Z]\s*\(|\d\s*[-−]\s*\d",
            blob or "",
        )
    ):
        return True
    return False


# A person in the stem is not the skill. "Your Father" is not an age problem.
ACTOR = {
    "father", "mother", "son", "daughter", "brother", "sister", "parent",
    "child", "boy", "girl", "man", "woman", "person", "people", "teacher",
    "taylor", "julian", "bobbie", "alexis", "priya", "han", "noah",
}

# Shared with lots of unrelated tasks. Not enough when the topic also has a narrower word.
BROAD_SPECIFIC = {
    "derivative", "integral", "limit", "add", "subtract", "multiply", "divide",
    "theorem", "function",
}


def _only_broad(overlap: set[str], profile: SkillProfile) -> bool:
    narrow = {tok for tok in profile.specific if tok not in BROAD_SPECIFIC}
    return bool(narrow) and bool(overlap) and not (overlap & narrow)


def filename_score(name: str, profile: SkillProfile) -> float:
    """Score an IM task filename. A single generic word scores 0."""
    tokens = content_tokens(name)
    specific = {tok for tok in (tokens & profile.specific) if tok not in ACTOR}
    generic = (tokens & profile.tokens) & GENERIC_ALONE
    file_specific = {tok for tok in tokens if tok not in GENERIC_ALONE}
    alien = file_specific - profile.tokens
    if alien and len(specific) <= len(alien):
        return 0.0
    if profile.anchor and not (specific & profile.anchor):
        return 0.0
    if _only_broad(specific, profile):
        return 0.0
    if specific:
        return 4.0 * len(specific) + 1.5 * len(generic)
    if len(generic) >= 2 and not _only_broad(generic, profile):
        return 1.5 * len(generic)
    return 0.0


def section_slug_score(slug: str, profile: SkillProfile, *, book_rank: int = 0) -> float:
    """Score an OpenStax slug. Generic overlap alone is not a match."""
    if re.search(r"introduction|key-terms|key-concepts|key-equations|review-exercises|answer-key", slug or ""):
        return 0.0
    tokens = content_tokens(slug.replace("-", " "))
    specific = tokens & profile.specific
    generic = (tokens & profile.tokens) & GENERIC_ALONE
    # "derivative" or "integral" alone matches every section in the chapter.
    # A topic that also names a rule or a theorem has to share that narrower word.
    broad = {"derivative", "integral", "limit", "function", "add", "subtract", "multiply", "divide"}
    narrow = {tok for tok in profile.specific if tok not in broad}
    if specific and narrow and not (narrow & tokens) and specific <= broad:
        return 0.0
    # A section about a different relation type is not a match on a shared modifier.
    if profile.specific and not specific and len(generic) < 2:
        return 0.0
    if not specific and len(generic) < 2:
        return 0.0
    # When the topic has two or more specific tokens, a section that shares only
    # a modifier (absolute, but not extremum) is a different skill.
    topic_specific = set(profile.specific)
    if len(topic_specific) >= 2 and not topic_specific <= tokens:
        longest = max(topic_specific, key=len)
        if longest not in tokens and len(specific) < 2:
            return 0.0
    score = 4.0 * len(specific) + 1.6 * len(generic)
    if book_rank == 0:
        score += 0.4
    elif book_rank >= 2:
        score -= 0.3
    return score
