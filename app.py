import streamlit as st
from groq import Groq
import time
import re

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Glade.ai · AI Contract Review",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d0f14; color: #e8e6e0; }

/* Sidebar */
[data-testid="stSidebar"] { background: #111318 !important; border-right: 1px solid #1e2130; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: #9a98a0 !important; font-size: 0.75rem !important;
    letter-spacing: 0.06em; text-transform: uppercase;
}
.settings-label {
    font-size: 0.65rem; color: #3a3850; letter-spacing: 0.14em;
    text-transform: uppercase; margin-bottom: 1rem;
    padding-bottom: 0.5rem; border-bottom: 1px solid #1e2130;
}

/* Hero */
.hero-eyebrow { font-size: 0.72rem; color: #c8b87a; letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 0.6rem; font-weight: 500; }
.hero-title { font-family: 'DM Serif Display', serif; font-size: 2.4rem; color: #e8e6e0; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.75rem; }
.hero-sub { font-size: 0.9rem; color: #6a6880; line-height: 1.6; max-width: 540px; margin-bottom: 2.2rem; }

/* Pills */
.pill-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 2.5rem; }
.pill { font-size: 0.7rem; font-weight: 500; letter-spacing: 0.05em; padding: 4px 12px; border-radius: 20px; border: 1px solid #1e2130; color: #6a6880; background: #13151c; }

/* Input */
.stTextArea textarea {
    background: #13151c !important; border: 1px solid #1e2130 !important;
    border-radius: 6px !important; color: #ccc9c0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.82rem !important;
    line-height: 1.7 !important; resize: vertical;
}
.stTextArea textarea:focus { border-color: #c8b87a !important; box-shadow: 0 0 0 2px rgba(200,184,122,0.10) !important; }

/* Upload */
[data-testid="stFileUploader"] { background: #13151c; border: 1px dashed #252838; border-radius: 6px; padding: 1.2rem; }
[data-testid="stFileUploader"]:hover { border-color: #c8b87a55; }

/* Button */
.stButton > button {
    background: #c8b87a !important; color: #0d0f14 !important; border: none !important;
    border-radius: 5px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    letter-spacing: 0.03em !important; padding: 0.65rem 1.6rem !important; transition: all 0.18s ease !important;
}
.stButton > button:hover { background: #d9cb92 !important; transform: translateY(-1px); box-shadow: 0 6px 24px rgba(200,184,122,0.28) !important; }

/* Microcopy */
.microcopy { font-size: 0.72rem; color: #3a3850; letter-spacing: 0.04em; margin-top: 0.5rem; }

/* Divider */
hr { border-color: #1a1c28 !important; margin: 2rem 0 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #1e2130; }
.stTabs [data-baseweb="tab"] { color: #4a4860; font-size: 0.8rem; letter-spacing: 0.04em; padding: 0.55rem 1.1rem; border-radius: 0; }
.stTabs [aria-selected="true"] { color: #c8b87a !important; border-bottom: 2px solid #c8b87a !important; background: transparent !important; }

/* Cards — all content rendered inside via HTML */
.r-card { background: #111318; border: 1px solid #1a1c28; border-radius: 8px; padding: 1.4rem 1.6rem; margin-bottom: 0.9rem; }
.r-card-title { font-family: 'DM Serif Display', serif; font-size: 0.95rem; color: #c8b87a; margin-bottom: 1rem; }
.r-card-body { font-size: 0.855rem; color: #b8b6b0; line-height: 1.8; }

/* Bullet list inside cards */
.r-list { list-style: none; padding: 0; margin: 0; }
.r-list li { padding: 0.3rem 0; border-bottom: 1px solid #141620; display: flex; gap: 0.6rem; align-items: flex-start; }
.r-list li:last-child { border-bottom: none; }
.r-list li::before { content: "—"; color: #3a3850; flex-shrink: 0; margin-top: 1px; }
.r-list-bold { font-weight: 600; color: #d8d6d0; margin-right: 4px; }

/* Risk badges */
.risk-high   { display:inline-block; white-space:nowrap; flex-shrink:0; background:#2e1010; color:#f87171; border:1px solid #4a1818; padding:2px 9px; border-radius:20px; font-size:0.67rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; margin-right:6px; vertical-align:middle; }
.risk-medium { display:inline-block; white-space:nowrap; flex-shrink:0; background:#261e08; color:#fbbf24; border:1px solid #3d3008; padding:2px 9px; border-radius:20px; font-size:0.67rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; margin-right:6px; vertical-align:middle; }
.risk-low    { display:inline-block; white-space:nowrap; flex-shrink:0; background:#0b2218; color:#34d399; border:1px solid #0f3323; padding:2px 9px; border-radius:20px; font-size:0.67rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; margin-right:6px; vertical-align:middle; }

/* Risk rows */
.risk-row { padding: 0.5rem 0; border-bottom: 1px solid #141620; line-height: 1.65; font-size: 0.855rem; color: #b8b6b0; display: flex; align-items: flex-start; gap: 0.5rem; }
.risk-row:last-child { border-bottom: none; }

/* Checklist */
.cl-item { display: flex; align-items: flex-start; gap: 0.65rem; padding: 0.5rem 0; border-bottom: 1px solid #141620; font-size: 0.855rem; color: #b8b6b0; line-height: 1.55; }
.cl-item:last-child { border-bottom: none; }
.cl-box { width: 15px; height: 15px; border: 1.5px solid #2a2d45; border-radius: 3px; flex-shrink: 0; margin-top: 2px; background: #0d0f14; }

/* Timing chip */
.timing-chip { display: inline-flex; align-items: center; gap: 0.4rem; background: #111318; border: 1px solid #1e2130; border-radius: 20px; padding: 4px 12px; font-size: 0.72rem; color: #5a5870; margin-bottom: 1.5rem; }
.timing-chip strong { color: #c8b87a; }

/* Alert */
.stAlert { background: #111318 !important; border: 1px solid #1e2130 !important; color: #9a98a0 !important; border-radius: 6px !important; font-size: 0.82rem !important; }
.stSpinner > div { border-top-color: #c8b87a !important; }

/* Text input */
.stTextInput input { background: #13151c !important; border: 1px solid #1e2130 !important; color: #ccc9c0 !important; border-radius: 4px !important; font-size: 0.82rem !important; }
.stTextInput input:focus { border-color: #c8b87a !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d0f14; }
::-webkit-scrollbar-thumb { background: #1e2130; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an AI contract review assistant for law firms and legal professionals.
Your job is to help attorneys quickly understand contracts by extracting key terms, identifying potential risks, and summarizing important obligations in a concise, decision-useful format.

Review style: flag-based, attorney-friendly, optimized for fast triage.

Guidelines:
- Be concise, neutral, and professional.
- Do not provide legal advice.
- Focus on practical review support for busy attorneys.
- Highlight unusual, missing, or one-sided terms — even if they appear buried in standard-looking language.
- Be especially alert to clauses that heavily favor one party, such as: unilateral fee changes, perpetual/irrevocable IP grants, immediate payment-on-termination, sole-discretion performance, no-cure termination, subcontractor use without approval, and liability caps that only protect one side.
- If something is unclear, say so plainly.
- Avoid speculation, but do not understate serious issues.

Return the output using EXACTLY this structure. Use plain text only — no markdown bold, no backticks, no code formatting inside any field values:

## 1. CONTRACT SUMMARY
2-4 plain sentences describing what this contract is about.

## 2. KEY PARTIES
- Party Name (Role): brief description
- Party Name (Role): brief description

## 3. IMPORTANT TERMS
- Term / Duration: [value]
- Payment Terms: [value]
- Responsibilities: [value]
- Termination Conditions: [value]
- Confidentiality / IP Provisions: [value]

## 4. POTENTIAL RISKS OR RED FLAGS
Each risk on its own line. Start every line with [HIGH RISK], [MEDIUM RISK], or [LOW RISK] followed by a colon and the issue description. Be thorough — list every notable issue you find.

Risk severity guide:
- [HIGH RISK]: Heavily one-sided, immediately attorney attention needed (e.g. perpetual IP grants, unilateral fee changes, no liability protection, immediate fees on termination, sole-discretion clauses).
- [MEDIUM RISK]: Needs review for business impact (e.g. auto-renewal with short notice, liability caps, subcontractor rights).
- [LOW RISK]: Standard but worth noting.

## 5. MISSING OR UNCLEAR INFORMATION
Plain sentences calling out absent, ambiguous, or incomplete details.

## 6. SUGGESTED LAWYER REVIEW CHECKLIST
- [action item]
- [action item]
(each item starts with a dash)
"""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="settings-label">⚙ Settings</div>', unsafe_allow_html=True)

    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com"
    )

    model_choice = st.selectbox(
        "Model",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
        index=0,
        help="Larger models are more thorough; smaller models are faster."
    )

    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.05,
                            help="Lower = more consistent outputs.")

    st.markdown("---")
    st.markdown("""
    <p style="color:#3a3850;font-size:0.68rem;line-height:1.7">
    Output is for decision support only and does not constitute legal advice.
    All reviews should be verified by a qualified attorney.
    </p>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-eyebrow">AI Contract Review Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Fast, structured contract<br>review for attorneys.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload or paste a contract to extract key terms, surface risks, and generate a decision-ready summary.</div>', unsafe_allow_html=True)
st.markdown("""
<div class="pill-row">
  <span class="pill">Key Term Extraction</span>
  <span class="pill">Risk Flagging</span>
  <span class="pill">Lawyer Checklist</span>
  <span class="pill">Plain-English Summary</span>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
tab_paste, tab_upload = st.tabs(["  Paste Contract  ", "  Upload .txt  "])
contract_text = ""

with tab_paste:
    contract_text = st.text_area(
        "Contract text",
        height=300,
        placeholder="Paste the full contract text here…\n\nExample: This Software License Agreement is entered into as of January 1, 2025, between Acme Corp ('Licensor') and Beta Inc ('Licensee')…",
        label_visibility="collapsed",
    )

with tab_upload:
    uploaded_file = st.file_uploader("Upload contract (.txt)", type=["txt"], label_visibility="collapsed")
    if uploaded_file:
        contract_text = uploaded_file.read().decode("utf-8")
        st.success(f"✓ **{uploaded_file.name}** — {len(contract_text):,} characters loaded")
        with st.expander("Preview"):
            st.code(contract_text[:600] + ("…" if len(contract_text) > 600 else ""), language=None)

st.markdown("<br>", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
btn_col, _ = st.columns([1, 5])
with btn_col:
    analyze_clicked = st.button("Generate Legal Review", use_container_width=True)
st.markdown('<div class="microcopy">Decision support only. Not legal advice.</div>', unsafe_allow_html=True)

# ── HTML rendering helpers ────────────────────────────────────────────────────
def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inject_risk_badges(text: str) -> str:
    text = re.sub(r'\[HIGH RISK\]',   '<span class="risk-high">High Risk</span>',   text, flags=re.IGNORECASE)
    text = re.sub(r'\[MEDIUM RISK\]', '<span class="risk-medium">Medium Risk</span>', text, flags=re.IGNORECASE)
    text = re.sub(r'\[LOW RISK\]',    '<span class="risk-low">Low Risk</span>',    text, flags=re.IGNORECASE)
    text = re.sub(r'🔴\s*HIGH\b',    '<span class="risk-high">High Risk</span>',   text)
    text = re.sub(r'🟡\s*MEDIUM\b',  '<span class="risk-medium">Medium Risk</span>', text)
    text = re.sub(r'🟢\s*LOW\b',     '<span class="risk-low">Low Risk</span>',    text)
    return text

def render_summary_card(label: str, body: str) -> str:
    """Plain paragraph card."""
    safe = escape_html(body.strip())
    return f"""
    <div class="r-card">
      <div class="r-card-title">{label}</div>
      <div class="r-card-body" style="line-height:1.8">{safe}</div>
    </div>"""

def render_bullet_card(label: str, body: str) -> str:
    """Bullet list card — handles '- Key: value' and '- item' formats."""
    lines = [l for l in body.splitlines() if l.strip()]
    items_html = ""
    for line in lines:
        line = line.lstrip("-•*").strip()
        if not line:
            continue
        # Check for bold-key pattern like "Term / Duration: value"
        m = re.match(r'\*{0,2}([^:*]+)\*{0,2}:\s*(.*)', line)
        if m:
            key = escape_html(m.group(1).strip())
            val = escape_html(m.group(2).strip())
            items_html += f'<li><span class="r-list-bold">{key}:</span> {val}</li>'
        else:
            items_html += f'<li>{escape_html(line)}</li>'
    return f"""
    <div class="r-card">
      <div class="r-card-title">{label}</div>
      <div class="r-card-body"><ul class="r-list">{items_html}</ul></div>
    </div>"""

def render_risks_card(label: str, body: str) -> str:
    """Risk rows with coloured badges, all inside card."""
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    rows_html = ""
    for line in lines:
        # Skip pure header lines
        if line.startswith("#"):
            continue
        badged = inject_risk_badges(escape_html(line))
        # If a badge was injected the escaped < would break it — re-inject on raw
        badged = inject_risk_badges(line)  # inject on original, badges are safe HTML
        # Escape only the text portion (after the badge)
        rows_html += f'<div class="risk-row">{badged}</div>'
    return f"""
    <div class="r-card">
      <div class="r-card-title">{label}</div>
      <div class="r-card-body">{rows_html}</div>
    </div>"""

def render_missing_card(label: str, body: str) -> str:
    """Missing info as simple paragraphs, inside card."""
    lines = [l.strip().lstrip("-•*").strip() for l in body.splitlines() if l.strip()]
    paras = "".join(f'<p style="margin:0.4rem 0">{escape_html(l)}</p>' for l in lines if l)
    return f"""
    <div class="r-card">
      <div class="r-card-title">{label}</div>
      <div class="r-card-body">{paras}</div>
    </div>"""

def render_checklist_card(label: str, body: str) -> str:
    """Checkbox list, all inside card."""
    items = [l.lstrip("-•*[ ]").strip() for l in body.splitlines()
             if l.strip() and (l.strip().startswith("-") or l.strip().startswith("•"))]
    items_html = "".join(
        f'<div class="cl-item"><div class="cl-box"></div><div>{escape_html(item)}</div></div>'
        for item in items if item
    )
    return f"""
    <div class="r-card">
      <div class="r-card-title">{label}</div>
      <div class="r-card-body">{items_html}</div>
    </div>"""

# ── Section map ───────────────────────────────────────────────────────────────
SECTION_MAP = {
    "1. CONTRACT SUMMARY":                  ("📄  Contract Summary",          "summary"),
    "2. KEY PARTIES":                       ("👥  Key Parties",               "parties"),
    "3. IMPORTANT TERMS":                   ("📋  Important Terms",           "terms"),
    "4. POTENTIAL RISKS OR RED FLAGS":      ("⚠️  Risks & Red Flags",        "risks"),
    "5. MISSING OR UNCLEAR INFORMATION":    ("🔍  Missing or Unclear Info",   "missing"),
    "6. SUGGESTED LAWYER REVIEW CHECKLIST": ("✅  Lawyer Review Checklist",   "checklist"),
}

RENDER_FN = {
    "summary":   render_summary_card,
    "parties":   render_bullet_card,
    "terms":     render_bullet_card,
    "risks":     render_risks_card,
    "missing":   render_missing_card,
    "checklist": render_checklist_card,
}

def parse_and_render(raw: str):
    parts = re.split(r'\n##\s+', "\n" + raw)
    rendered = False

    for part in parts:
        part = part.strip()
        if not part:
            continue

        matched_key = matched_label = matched_type = None
        for key, (label, stype) in SECTION_MAP.items():
            if part.upper().startswith(key.upper()):
                matched_key, matched_label, matched_type = key, label, stype
                break

        if not matched_key:
            continue

        body = part[len(matched_key):].strip()
        rendered = True

        fn = RENDER_FN.get(matched_type, render_summary_card)
        html = fn(matched_label, body)
        st.markdown(html, unsafe_allow_html=True)

    if not rendered:
        st.markdown(raw)

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not groq_api_key:
        st.error("Please add your Groq API key in **Settings** (sidebar ›).")
    elif not contract_text or len(contract_text.strip()) < 50:
        st.warning("Please paste or upload a contract to continue.")
    else:
        MAX_CHARS = 36000
        if len(contract_text) > MAX_CHARS:
            st.info(f"Contract exceeds limit — analyzing first {MAX_CHARS:,} characters.")
            contract_text = contract_text[:MAX_CHARS]

        try:
            client = Groq(api_key=groq_api_key)

            with st.spinner("Reviewing contract…"):
                t0 = time.time()
                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Please review the following contract:\n\n{contract_text}"}
                    ],
                    temperature=temperature,
                    max_tokens=4096,
                )
                elapsed = time.time() - t0

            result = response.choices[0].message.content

            st.markdown("---")
            st.markdown(
                f'<div class="timing-chip">⚡ Review generated in <strong>{elapsed:.1f}s</strong></div>',
                unsafe_allow_html=True
            )

            parse_and_render(result)

            st.markdown("---")
            dl_col, _ = st.columns([1, 5])
            with dl_col:
                st.download_button(
                    label="⬇ Download Report",
                    data=result,
                    file_name="glade_contract_review.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        except Exception as e:
            err = str(e)
            if "api_key" in err.lower() or "authentication" in err.lower() or "invalid" in err.lower():
                st.error("Invalid Groq API key — please check Settings.")
            elif "rate" in err.lower():
                st.error("Rate limit reached. Please wait a moment and try again.")
            else:
                st.error(f"Something went wrong: {err}")