"""Approved report data -> one complete, local, fixed-A4 HTML report.

Authority: docs/governing/PHASE_1_REPORT_RENDERER_CONTRACT.md. The renderer
- reads only the approved ``report_data`` dict, never the case file, captures or trace;
- takes its visual source (CSS, icons, logo, illustration) from the vendored templates in
  ``templates/report/`` at render time, so the approved design is not copied into code;
- writes only founder-approved text, the template's fixed copy and the contract's fixed wording;
- makes no recommendation and invents no prose. Where the contract gives no treatment it refuses
  with RenderError instead of guessing.

It is called only by ``workflow.run_build`` after every approval, fingerprint and Review gate passes.
"""

from __future__ import annotations

import base64
import datetime as dt
import html
import re
from decimal import Decimal
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "report"

# Page type -> approved template pages whose CSS styles it.
PAGE_CSS = {
    "cover": ["billvisor-report-page-1.html"],
    "overview": ["billvisor-report-page-2.html"],
    "priorities": ["billvisor-report-page-3.html"],
    # Scored service pages use page 4's rules; the limitations variant adds the status and
    # Confirm-information rules. No selector is defined differently in the two files.
    "service": ["billvisor-report-page-4.html", "billvisor-report-service-analysed-with-limitations.html"],
    "plan": ["billvisor-report-page-7.html"],
}

BAND_CLASS = {"Good": "good", "Medium": "medium", "Poor": "poor"}
BAND_VAR = {"Good": "var(--green)", "Medium": "var(--amber)", "Poor": "var(--red)"}

# Renderer contract section 8.
CODE_TEXT = {
    "out_of_contract": "Out of contract",
    "unknown": "No end date known",
    "no_end_date": "No end date known",
    "sim_only": "SIM only",
    "handset_included": "Handset included",
}
SERVICES_TEXT = {"both": "Gas and electricity", "gas": "Gas", "electricity": "Electricity"}

# Renderer contract section 4 (fixed Energy sentence).
ENERGY_SENTENCE = ("This uses your current tariff and the annual energy-use figure available for your home. "
                   "Your monthly payments may vary through the year.")

UNIT_TEXT = {
    # unit_id: (page title, current-service heading, page icon, overview icon)
    "broadband": ("Broadband Analysis", "Your broadband", "icon-wifi", "icon-wifi"),
    "mobile": ("Mobile Analysis", "Your mobile plan", "icon-mobile", "icon-mobile"),
    "energy_combined": ("Energy Analysis", "Your gas and electricity", "icon-electricity", "icon-energy"),
    "electricity": ("Electricity Analysis", "Your electricity", "icon-electricity", "icon-energy"),
    "gas": ("Gas Analysis", "Your gas", "icon-gas", "icon-gas"),
}
ENERGY_UNITS = {"energy_combined", "electricity", "gas"}


class RenderError(Exception):
    """The approved data cannot be rendered under the renderer contract."""


# ---------------------------------------------------------------- formatting

def e(value) -> str:
    return html.escape(str(value), quote=True)


def money_whole(n: int) -> str:
    return f"£{n:,}"


def money_2dp(d: Decimal) -> str:
    return f"£{Decimal(d).quantize(Decimal('0.01')):,}"


def end_text(value) -> str:
    if value in CODE_TEXT:
        return CODE_TEXT[value]
    try:
        d = dt.date.fromisoformat(str(value))
    except ValueError:
        raise RenderError(f"no display rule for contract/tariff end value {value!r}") from None
    return f"{d.day} {d.strftime('%B %Y')}"


def number_text(value) -> str:
    d = Decimal(str(value))
    return f"{d.normalize():f}"


# ---------------------------------------------------------------- template assets

