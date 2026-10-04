#!/usr/bin/env python3
"""Extract role prompts from TradingAgents agent files into Markdown (v3).

Fidelity rules (learned the hard way in v2):
- The collaboration preamble is NOT shared by all roles. Upstream, only the
  analyst nodes built on ChatPromptTemplate.from_messages use it, and the
  sentiment analyst uses a deliberately shortened variant with no tool-range
  wording (upstream comment: tool wording would invite a hallucinated tool
  call, see TA issue #1130). Researchers, risk debators, the trader, and the
  managers use plain f-string / messages-list prompts with no preamble.
- v3 therefore extracts each role's preamble FROM ITS OWN SOURCE, splitting
  the system template at "{system_message}". Roles without the template get
  a "not used" note instead of fabricated preamble text.

Usage:
    python3 extract_roles.py [--ta-src /path/to/TradingAgents] [--out DIR]

Handles all upstream patterns:
  system_message = <expr>
  prompt = <string expr>            (not ChatPromptTemplate / .partial chains)
  messages = [{role: system, content: ...}, {role: user, content: ...}]
TOOLS tuple extracted where present.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path

SHA = "1394a3f72aa4393e1a98f51b382434c4b4c2d972"

ROLES = [
    ("tradingagents/agents/analysts/fundamentals_analyst.py", "fundamentals-analyst.md", "Fundamentals Analyst"),
    ("tradingagents/agents/analysts/market_analyst.py", "technical-analyst.md", "Technical (Market) Analyst"),
    ("tradingagents/agents/analysts/news_analyst.py", "news-analyst.md", "News Analyst"),
    ("tradingagents/agents/analysts/sentiment_analyst.py", "sentiment-analyst.md", "Sentiment Analyst"),
    ("tradingagents/agents/researchers/bull_researcher.py", "bull-researcher.md", "Bull Researcher"),
    ("tradingagents/agents/researchers/bear_researcher.py", "bear-researcher.md", "Bear Researcher"),
    ("tradingagents/agents/risk_mgmt/aggressive_debator.py", "risk-debator-aggressive.md", "Risk Debator (Aggressive)"),
    ("tradingagents/agents/risk_mgmt/conservative_debator.py", "risk-debator-conservative.md", "Risk Debator (Conservative)"),
    ("tradingagents/agents/risk_mgmt/neutral_debator.py", "risk-debator-neutral.md", "Risk Debator (Neutral)"),
    ("tradingagents/agents/trader/trader.py", "trader.md", "Trader"),
    ("tradingagents/agents/managers/research_manager.py", "research-manager.md", "Research Manager"),
    ("tradingagents/agents/managers/portfolio_manager.py", "portfolio-manager.md", "Portfolio Manager"),
]

# Upstream source-comment captured for roles whose preamble is intentionally
# shortened (sentiment analyst). Preserved as an editor's note, not prompt text.
SENTIMENT_NOTE = (
    "_Editor's note: upstream this role uses a shortened preamble with no "
    "tool-range wording, because its data is pre-fetched into the prompt; the "
    "source comment reads: \"No tool-calling here: the data is pre-fetched "
    "into the prompt, so tool-range wording would only invite a hallucinated "
    "tool call (#1130).\"_"
)


def render(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return render(node.left) + render(node.right)
    if isinstance(node, ast.JoinedStr):
        out = []
        for v in node.values:
            if isinstance(v, ast.Constant):
                out.append(v.value)
            elif isinstance(v, ast.FormattedValue):
                out.append("{" + ast.unparse(v.value).strip() + "}")
        return "".join(out)
    if isinstance(node, ast.Call):
        return "{call:" + ast.unparse(node.func).strip() + "}"
    if isinstance(node, ast.Name):
        return "{" + node.id + "}"
    if isinstance(node, ast.Attribute):
        return "{" + ast.unparse(node).strip() + "}"
    return "{dynamic:" + ast.unparse(node).strip()[:60] + "}"


def is_string_expr(node):
    """True if the expression plausibly evaluates to prompt text."""
    if isinstance(node, (ast.Constant, ast.JoinedStr)):
        return True
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return is_string_expr(node.left) and is_string_expr(node.right)
    if isinstance(node, ast.Call):
        # Bare function calls (get_language_instruction(), _build_system_message())
        # are prompt builders. Attribute calls (ChatPromptTemplate.from_messages,
        # prompt.partial) are template machinery, not prompt text.
        return isinstance(node.func, ast.Name)
    return False


def extract_preamble(tree):
    """Return this role's own preamble text, or None if upstream has none.

    For ChatPromptTemplate.from_messages roles the system template is
    <preamble>{system_message}; the preamble is everything before that
    marker. This is per-role fidelity: v2 stamped one shared constant on all
    roles, which fabricated a tool-claiming preamble for 8 roles and used the
    wrong variant for the sentiment analyst.
    """
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
            continue
        if node.func.attr != "from_messages" or not node.args:
            continue
        arg = node.args[0]
        if not isinstance(arg, ast.List):
            continue
        for elt in arg.elts:
            if not (isinstance(elt, ast.Tuple) and len(elt.elts) == 2):
                continue
            k, v = elt.elts
            if isinstance(k, ast.Constant) and k.value == "system":
                text = render(v)
                if "{system_message}" in text:
                    return text.split("{system_message}", 1)[0].strip()
    return None


def extract(path):
    tree = ast.parse(path.read_text())
    doc = ast.get_docstring(tree) or ""
    preamble = extract_preamble(tree)
    tools = []
    prompts = {}  # label -> text
    builders = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_build_system_message":
            for sub in ast.walk(node):
                if isinstance(sub, ast.Return) and sub.value is not None:
                    builders[node.name] = render(sub.value)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "TOOLS" in names:
            elts = node.value.elts if isinstance(node.value, (ast.Tuple, ast.List)) else []
            tools = [ast.unparse(e).strip() for e in elts]
        if "system_message" in names and is_string_expr(node.value):
            v = node.value
            if isinstance(v, ast.Call):
                prompts["system"] = builders.get("_build_system_message", "{_build_system_message(...)}")
            else:
                prompts["system"] = render(v)
        if "prompt" in names and is_string_expr(node.value) and "system" not in prompts:
            prompts["system"] = render(node.value)
        if "messages" in names and isinstance(node.value, ast.List):
            for elt in node.value.elts:
                if not isinstance(elt, ast.Dict):
                    continue
                kv = {}
                for k, val in zip(elt.keys, elt.values):
                    if isinstance(k, ast.Constant):
                        kv[k.value] = val
                role = kv.get("role")
                role_s = role.value if isinstance(role, ast.Constant) else None
                if role_s in ("system", "user") and "content" in kv:
                    prompts[role_s] = render(kv["content"])
    return doc, preamble, tools, prompts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ta-src", default="/tmp/ta")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    TA = Path(args.ta_src)
    OUT = Path(args.out) if args.out else Path(__file__).resolve().parent / "agents"
    OUT.mkdir(parents=True, exist_ok=True)

    for rel, outname, title in ROLES:
        doc, preamble, tools, prompts = extract(TA / rel)
        md = [f"# {title}", "",
              f"> Extracted verbatim from `TauricResearch/TradingAgents` commit `{SHA}`,",
              f"> file `{rel}`. Runtime interpolations shown as `{{placeholders}}`.",
              "> LangGraph node wiring, tool-call loop, and structured-output",
              "> plumbing are deliberately NOT included — domain content only.", ""]
        if doc:
            md += ["## Module notes (upstream docstring)", "", doc.strip(), ""]
        if preamble is not None:
            md += ["## Collaboration preamble (this role's own, from its source)", "",
                   preamble, ""]
            if "sentiment_analyst" in rel:
                md += [SENTIMENT_NOTE, ""]
        else:
            md += ["## Preamble",
                   "",
                   "_Not used — upstream this role's prompt contains no shared "
                   "collaboration preamble; the prompt below is the complete "
                   "prompt text as written._",
                   ""]
        if "system" in prompts:
            md += ["## System prompt", "", prompts["system"].strip(), ""]
        if "user" in prompts:
            md += ["## User-message template", "", prompts["user"].strip(), ""]
        if not prompts:
            md += ["_No prompt text found — check upstream file._", ""]
        md += ["## Tools offered to this role", ""]
        for t in tools:
            md += [f"- `{t}`"]
        if not tools:
            md += ["- _(none — data pre-fetched into the prompt or decided by other roles)_"]
        md += [""]
        (OUT / outname).write_text("\n".join(md))
        print("wrote", outname, "| preamble:", "yes" if preamble else "no",
              "| tools:", len(tools),
              "| sys:", len(prompts.get("system", "")),
              "| usr:", len(prompts.get("user", "")))


if __name__ == "__main__":
    main()