def _read(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def _data_uri(name: str, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode((TEMPLATE_DIR / name).read_bytes()).decode("ascii")


def _page_css(name: str) -> str:
    m = re.search(r"<style>(.*?)</style>", _read(name), re.S)
    if not m:
        raise RenderError(f"{name}: no <style> block")
    return m.group(1)


def _icon_symbols() -> str:
    """Every <symbol> used by the approved pages, once (ids are identical across pages)."""
    symbols: dict[str, str] = {}
    for f in sorted(TEMPLATE_DIR.glob("*.html")):
        for m in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', f.read_text(encoding="utf-8"), re.S):
            if symbols.setdefault(m.group(1), m.group(0)) != m.group(0):
                raise RenderError(f"icon {m.group(1)} is defined differently in {f.name}")
    return "".join(symbols.values())


# ---------------------------------------------------------------- CSS scoping

_DOCUMENT_SELECTORS = {"html", "body", "*", ":root"}


def _blocks(css: str):
    """Yield (prelude, body) for each top-level block; bodies may contain nested blocks."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    i = 0
    while True:
        j = css.find("{", i)
        if j < 0:
            return
        depth, k = 1, j + 1
        while depth:
            if k >= len(css):
                raise RenderError("unbalanced braces in template CSS")
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        yield css[i:j].strip(), css[j + 1:k - 1]
        i = k


def scope_css(css: str, scope: str) -> str:
    """Prefix every page selector with ``.<scope>`` so pages with different rules for the same class
    can share one document. Document-level rules (html, body, *, :root, @page) are dropped: the
    renderer writes its own document rules."""
    out = []
    for prelude, body in _blocks(css):
        if prelude.startswith("@media"):
            inner = scope_css(body, scope)
            if inner.strip():
                out.append(f"{prelude} {{\n{inner}\n}}")
            continue
        if prelude.startswith("@"):
            continue  # @page and similar belong to the document
        selectors = [s.strip() for s in prelude.split(",")]
        kept = [f".{scope} {s}" for s in selectors if s.split()[0] not in _DOCUMENT_SELECTORS]
        if kept:
            out.append(f"{', '.join(kept)} {{{body}}}")
    return "\n".join(out)


DOCUMENT_CSS = """
* { box-sizing: border-box; }
html, body { margin: 0; }
body {
  display: flex; flex-direction: column; align-items: center; gap: 32px; padding: 32px;
  color: var(--ink); background: var(--canvas);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.bv-page { break-after: page; }
.bv-page:last-child { break-after: auto; }
@media print {
  @page { size: A4; margin: 0; }
  body { padding: 0; gap: 0; background: var(--white); }
  .page { border: 0; border-radius: 0; box-shadow: none; }
}
"""

# Contract-required states the static samples could not show (band colours, Stay put, figure row).
RENDERER_CSS = """
.bv-cover.band-good .score-label { color: var(--green); }
.bv-cover.band-medium .score-label { color: var(--amber); }
.bv-cover.band-poor .score-label { color: var(--red); }

.bv-service.band-good .gauge .progress { stroke: var(--green); }
.bv-service.band-medium .gauge .progress { stroke: var(--amber); }
.bv-service.band-poor .gauge .progress { stroke: var(--red); }
.bv-service.band-good .market-position { color: var(--green); }
.bv-service.band-medium .market-position { color: var(--amber); }
.bv-service.band-poor .market-position { color: var(--red); }
.bv-service.stay-put .recommendation { background: var(--green-soft); border-color: var(--green-border); }
.bv-service.stay-put .recommendation .icon,
.bv-service.stay-put .recommendation-label { color: var(--green); }

.bv-service .figures { display: grid; gap: 12px; padding: 18px 24px 20px; border-top: 1px solid var(--line); }
.bv-service .figure span { display: block; margin-bottom: 4px; color: var(--muted); font-size: 9px; font-weight: 700; }
.bv-service .figure strong { color: var(--navy); font-size: 15px; letter-spacing: -0.02em; }
.bv-service .figure.figure-saving strong { color: var(--green); }
.bv-service .figure.figure-saving small { margin-left: 6px; color: var(--green); font-size: 9px; font-weight: 700; }
.bv-service .meaning p + p { margin-top: 8px; }
.bv-service .missing-details .missing-value { margin-right: 6px; }

.bv-overview .interpretation.single { grid-template-columns: 1fr; }
.bv-overview .interpretation.single .interpretation-copy { padding-left: 0; border-left: 0; }

.bv-plan .top-action-content .action-reason { margin: 8px 0 0; color: var(--body-copy); font-size: 10px; line-height: 1.5; }
.bv-plan .help p + p { margin-top: 6px; }
"""


# ---------------------------------------------------------------- shared fragments

def _brand(logo: str) -> str:
    return f'<div class="report-brand"><img src="{logo}" alt="" /><span>Billvisor</span></div>'


def _watermark(logo: str) -> str:
    return f'<img class="closing-watermark" src="{logo}" alt="" aria-hidden="true" />'


def _icon(icon_id: str, cls: str = "icon") -> str:
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{icon_id}" /></svg>'


def _footer(report: dict, n: int, total: int) -> str:
    return (f'<div class="footer">{e(report["report_id"])} · Version {e(report["report_version"])} · '
            f'Page {n} of {total}</div>')


def _gauge_large(value: int) -> str:
    return ('<svg viewBox="0 0 180 130" aria-hidden="true">'
            '<path class="track" d="M22 111 A72 72 0 1 1 158 111" pathLength="100" />'
            f'<path class="progress" d="M22 111 A72 72 0 1 1 158 111" pathLength="100" stroke-dasharray="{value} 100" />'
            '</svg>')


def _mini_score(score: dict | None) -> str:
    if not score:
        return '<div class="score unknown" aria-label="Health score unavailable"><span class="score-value">—</span></div>'
    v, cls = score["value"], BAND_CLASS[score["band"]]
    return (f'<div class="score {cls}" aria-label="Health score {v} out of 100">'
            '<svg viewBox="0 0 58 56" aria-hidden="true">'
            '<path class="track" d="M14 46 A22 22 0 1 1 44 46" pathLength="100" />'
            f'<path class="progress" d="M14 46 A22 22 0 1 1 44 46" pathLength="100" stroke-dasharray="{v} 100" />'
            f'</svg><span class="score-value">{v}</span></div>')


def _primary(data: dict) -> tuple[dict, dict]:
    if not data["priority_actions"]:
        raise RenderError("no priority actions: the cover and action plan need a primary action")
    action = data["priority_actions"][0]
    page = next(p for p in data["service_pages"] if p["unit_id"] == action["unit_id"])
    return action, page


# ---------------------------------------------------------------- pages

def _cover(data: dict, logo: str, house: str) -> tuple[str, str]:
    ov = data["overall"]
    if ov is None:
        raise RenderError("no overall Bills Health Score (no service has a numeric score); the renderer contract "
                          "has no approved cover treatment for this case")
    action, page = _primary(data)
    totals = data["totals"]
    services = ov["contributing_services"]
    savings = totals["potential_savings_gbp"]
    saving_block = (f'<div class="saving"><span>Potential annual savings</span><strong>{money_whole(savings)}</strong>'
                    '<small>across reviewed bills</small></div>') if savings is not None else ""
    body = f"""
<article class="page">
  <header class="topbar">
    <div class="brand"><img class="brand-logo" src="{logo}" alt="" />Billvisor</div>
    <div class="meta">Bills Health Report<br />{e(data["report"]["first_name"])}</div>
  </header>
  <section class="hero">
    <div class="hero-copy">
      <h1>Your Bills<br />Health Report</h1>
      <p class="intro">A clear view of your household bills, what deserves your attention and what does not.</p>
    </div>
    <div class="house-circle" aria-hidden="true"></div>
    <img class="house" src="{house}" alt="House illustration" />
  </section>
  <section class="health-card">
    <div class="score-panel">
      <p class="card-kicker">Bills Health Score</p>
      <div class="gauge-wrap">
        <svg viewBox="0 0 180 130" aria-hidden="true">
          <path d="M22 111 A72 72 0 1 1 158 111" pathLength="100" fill="none" stroke="var(--gauge-track)" stroke-width="10" stroke-linecap="round" />
          <path d="M22 111 A72 72 0 1 1 158 111" pathLength="100" fill="none" stroke="{BAND_VAR[ov["band"]]}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{ov["value"]} 100" />
        </svg>
        <div class="score-value"><strong>{ov["value"]}</strong><span>/100</span></div>
      </div>
      <div class="score-label">{e(ov["band"])}</div>
      <p class="score-note">Based on {services} scored service{"" if services == 1 else "s"}</p>
    </div>
    <div class="answer-panel">
      <div>
        <div class="answer-label">Our top recommendation</div>
        <p class="answer-title">{e(action["next_step"])}</p>
        <p class="answer-reason">{e(page["explanation"])}</p>
      </div>
      {saving_block}
    </div>
  </section>
  <section class="glance-card">
    <p class="glance-title">At a glance</p>
    <div class="metrics">
      <div class="metric">{_icon("icon-report", "metric-icon")}<div><strong>{totals["services_reviewed"]}</strong><span>services reviewed</span></div></div>
      <div class="metric">{_icon("icon-spend", "metric-icon")}<div><strong>{money_whole(totals["annual_spend_gbp"]) if totals["annual_spend_gbp"] is not None else "—"}</strong><span>annual spend</span></div></div>
      <div class="metric saving-metric">{_icon("icon-savings", "metric-icon")}<div><strong>{money_whole(savings) if savings is not None else "—"}</strong><span>potential savings</span></div></div>
      <div class="metric">{_icon("icon-action", "metric-icon")}<div><strong>{totals["priority_actions"]}</strong><span>priority actions</span></div></div>
    </div>
  </section>
  {_watermark(logo)}
  @@FOOTER@@
</article>"""
    return f"bv-cover band-{BAND_CLASS[ov['band']]}", body


def _overview(data: dict, logo: str) -> tuple[str, str]:
    rows = []
    for r in data["overview"]:
        icon = UNIT_TEXT[r["unit_id"]][3]
        if r["coverage_status"] == "Not analysed":
            position = '<span class="position unknown">Not analysed</span>'
        elif r["score"]:
            position = f'<span class="position {BAND_CLASS[r["score"]["band"]]}">{e(r["score"]["band"])}</span>'
        else:
            position = '<span class="position unknown">—</span>'
        spend = f'<td class="money">{money_whole(r["annual_spend_gbp"])}</td>' if r["annual_spend_gbp"] is not None \
            else '<td class="money">—</td>'
        saving = f'<td class="saving">{money_whole(r["potential_saving_gbp"])}</td>' \
            if r["potential_saving_gbp"] is not None else "<td>—</td>"
        rows.append(f'<tr><td><div class="service">{_icon(icon)}{e(r["label"])}</div></td>{spend}<td>{position}</td>'
                    f'{saving}<td>{_mini_score(r["score"])}</td></tr>')
    totals = data["totals"]
    spend_total = money_whole(totals["annual_spend_gbp"]) if totals["annual_spend_gbp"] is not None else "—"
    savings = totals["potential_savings_gbp"]
    interp = []
    if savings is not None:
        interp.append(f'<div class="saving-summary">{_icon("icon-savings")}<div><span>Total potential savings</span>'
                      f'<strong>{money_whole(savings)}</strong></div></div>')
    if data["summary"]:
        interp.append(f'<div class="interpretation-copy"><p>{e(data["summary"])}</p></div>')
    body = f"""
<article class="page">
  {_brand(logo)}
  <h1>Your Household Overview</h1>
  <section class="overview">
    <table>
      <colgroup><col style="width:25%" /><col style="width:17%" /><col style="width:21%" /><col style="width:20%" /><col style="width:17%" /></colgroup>
      <thead><tr><th>Service</th><th>Annual spend</th><th>Market position</th><th>Potential savings</th><th>Health score</th></tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table>
    <div class="total-row">
      <div class="total-label">Total</div>
      <div class="total-stat"><span>Annual spend</span><strong>{spend_total}</strong></div>
      <div></div>
      <div class="total-stat savings"><span>Potential savings</span><strong>{money_whole(savings) if savings is not None else "—"}</strong></div>
      <div></div>
    </div>
  </section>
  {f'<section class="interpretation{" single" if len(interp) == 1 else ""}">{"".join(interp)}</section>' if interp else ""}
  <div class="key" aria-label="Market position key">
    <div class="key-item"><span class="dot good"></span>Good</div>
    <div class="key-item"><span class="dot medium"></span>Medium</div>
    <div class="key-item"><span class="dot poor"></span>Poor</div>
    <div class="key-item"><span class="dot unknown"></span>Analysed with limitations</div>
  </div>
  {_watermark(logo)}
  @@FOOTER@@
</article>"""
    return "bv-overview", body


def _action_class(action: dict, page: dict) -> str:
    """Card accent: green for Stay put, otherwise the service's score band (no priority mapping)."""
    if action["action_type"] == "Stay put":
        return "none"
    score = page["score"]
    return {"Poor": "high", "Medium": "medium", "Good": "none"}[score["band"]] if score else ""


def _priorities(data: dict, logo: str) -> tuple[str, str]:
    pages = {p["unit_id"]: p for p in data["service_pages"]}
    cards = []
    for a in data["priority_actions"]:
        page = pages[a["unit_id"]]
        chip = '<span class="priority">No action needed</span>' if a["action_type"] == "Stay put" else ""
        stats = ""
        if a["potential_saving_gbp"] is not None:
            stats += f'<div class="stat saving"><span>Potential savings</span><strong>{money_whole(a["potential_saving_gbp"])}</strong></div>'
        if a["effort"]:
            stats += f'<div class="stat"><span>Effort</span><strong>{e(a["effort"])}</strong></div>'
        cards.append(f"""
    <article class="action {_action_class(a, page)}">
      {_icon(UNIT_TEXT[a["unit_id"]][2], "icon service-icon")}
      <div>{chip}<strong class="action-title">{e(a["next_step"])}</strong><p class="action-reason">{e(page["explanation"])}</p></div>
      {stats}
    </article>""")
    why = ""
    if data["priority_reason"]:
        why = (f'<section class="why">{_icon("icon-info")}<div><strong>Why these priorities?</strong>'
               f'<p>{e(data["priority_reason"])}</p></div></section>')
    body = f"""
<article class="page">
  {_brand(logo)}
  <h1>Your Priority Actions</h1>
  <p class="intro">We focus on what is most worth your time.</p>
  <section class="actions">{"".join(cards)}
  </section>
  {why}
  {_watermark(logo)}
  @@FOOTER@@
</article>"""
    return "bv-priorities", body


def _facts(page: dict) -> str:
    uid, cs = page["unit_id"], page["current_service"]
    confirm = page["action_type"] == "Confirm information"
    if uid == "broadband":
        rows = [("Provider", cs["provider"]),
                ("Download speed", None if cs["download_speed_mbps"] is None else f"{number_text(cs['download_speed_mbps'])} Mbps"),
                ("Monthly cost", None if cs["monthly_cost_gbp"] is None else money_2dp(cs["monthly_cost_gbp"])),
                ("Contract ends", None if cs["contract_end"] is None else end_text(cs["contract_end"]))]
    elif uid == "mobile":
        allowance = ("Unlimited data" if cs["data_allowance_unlimited"]
                     else None if cs["data_allowance_gb"] is None else f"{number_text(cs['data_allowance_gb'])} GB")
        rows = [("Provider", cs["provider"]),
                ("Data allowance", allowance),
                ("Plan type", None if cs["plan_type"] is None else CODE_TEXT[cs["plan_type"]]),
                ("Monthly cost", None if cs["monthly_cost_gbp"] is None else money_2dp(cs["monthly_cost_gbp"])),
                ("Contract ends", None if cs["contract_end"] is None else end_text(cs["contract_end"]))]
    else:
        services = cs["services"]
        if services is not None and services not in SERVICES_TEXT:
            raise RenderError(f"no display rule for energy services value {services!r}")
        rows = [("Supplier", cs["supplier"]),
                ("Services", None if services is None else SERVICES_TEXT[services]),
                ("Tariff", cs["tariff"]),
                ("Monthly payment", None if cs["monthly_payment_gbp"] is None else money_2dp(cs["monthly_payment_gbp"])),
                ("Tariff ends", None if cs["tariff_end"] is None else end_text(cs["tariff_end"]))]
    out = []
    for label, value in rows:
        if value is None:
            if confirm and label != "Monthly payment":
                out.append(f'<div class="fact"><dt>{label}</dt><dd class="missing">Not provided</dd></div>')
            continue  # contract section 4: render only fields that were supplied
        out.append(f'<div class="fact"><dt>{label}</dt><dd>{e(value)}</dd></div>')
    return "".join(out)


def _figures(page: dict) -> str:
    items = []
    if page["unit_id"] in ENERGY_UNITS:
        if page["current_annual_spend_gbp"] is not None:
            items.append(f'<div class="figure"><span>Estimated annual energy cost</span>'
                         f'<strong>{money_whole(page["current_annual_spend_gbp"])}</strong></div>')
    else:
        if page["current_annual_spend_gbp"] is not None:
            items.append(f'<div class="figure"><span>You pay each year</span>'
                         f'<strong>{money_whole(page["current_annual_spend_gbp"])}</strong></div>')
        if page["comparison_annual_gbp"] is not None:
            items.append(f'<div class="figure"><span>Similar services cost</span>'
                         f'<strong>about {money_whole(page["comparison_annual_gbp"])} a year</strong></div>')
    if page["potential_saving_gbp"] is not None:
        # QA section 3: a displayed saving is identified as an estimate (the approved template's marker).
        items.append(f'<div class="figure figure-saving"><span>Potential saving</span>'
                     f'<strong>{money_whole(page["potential_saving_gbp"])}</strong><small>Estimated</small></div>')
    return f'<div class="figures">{"".join(items)}</div>' if items else ""


def _service(page: dict, logo: str) -> tuple[str, str]:
    uid = page["unit_id"]
    title, heading, icon, _ = UNIT_TEXT[uid]
    confirm = page["action_type"] == "Confirm information"
    score = page["score"]
    if score:
        right = f"""
      <div class="score-section">
        <div class="score-label">Health score</div>
        <div class="gauge">{_gauge_large(score["value"])}<div class="gauge-value"><strong>{score["value"]}</strong><span>/100</span></div></div>
        <div class="market-position">{e(score["band"])}</div>
      </div>"""
    else:
        right = f"""
      <div class="status-section"><div>
        <div class="status-mark">-</div>
        <strong>{e(page["coverage_status"])}</strong>
        <p>We have not calculated a health score or market position.</p>
      </div></div>"""

    if confirm:
        sections = []
        if page["confirmed_items"]:
            items = "".join(f'<div class="confirmed-item"><span class="check">✓</span><span>{e(t)}</span></div>'
                            for t in page["confirmed_items"])
            sections.append(f'<section class="received"><h2>What we could confirm</h2><div class="confirmed-list">{items}</div></section>')
        needed = "".join(f'<span class="missing-value">{e(t)}</span>' for t in page["still_needed"])
        limitation = f'<p>{e(page["limitation"])}</p>' if page["limitation"] else ""
        sections.append(f'<section class="missing-details"><h2>What we still need</h2>{limitation}{needed}</section>')
        rec_icon = "icon-reply"
    else:
        sections = []
        if page["headline"]:
            sections.append(f'<section class="comparison"><h2>How it compares</h2><p>{e(page["headline"])}</p></section>')
        meaning = [page["limitation"], page["estimate_note"],
                   ENERGY_SENTENCE if uid in ENERGY_UNITS else None,
                   page["provider_note"]] + [f["text"] for f in page["findings"]]
        meaning = [m for m in meaning if m]
        if meaning:
            sections.append('<section class="meaning"><h2>What this means</h2>'
                            + "".join(f"<p>{e(m)}</p>" for m in meaning) + "</section>")
        rec_icon = icon
    sections.append(f"""
      <section class="recommendation">
        {_icon(rec_icon)}
        <div>
          <span class="recommendation-label">Our recommendation</span>
          <strong>{e(page["next_step"])}</strong>
          <p>{e(page["explanation"])}</p>
        </div>
      </section>""")

    classes = ["bv-service"]
    if score:
        classes.append(f"band-{BAND_CLASS[score['band']]}")
    if page["action_type"] == "Stay put":
        classes.append("stay-put")
    body = f"""
<article class="page">
  {_brand(logo)}
  <header class="page-title">{_icon(icon)}<h1>{title}</h1></header>
  <section class="analysis-grid">
    <article class="card current">
      <div class="card-section"><h2>{heading}</h2><dl class="facts">{_facts(page)}</dl></div>
      {"" if confirm else _figures(page)}
      {right}
    </article>
    <article class="card analysis">{"".join(sections)}
    </article>
  </section>
  {_watermark(logo)}
  @@FOOTER@@
</article>"""
    return " ".join(classes), body


def _plan(data: dict, logo: str) -> tuple[str, str]:
    action, page = _primary(data)
    pages = {p["unit_id"]: p for p in data["service_pages"]}
    stats = ""
    if action["potential_saving_gbp"] is not None:
        stats += (f'<div class="action-stat saving"><span>Potential saving</span>'
                  f'<strong>{money_whole(action["potential_saving_gbp"])} / year</strong></div>')
    if action["effort"]:
        stats += f'<div class="action-stat"><span>Effort</span><strong>{e(action["effort"])}</strong></div>'
    rows = []
    for a in data["priority_actions"]:
        saving = f'<td class="saving">{money_whole(a["potential_saving_gbp"])}</td>' \
            if a["potential_saving_gbp"] is not None else "<td>—</td>"
        rows.append(f'<tr><td><div class="service-action">{_icon(UNIT_TEXT[a["unit_id"]][2])}{e(a["next_step"])}</div></td>'
                    f'{saving}<td class="time">{e(a["effort"]) if a["effort"] else "—"}</td></tr>')
    notes = "".join(f"<p>{e(n)}</p>" for n in data["report_notes"])
    _ = pages  # every action has a page (checked by _primary/_priorities)
    body = f"""
<article class="page">
  {_brand(logo)}
  <h1>Your Action Plan</h1>
  <section class="top-action">
    {_icon("icon-star")}
    <div class="top-action-content">
      <span class="action-kicker">If you only do one thing...</span>
      <strong class="action-title">{e(action["next_step"])}</strong>
      <p class="action-reason">{e(page["explanation"])}</p>
      {f'<div class="top-action-stats">{stats}</div>' if stats else ""}
    </div>
  </section>
  <section class="plan">
    <table>
      <colgroup><col style="width:56%" /><col style="width:24%" /><col style="width:20%" /></colgroup>
      <thead><tr><th>Action</th><th>Potential savings</th><th>Effort</th></tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table>
  </section>
  <section class="help">
    {_icon("icon-support")}
    <div>
      <strong>We are here to help</strong>
      <p>Reply to your report if anything is unclear or if any detail needs correcting. You will not need to start again.</p>
      {notes}
    </div>
  </section>
  {_watermark(logo)}
  @@FOOTER@@
</article>"""
    return "bv-plan", body


# ---------------------------------------------------------------- document

def render_report(data: dict) -> str:
    """Render approved report data (the dict written to report_data.v<N>.json) to one HTML document."""
    if not str(data.get("contract_version", "")).startswith("1."):
        raise RenderError(f"unsupported report_data contract_version {data.get('contract_version')!r}")
    logo = _data_uri("billvisor-logo.svg", "image/svg+xml")
    house = _data_uri("billvisor-house.png", "image/png")

    pages = [_cover(data, logo, house), _overview(data, logo), _priorities(data, logo)]
    pages += [_service(p, logo) for p in data["service_pages"]]
    pages.append(_plan(data, logo))
    total = len(pages)
    rendered = []
    for n, (classes, body) in enumerate(pages, start=1):
        body = body.replace("@@FOOTER@@", _footer(data["report"], n, total))
        rendered.append(f'<div class="bv-page {classes}">{body}\n</div>')

    css = [_read("report-design-tokens.css"), DOCUMENT_CSS]
    for scope, files in PAGE_CSS.items():
        css.extend(scope_css(_page_css(f), f"bv-{scope}") for f in files)
    css.append(RENDERER_CSS)

    report = data["report"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Bills Health Report · {e(report["report_id"])} · Version {e(report["report_version"])}</title>
<style>
{chr(10).join(css)}
</style>
</head>
<body>
<svg width="0" height="0" aria-hidden="true" style="position:absolute">{_icon_symbols()}</svg>
{chr(10).join(rendered)}
</body>
</html>
"""
