"""
BLEU & ROUGE Scorer — Streamlit UI
====================================
Run with:
    pip install streamlit plotly pandas
    streamlit run bleu_rouge_app.py
"""

import json
import math
import re
from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="BLEU & ROUGE Scorer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  GLOBAL STYLES
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e2e8f0;
}

.stApp {
    background: #0a0f1e;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1426 !important;
    border-right: 1px solid #1e2d4a;
}
[data-testid="stSidebar"] * { color: #c8d6ef !important; }

/* ── Header strip ── */
.hero-header {
    background: linear-gradient(135deg, #0f1f3d 0%, #0a1628 50%, #0d1a30 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-header::after {
    content: "";
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(99,102,241,0.09) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -1px;
    color: #f0f6ff;
    margin: 0 0 6px;
}
.hero-title span { color: #38bdf8; }
.hero-sub {
    color: #7ea8cc;
    font-size: 0.92rem;
    font-weight: 300;
    letter-spacing: 0.3px;
}
.badge {
    display: inline-block;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.25);
    color: #38bdf8;
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
    padding: 3px 10px;
    border-radius: 100px;
    margin-right: 6px;
    margin-top: 12px;
}

/* ── Metric cards ── */
.metric-card {
    background: #0d1426;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 10px;
    position: relative;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #2d4a6e; }
.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #6b8aad;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-verdict {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.5px;
}
.metric-bar-wrap {
    background: #0a1220;
    border-radius: 100px;
    height: 5px;
    margin-top: 12px;
    overflow: hidden;
}
.metric-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.6s cubic-bezier(.4,0,.2,1);
}
.score-good   { color: #34d399; }
.score-fair   { color: #fbbf24; }
.score-low    { color: #f87171; }
.bar-good     { background: linear-gradient(90deg,#059669,#34d399); }
.bar-fair     { background: linear-gradient(90deg,#d97706,#fbbf24); }
.bar-low      { background: linear-gradient(90deg,#dc2626,#f87171); }

/* ── Section titles ── */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4a6fa8;
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg,#1e2d4a,transparent);
}

/* ── Info box ── */
.info-box {
    background: rgba(56,189,248,0.06);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.84rem;
    color: #93c5fd;
    line-height: 1.6;
    margin-bottom: 10px;
}
.info-box strong { color: #bae6fd; }

/* ── Batch table ── */
.batch-summary {
    background: #0d1426;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.avg-chip {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    background: #0a1220;
    border: 1px solid #1e3050;
    border-radius: 8px;
    padding: 6px 12px;
    margin: 4px;
    color: #93c5fd;
}
.avg-chip span { color: #34d399; font-weight: 700; }

/* ── Stat pills ── */
.stat-row { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
.stat-pill {
    background: #0a1220;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.8rem;
    color: #7ea8cc;
}
.stat-pill b { color: #c8d6ef; font-family: 'Space Mono', monospace; }

/* ── Textarea label ── */
.stTextArea label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #4a6fa8 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
.stTextArea textarea {
    background: #0d1426 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
    color: #c8d6ef !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 28px !important;
    transition: opacity 0.2s, transform 0.1s !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Tabs ── */
.stTabs [role="tablist"] {
    background: #0d1426;
    border-radius: 10px;
    border: 1px solid #1e2d4a;
    padding: 4px;
    gap: 4px;
}
.stTabs [role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: #6b8aad !important;
    border-radius: 7px !important;
    padding: 8px 20px !important;
    border: none !important;
}
.stTabs [role="tab"][aria-selected="true"] {
    background: #162035 !important;
    color: #e2e8f0 !important;
}
.stTabs [role="tabpanel"] { padding-top: 20px !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0d1426 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #7ea8cc !important;
    font-size: 0.84rem !important;
}
.streamlit-expanderContent {
    background: #090e1c !important;
    border: 1px solid #1e2d4a !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 14px 16px !important;
    font-size: 0.84rem !important;
    color: #93b4d4 !important;
}

/* ── Select / radio ── */
.stSelectbox > div > div {
    background: #0d1426 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #c8d6ef !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: #0d1426 !important;
    border: 1px solid #1e3050 !important;
    border-radius: 8px !important;
    color: #38bdf8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
}
.stDownloadButton > button:hover {
    border-color: #38bdf8 !important;
    background: #0f1e38 !important;
}

/* ── Plotly chart ── */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* ── Dividers ── */
hr { border-color: #1e2d4a !important; margin: 20px 0 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #0d1426 !important;
    border: 1px dashed #2a3f60 !important;
    border-radius: 10px !important;
}

/* ── Hide Streamlit branding ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  CORE LOGIC  (self-contained, no external NLP deps required)
# ══════════════════════════════════════════════════════════════════════════════

def tokenize(text: str) -> list:
    text = re.sub(r'[^\w\s]', ' ', text, flags=re.UNICODE)
    return [t for t in text.lower().split() if t]

def _ngrams(tokens: list, n: int) -> Counter:
    return Counter(tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1))

def _clipped_precision(candidate, reference, n):
    cg = _ngrams(candidate, n); rg = _ngrams(reference, n)
    clipped = sum(min(c, rg[g]) for g, c in cg.items())
    return clipped, max(sum(cg.values()), 1)

def _brevity_penalty(cand_len, ref_len):
    if cand_len >= ref_len: return 1.0
    return math.exp(1 - ref_len / cand_len)

def compute_bleu(candidate, reference, max_n=4):
    ct = tokenize(candidate); rt = tokenize(reference)
    results = {}
    for n in range(1, max_n + 1):
        precs = []
        for order in range(1, n + 1):
            clipped, total = _clipped_precision(ct, rt, order)
            precs.append(math.log((clipped + 1) / (total + 1)))
        bp = _brevity_penalty(len(ct), len(rt))
        results[f"bleu_{n}"] = round(bp * math.exp(sum(precs) / n), 4)
    results["brevity_penalty"]  = round(_brevity_penalty(len(ct), len(rt)), 4)
    results["candidate_length"] = len(ct)
    results["reference_length"] = len(rt)
    return results

def _f1(p, r):
    return 0.0 if p + r == 0 else 2 * p * r / (p + r)

def _rouge_n(candidate, reference, n):
    ct = tokenize(candidate); rt = tokenize(reference)
    cg = _ngrams(ct, n); rg = _ngrams(rt, n)
    overlap = sum(min(c, cg[g]) for g, c in rg.items())
    r = overlap / max(sum(rg.values()), 1)
    p = overlap / max(sum(cg.values()), 1)
    return {"precision": round(p,4), "recall": round(r,4), "f1": round(_f1(p,r),4)}

def _lcs_length(a, b):
    if len(a) < len(b): a, b = b, a
    prev = [0] * (len(b) + 1)
    for tok in a:
        curr = [0] * (len(b) + 1)
        for j, t in enumerate(b, 1):
            curr[j] = prev[j-1]+1 if tok==t else max(prev[j], curr[j-1])
        prev = curr
    return prev[len(b)]

def _rouge_l(candidate, reference):
    ct = tokenize(candidate); rt = tokenize(reference)
    lcs = _lcs_length(ct, rt)
    r = lcs / max(len(rt), 1); p = lcs / max(len(ct), 1)
    return {"precision":round(p,4),"recall":round(r,4),"f1":round(_f1(p,r),4),"lcs_length":lcs}

def compute_rouge(candidate, reference):
    return {
        "rouge_1": _rouge_n(candidate, reference, 1),
        "rouge_2": _rouge_n(candidate, reference, 2),
        "rouge_l": _rouge_l(candidate, reference),
    }


# ══════════════════════════════════════════════════════════════════════════════
#  EXPLANATIONS
# ══════════════════════════════════════════════════════════════════════════════

EXPLANATIONS = {
    "bleu_1": {
        "title": "BLEU-1 — Unigram Precision",
        "what":  "Checks what fraction of individual words in the candidate appear in the reference.",
        "ranges": [(0.7,"Strong — most candidate words are present in the reference."),
                   (0.4,"Moderate — decent word overlap but some mismatches."),
                   (0.0,"Low — many candidate words are absent from the reference.")],
        "tip": "BLEU-1 is the most lenient variant. A high score alone doesn't imply fluency."
    },
    "bleu_2": {
        "title": "BLEU-2 — Bigram Precision",
        "what":  "Measures how many consecutive word-pairs in the candidate match those in the reference.",
        "ranges": [(0.5,"Good bigram overlap — reasonable fluency."),
                   (0.25,"Moderate — some phrases align but structure diverges."),
                   (0.0,"Low — phrasing differs substantially.")],
        "tip": "Bigrams start testing word order, not just word presence."
    },
    "bleu_3": {
        "title": "BLEU-3 — Trigram Precision",
        "what":  "Checks 3-word phrase matches between candidate and reference.",
        "ranges": [(0.4,"Strong trigram overlap — multi-word phrases align well."),
                   (0.15,"Some 3-word phrases match but structural divergence exists."),
                   (0.0,"Very few 3-word sequences match.")],
        "tip": "Even good paraphrases can score low on BLEU-3."
    },
    "bleu_4": {
        "title": "BLEU-4 — Standard BLEU (4-gram Precision)",
        "what":  "Industry-standard variant requiring 4-word sequence matches.",
        "ranges": [(0.5,"Excellent — near professional translation quality."),
                   (0.3,"Acceptable — captures gist but doesn't mirror reference phrasing."),
                   (0.1,"Low to moderate — room for improvement."),
                   (0.0,"Very low — candidate differs greatly from reference.")],
        "tip": "Most researchers report BLEU-4. It does NOT measure meaning, only surface overlap."
    },
    "rouge_1": {
        "title": "ROUGE-1 — Unigram F1",
        "what":  "Measures unigram overlap using F1, balancing precision and recall.",
        "ranges": [(0.6,"High vocabulary coverage — candidate includes most reference keywords."),
                   (0.35,"Moderate overlap — some keywords covered, others missing."),
                   (0.0,"Low — key words from the reference may be missing entirely.")],
        "tip": "Unlike BLEU, ROUGE measures recall — how much of the reference is covered."
    },
    "rouge_2": {
        "title": "ROUGE-2 — Bigram F1",
        "what":  "Checks 2-word phrase overlap using F1.",
        "ranges": [(0.4,"Strong phrase-level match."),
                   (0.15,"Some phrase overlap but structural differences reduce score."),
                   (0.0,"Low — ideas expressed in structurally different ways.")],
        "tip": "Gap between ROUGE-1 and ROUGE-2 reveals word-order divergence."
    },
    "rouge_l": {
        "title": "ROUGE-L — Longest Common Subsequence F1",
        "what":  "Uses LCS — longest word sequence appearing in both texts in order (not necessarily consecutive).",
        "ranges": [(0.5,"Strong sequential structure match."),
                   (0.3,"Moderate LCS overlap — some structural alignment."),
                   (0.0,"Low — sentence structure differs considerably.")],
        "tip": "More flexible than ROUGE-2 as it doesn't require consecutive phrases."
    },
}

LANGUAGE_EXAMPLES = {
    # ── Monolingual examples ──────────────────────────────────────────────────
    "English": {
        "ref":  "The quick brown fox jumps over the lazy dog near the river bank.",
        "cand": "A quick brown fox leaps over the lazy dog by the river.",
        "mode": "mono",
    },
    "Hindi": {
        "ref":  "मशीन लर्निंग एक प्रकार की कृत्रिम बुद्धिमत्ता है जो डेटा से सीखती है।",
        "cand": "मशीन लर्निंग कृत्रिम बुद्धिमत्ता का एक रूप है जो डेटा से सीखता है।",
        "mode": "mono",
    },
    "Tamil": {
        "ref":  "செயற்கை நுண்ணறிவு என்பது கணினி அமைப்புகளில் மனித அறிவை உருவகப்படுத்துகிறது.",
        "cand": "AI என்பது கணினிகளில் மனித சிந்தனையை பிரதிபலிக்கும் தொழில்நுட்பம்.",
        "mode": "mono",
    },
    "Malayalam": {
        "ref":  "കൃത്രിമ ബുദ്ധി മനുഷ്യ ചിന്തയെ അനുകരിക്കുന്ന സാങ്കേതിക വിദ്യയാണ്.",
        "cand": "AI മനുഷ്യ ബുദ്ധിയെ അനുകരിക്കുന്ന കമ്പ്യൂട്ടർ സംവിധാനമാണ്.",
        "mode": "mono",
    },
    "Telugu": {
        "ref":  "కృత్రిమ మేధస్సు మానవ తెలివిని అనుకరించే సాంకేతిక పరిజ్ఞానం.",
        "cand": "AI మానవ ఆలోచనను అనుసరించే కంప్యూటర్ సిస్టమ్.",
        "mode": "mono",
    },
    # ── English → Indian language (EN ref, Indian cand) ──────────────────────
    "EN → Hindi": {
        "ref":  "Artificial intelligence is transforming the way we live and work every day.",
        "cand": "कृत्रिम बुद्धिमत्ता हमारे जीने और काम करने के तरीके को हर दिन बदल रही है।",
        "mode": "en_to_indian",
        "lang_label": "English → Hindi",
    },
    "EN → Tamil": {
        "ref":  "Climate change is one of the greatest challenges facing humanity today.",
        "cand": "காலநிலை மாற்றம் இன்று மனிதகுலம் எதிர்கொள்ளும் மிகப்பெரிய சவால்களில் ஒன்றாகும்.",
        "mode": "en_to_indian",
        "lang_label": "English → Tamil",
    },
    "EN → Malayalam": {
        "ref":  "Education is the most powerful weapon you can use to change the world.",
        "cand": "ലോകത്തെ മാറ്റാൻ ഉപയോഗിക്കാൻ കഴിയുന്ന ഏറ്റവും ശക്തമായ ആയുധം വിദ്യാഭ്യാസമാണ്.",
        "mode": "en_to_indian",
        "lang_label": "English → Malayalam",
    },
    "EN → Telugu": {
        "ref":  "Space exploration has always been a source of wonder and scientific discovery.",
        "cand": "అంతరిక్ష అన్వేషణ ఎల్లప్పుడూ ఆశ్చర్యం మరియు శాస్త్రీయ ఆవిష్కరణల మూలంగా ఉంది.",
        "mode": "en_to_indian",
        "lang_label": "English → Telugu",
    },
    "EN → Kannada": {
        "ref":  "Technology is rapidly changing the landscape of modern agriculture.",
        "cand": "ತಂತ್ರಜ್ಞಾನವು ಆಧುನಿಕ ಕೃಷಿಯ ಸ್ವರೂಪವನ್ನು ವೇಗವಾಗಿ ಬದಲಾಯಿಸುತ್ತಿದೆ.",
        "mode": "en_to_indian",
        "lang_label": "English → Kannada",
    },
    "EN → Bengali": {
        "ref":  "The river flows gently through the green valleys of the countryside.",
        "cand": "নদীটি গ্রামাঞ্চলের সবুজ উপত্যকার মধ্য দিয়ে মৃদুভাবে প্রবাহিত হয়।",
        "mode": "en_to_indian",
        "lang_label": "English → Bengali",
    },
    # ── Indian language → English (Indian ref, EN cand) ──────────────────────
    "Hindi → EN": {
        "ref":  "भारत विविधताओं से भरा एक महान देश है जहाँ अनेक भाषाएँ और संस्कृतियाँ हैं।",
        "cand": "India is a great country full of diversity, with many languages and cultures.",
        "mode": "indian_to_en",
        "lang_label": "Hindi → English",
    },
    "Tamil → EN": {
        "ref":  "தமிழ் மொழி உலகின் மிகப் பழமையான மொழிகளில் ஒன்றாகும்.",
        "cand": "Tamil is one of the oldest languages in the world.",
        "mode": "indian_to_en",
        "lang_label": "Tamil → English",
    },
    "Malayalam → EN": {
        "ref":  "കേരളം അതിന്റെ സുന്ദരമായ ബാക്ക്‌വാട്ടറുകൾക്കും ആയുർവേദ പാരമ്പര്യത്തിനും പ്രസിദ്ധമാണ്.",
        "cand": "Kerala is famous for its beautiful backwaters and Ayurvedic tradition.",
        "mode": "indian_to_en",
        "lang_label": "Malayalam → English",
    },
    "Telugu → EN": {
        "ref":  "తెలుగు సాహిత్యం శతాబ్దాల నాటి గొప్ప చరిత్రను కలిగి ఉంది.",
        "cand": "Telugu literature has a great history spanning centuries.",
        "mode": "indian_to_en",
        "lang_label": "Telugu → English",
    },
    "Kannada → EN": {
        "ref":  "ಕರ್ನಾಟಕದ ಶಾಸ್ತ್ರೀಯ ಸಂಗೀತ ಮತ್ತು ನೃತ್ಯ ಕಲೆಗಳು ವಿಶ್ವ ಪ್ರಸಿದ್ಧವಾಗಿವೆ.",
        "cand": "Karnataka's classical music and dance arts are world-renowned.",
        "mode": "indian_to_en",
        "lang_label": "Kannada → English",
    },
    "Bengali → EN": {
        "ref":  "রবীন্দ্রনাথ ঠাকুর বাংলা সাহিত্যের সর্বশ্রেষ্ঠ কবি ও লেখক।",
        "cand": "Rabindranath Tagore is the greatest poet and writer of Bengali literature.",
        "mode": "indian_to_en",
        "lang_label": "Bengali → English",
    },
    "Custom": {"ref": "", "cand": "", "mode": "mono"},
}


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def verdict(score):
    if score >= 0.5: return "Good",  "score-good", "bar-good"
    if score >= 0.25: return "Fair", "score-fair", "bar-fair"
    return "Low", "score-low", "bar-low"

def interpret(key, score):
    for threshold, text in EXPLANATIONS.get(key, {}).get("ranges", []):
        if score >= threshold: return text
    return ""

def metric_card_html(label, score, sublabel=""):
    pct = round(score * 100, 1)
    verd, score_cls, bar_cls = verdict(score)
    sub = f'<div style="font-size:0.76rem;color:#4a6fa8;margin-top:2px">{sublabel}</div>' if sublabel else ""
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value {score_cls}">{pct}<span style="font-size:1rem;color:#4a6fa8">%</span></div>
      <div class="metric-verdict {score_cls}">⬤ {verd}</div>
      {sub}
      <div class="metric-bar-wrap">
        <div class="metric-bar-fill {bar_cls}" style="width:{pct}%"></div>
      </div>
    </div>"""

def radar_chart(bleu, rouge):
    labels = ["BLEU-1", "BLEU-2", "BLEU-3", "BLEU-4", "ROUGE-1", "ROUGE-2", "ROUGE-L"]
    values = [
        bleu["bleu_1"], bleu["bleu_2"], bleu["bleu_3"], bleu["bleu_4"],
        rouge["rouge_1"]["f1"], rouge["rouge_2"]["f1"], rouge["rouge_l"]["f1"],
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        fillcolor='rgba(56,189,248,0.12)',
        line=dict(color='#38bdf8', width=2),
        marker=dict(size=6, color='#38bdf8'),
        name="Scores",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(13,20,38,0)',
            angularaxis=dict(
                tickfont=dict(family='Space Mono', size=11, color='#6b8aad'),
                linecolor='#1e2d4a', gridcolor='#1e2d4a',
            ),
            radialaxis=dict(
                range=[0, 1], tickvals=[0.25, 0.5, 0.75, 1.0],
                tickformat='.0%', tickfont=dict(family='Space Mono', size=9, color='#3a5070'),
                linecolor='#1e2d4a', gridcolor='#1e2d4a',
            ),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=20, b=20),
        height=340,
        showlegend=False,
    )
    return fig

def bar_chart(bleu, rouge):
    labels = ["BLEU-1","BLEU-2","BLEU-3","BLEU-4","ROUGE-1 F1","ROUGE-2 F1","ROUGE-L F1"]
    values = [
        bleu["bleu_1"], bleu["bleu_2"], bleu["bleu_3"], bleu["bleu_4"],
        rouge["rouge_1"]["f1"], rouge["rouge_2"]["f1"], rouge["rouge_l"]["f1"],
    ]
    colors = ['#34d399' if v>=0.5 else '#fbbf24' if v>=0.25 else '#f87171' for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation='h',
        marker_color=colors, marker_line_width=0,
        text=[f"{v*100:.1f}%" for v in values],
        textposition='outside', textfont=dict(family='Space Mono', size=11, color='#c8d6ef'),
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0,1.15], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(tickfont=dict(family='Space Mono', size=11, color='#6b8aad'),
                   gridcolor='#1e2d4a'),
        margin=dict(l=10, r=60, t=10, b=10),
        height=280,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:1rem;font-weight:700;
    color:#38bdf8;letter-spacing:-0.5px;margin-bottom:4px;">⚡ BLEU·ROUGE</div>
    <div style="font-size:0.78rem;color:#4a6fa8;margin-bottom:24px;">NLP Evaluation Suite v2.0</div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.7rem;letter-spacing:2px;color:#2d4a6e;text-transform:uppercase;margin-bottom:8px">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    Computes <strong>BLEU-1–4</strong> and <strong>ROUGE-1, ROUGE-2, ROUGE-L</strong> scores.<br><br>
    Fully supports <strong>Indian language scripts</strong> — Hindi, Tamil, Malayalam, Telugu, Kannada, Bengali, and more.<br><br>
    Includes <strong>cross-lingual examples</strong>: English ↔ Indian languages for translation evaluation.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.7rem;letter-spacing:2px;color:#2d4a6e;text-transform:uppercase;margin:20px 0 8px">Score Guide</div>', unsafe_allow_html=True)
    for label, color, rng in [
        ("Good (≥ 50%)",  "#34d399", "Strong surface-form agreement"),
        ("Fair (25–49%)", "#fbbf24", "Moderate overlap"),
        ("Low (< 25%)",   "#f87171", "Significant divergence"),
    ]:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;font-size:0.82rem;color:#7ea8cc">
          <div style="width:8px;height:8px;border-radius:50%;background:{color};flex-shrink:0"></div>
          <div><b style="color:{color}">{label}</b><br><span style="font-size:0.75rem">{rng}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#2d4a6e;line-height:1.7">
    Pure-Python implementation · No external NLP libs required · Unicode-aware tokeniser
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero-header">
  <div class="hero-title">BLEU & ROUGE <span>Scorer</span></div>
  <div class="hero-sub">Automatic evaluation metrics for NLP — translation, summarisation & generation</div>
  <div>
    <span class="badge">BLEU-1 → 4</span>
    <span class="badge">ROUGE-1 / 2 / L</span>
    <span class="badge">Indic Scripts</span>
    <span class="badge">EN ↔ Indian</span>
    <span class="badge">Batch Mode</span>
    <span class="badge">JSON Export</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════

tab_single, tab_batch, tab_compare, tab_improve = st.tabs(["  Single Pair  ", "  Batch Mode  ", "  Score Glossary  ", "  💡 Improve Scores  "])


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 1 — SINGLE PAIR
# ─────────────────────────────────────────────────────────────────────────────

with tab_single:
    # ── Translation direction filter + example picker ──────────────────────
    st.markdown('<div class="section-title">Load Example</div>', unsafe_allow_html=True)

    DIRECTION_GROUPS = {
        "Monolingual (same language)": [k for k, v in LANGUAGE_EXAMPLES.items() if v.get("mode") == "mono"],
        "English → Indian Language":   [k for k, v in LANGUAGE_EXAMPLES.items() if v.get("mode") == "en_to_indian"],
        "Indian Language → English":   [k for k, v in LANGUAGE_EXAMPLES.items() if v.get("mode") == "indian_to_en"],
        "Custom":                       ["Custom"],
    }

    dir_col, lang_col = st.columns([2, 3])
    with dir_col:
        direction = st.selectbox(
            "Translation direction",
            list(DIRECTION_GROUPS.keys()),
            index=0,
        )
    with lang_col:
        available = DIRECTION_GROUPS[direction]
        lang_choice = st.selectbox(
            "Load a built-in example",
            available,
            index=0,
        )

    ex = LANGUAGE_EXAMPLES[lang_choice]

    # Derive text-area labels based on direction mode
    _mode = ex.get("mode", "mono")
    if _mode == "en_to_indian":
        _lang_label = ex.get("lang_label", lang_choice)
        ref_label  = f"Reference Text  — English  (ground-truth)"
        cand_label = f"Candidate Text  — {_lang_label.split('→')[1].strip()}  (model output)"
    elif _mode == "indian_to_en":
        _lang_label = ex.get("lang_label", lang_choice)
        ref_label  = f"Reference Text  — {_lang_label.split('→')[0].strip()}  (ground-truth)"
        cand_label = f"Candidate Text  — English  (model output)"
    else:
        ref_label  = "Reference Text  (expected / ground-truth)"
        cand_label = "Candidate Text  (model output / hypothesis)"

    # Show a contextual hint for cross-lingual pairs
    if _mode in ("en_to_indian", "indian_to_en"):
        st.markdown("""
        <div class="info-box" style="margin-bottom:14px">
        <strong>Cross-lingual mode:</strong> BLEU &amp; ROUGE measure <em>token-surface overlap</em>.
        For cross-lingual pairs the reference and candidate share <em>no</em> tokens, so scores will
        be near <strong>0</strong> — this is expected. Use these examples to test your tokeniser
        or to verify your translated output matches a bilingual reference sentence exactly.
        </div>""", unsafe_allow_html=True)

    # Input area
    col_ref, col_cand = st.columns(2, gap="medium")
    with col_ref:
        ref_text = st.text_area(
            ref_label,
            value=ex["ref"],
            height=130,
            placeholder="Paste your reference sentence here…",
        )
    with col_cand:
        cand_text = st.text_area(
            cand_label,
            value=ex["cand"],
            height=130,
            placeholder="Paste the generated / translated text here…",
        )

    col_btn, col_exp = st.columns([2, 3])
    with col_btn:
        run_btn = st.button("⚡  Compute Scores", use_container_width=True)
    with col_exp:
        show_explain = st.checkbox("Show metric explanations", value=True)

    if run_btn:
        if not ref_text.strip() or not cand_text.strip():
            st.error("Both Reference and Candidate texts are required.")
        else:
            bleu  = compute_bleu(cand_text, ref_text)
            rouge = compute_rouge(cand_text, ref_text)

            # ── Token stats bar ──
            bp = bleu["brevity_penalty"]
            bp_flag = " ⚠ penalty applied" if bp < 1.0 else " ✓ no penalty"
            st.markdown(f"""
            <div class="stat-row">
              <div class="stat-pill">Reference tokens: <b>{bleu['reference_length']}</b></div>
              <div class="stat-pill">Candidate tokens: <b>{bleu['candidate_length']}</b></div>
              <div class="stat-pill">Brevity penalty: <b>{bp:.4f}</b><span style="color:#{'fbbf24' if bp<1 else '34d399'};font-size:0.75rem"> {bp_flag}</span></div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-title">BLEU Scores</div>', unsafe_allow_html=True)
            b_cols = st.columns(4, gap="small")
            for i, (col, key, label) in enumerate(zip(b_cols,
                    ["bleu_1","bleu_2","bleu_3","bleu_4"],
                    ["BLEU-1  Unigram","BLEU-2  Bigram","BLEU-3  Trigram","BLEU-4  ★ Standard"])):
                with col:
                    st.markdown(metric_card_html(label, bleu[key]), unsafe_allow_html=True)
                    if show_explain:
                        interp = interpret(key, bleu[key])
                        if interp:
                            with st.expander("Details"):
                                st.markdown(f"**{EXPLANATIONS[key]['title']}**")
                                st.markdown(f"{EXPLANATIONS[key]['what']}")
                                st.markdown(f"*{interp}*")
                                st.caption(f"💡 {EXPLANATIONS[key]['tip']}")

            st.markdown('<div class="section-title">ROUGE Scores</div>', unsafe_allow_html=True)
            r_cols = st.columns(3, gap="small")
            for col, key, label in zip(r_cols,
                    ["rouge_1","rouge_2","rouge_l"],
                    ["ROUGE-1  Unigram F1","ROUGE-2  Bigram F1","ROUGE-L  LCS F1"]):
                m = rouge[key]
                with col:
                    sub = f"P: {m['precision']*100:.1f}%  ·  R: {m['recall']*100:.1f}%"
                    if key == "rouge_l":
                        sub += f"  ·  LCS: {m['lcs_length']} tokens"
                    st.markdown(metric_card_html(label, m["f1"], sublabel=sub), unsafe_allow_html=True)
                    if show_explain:
                        interp = interpret(key, m["f1"])
                        if interp:
                            with st.expander("Details"):
                                st.markdown(f"**{EXPLANATIONS[key]['title']}**")
                                st.markdown(f"{EXPLANATIONS[key]['what']}")
                                st.markdown(f"*{interp}*")
                                st.caption(f"💡 {EXPLANATIONS[key]['tip']}")

            # ── Charts ──
            st.markdown('<div class="section-title">Visualisation</div>', unsafe_allow_html=True)
            vcol1, vcol2 = st.columns([1, 1], gap="medium")
            with vcol1:
                st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.7rem;color:#4a6fa8;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">Radar Overview</div>', unsafe_allow_html=True)
                st.plotly_chart(radar_chart(bleu, rouge), use_container_width=True, config={"displayModeBar": False})
            with vcol2:
                st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.7rem;color:#4a6fa8;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px">Bar Breakdown</div>', unsafe_allow_html=True)
                st.plotly_chart(bar_chart(bleu, rouge), use_container_width=True, config={"displayModeBar": False})

            # ── Export ──
            st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
            result_json = json.dumps({
                "reference": ref_text, "candidate": cand_text,
                "bleu": bleu, "rouge": rouge
            }, ensure_ascii=False, indent=2)
            st.download_button(
                label="⬇  Download JSON",
                data=result_json,
                file_name="bleu_rouge_scores.json",
                mime="application/json",
            )

            # ── Smart improvement tips (context-aware) ──
            st.markdown('<div class="section-title">💡 How to Improve These Scores</div>', unsafe_allow_html=True)

            bleu4   = bleu["bleu_4"]
            r1      = rouge["rouge_1"]["f1"]
            r2      = rouge["rouge_2"]["f1"]
            rl      = rouge["rouge_l"]["f1"]
            bp      = bleu["brevity_penalty"]
            prec_r1 = rouge["rouge_1"]["precision"]
            rec_r1  = rouge["rouge_1"]["recall"]

            tips = []

            # Brevity penalty tip
            if bp < 0.9:
                tips.append(("⚠️ Candidate too short", "#fbbf24",
                    f"Your brevity penalty is <b>{bp:.3f}</b> — the candidate is significantly shorter than the reference. "
                    "Try generating longer, more complete outputs. Truncating or summarising too aggressively hurts BLEU."))

            # Low BLEU-1 → word choice
            if bleu["bleu_1"] < 0.4:
                tips.append(("🔤 Word choice mismatch", "#f87171",
                    "BLEU-1 (unigram) is low — the candidate uses words that rarely appear in the reference. "
                    "Check your vocabulary: use the same terminology as the reference domain. "
                    "For MT, fine-tune on in-domain parallel data."))

            # Good BLEU-1 but low BLEU-2/3 → word order
            elif bleu["bleu_1"] >= 0.4 and bleu["bleu_2"] < 0.25:
                tips.append(("🔀 Word order issues", "#fbbf24",
                    "Individual words match (BLEU-1 is okay) but bigrams/trigrams don't — word order likely differs. "
                    "Focus on syntactic fluency: reordering, better beam search, or a reranking step."))

            # Low BLEU-4 specifically
            if bleu4 < 0.2:
                tips.append(("📐 Phrase-level divergence (BLEU-4)", "#f87171",
                    "BLEU-4 is very low. Four-gram matches are rare, meaning the candidate phrasing diverges strongly. "
                    "Use larger beam sizes during decoding, add phrase-table coverage in SMT, "
                    "or fine-tune with more domain-specific examples."))

            # Precision >> Recall → candidate too generic / short
            if prec_r1 > rec_r1 + 0.2:
                tips.append(("📉 Low recall — missing reference content", "#fbbf24",
                    f"ROUGE-1 Precision ({prec_r1*100:.1f}%) is much higher than Recall ({rec_r1*100:.1f}%). "
                    "The candidate is precise but misses key content from the reference. "
                    "Increase output length or coverage — add more detail, named entities, or key phrases."))

            # Recall >> Precision → candidate too verbose / hallucinating
            if rec_r1 > prec_r1 + 0.2:
                tips.append(("📈 Low precision — noisy / verbose candidate", "#fbbf24",
                    f"ROUGE-1 Recall ({rec_r1*100:.1f}%) is much higher than Precision ({prec_r1*100:.1f}%). "
                    "The candidate covers the reference content but adds extra words not in the reference. "
                    "Reduce hallucination, trim filler phrases, or tune length penalty."))

            # ROUGE-1 good but ROUGE-2 low → phrase structure
            if r1 >= 0.4 and r2 < 0.2:
                tips.append(("🧩 Weak phrase structure (ROUGE-2)", "#fbbf24",
                    "Unigrams overlap well but bigrams don't. The words are right but not in the right order or combination. "
                    "Work on fluency: coherent sentence structure, better language model, or post-editing."))

            # ROUGE-L much lower than ROUGE-1 → fragmented output
            if r1 - rl > 0.2:
                tips.append(("🔗 Fragmented output (ROUGE-L gap)", "#f87171",
                    f"ROUGE-1 ({r1*100:.1f}%) is much higher than ROUGE-L ({rl*100:.1f}%). "
                    "Matching words exist but not in the same sequential order. "
                    "Improve sentence-level coherence — the overall structure of the output diverges from the reference."))

            # All scores good
            if bleu4 >= 0.5 and r1 >= 0.6:
                tips.append(("✅ Scores look strong!", "#34d399",
                    "BLEU-4 and ROUGE-1 are both high. For further gains: use multiple references, "
                    "add semantic metrics (BERTScore, chrF), and always complement with human evaluation."))

            # Generic always-on tips
            tips.append(("📚 General best practices", "#38bdf8",
                "<b>1. Use multiple references</b> — BLEU/ROUGE measure surface overlap; more references = fairer evaluation.<br>"
                "<b>2. Domain-specific training data</b> — Models trained on in-domain text produce outputs closer to reference phrasing.<br>"
                "<b>3. Beam search tuning</b> — Larger beam sizes (e.g. 10–20) often improve BLEU scores at inference time.<br>"
                "<b>4. Post-editing / reranking</b> — Rerank N-best outputs using a language model score + BLEU proxy.<br>"
                "<b>5. These metrics have limits</b> — A semantically perfect paraphrase can score 0. Always use human eval alongside."))

            for title, color, body in tips:
                st.markdown(f"""
                <div style="background:rgba(13,20,38,0.8);border:1px solid {color}33;border-left:3px solid {color};
                     border-radius:10px;padding:14px 18px;margin-bottom:10px;">
                  <div style="font-family:'Space Mono',monospace;font-size:0.75rem;color:{color};
                       font-weight:700;letter-spacing:0.5px;margin-bottom:6px">{title}</div>
                  <div style="font-size:0.85rem;color:#93b4d4;line-height:1.65">{body}</div>
                </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 2 — BATCH MODE
# ─────────────────────────────────────────────────────────────────────────────

with tab_batch:
    st.markdown("""
    <div class="info-box">
    Upload two <strong>line-aligned plain-text files</strong> — one reference sentence per line,
    one candidate sentence per line. Each line is scored as a pair.
    </div>""", unsafe_allow_html=True)

    bcol1, bcol2 = st.columns(2, gap="medium")
    with bcol1:
        ref_file  = st.file_uploader("Reference file (.txt)", type=["txt"])
    with bcol2:
        cand_file = st.file_uploader("Candidate file (.txt)", type=["txt"])

    batch_btn = st.button("⚡  Run Batch Scoring", use_container_width=False)

    if batch_btn:
        if not ref_file or not cand_file:
            st.error("Please upload both files.")
        else:
            refs  = [l for l in ref_file.read().decode("utf-8").splitlines() if l.strip()]
            cands = [l for l in cand_file.read().decode("utf-8").splitlines() if l.strip()]

            if len(refs) != len(cands):
                st.error(f"Line count mismatch: {len(refs)} references vs {len(cands)} candidates.")
            else:
                all_results = []
                totals = {k: 0.0 for k in ["bleu_1","bleu_2","bleu_3","bleu_4","r1_f1","r2_f1","rl_f1"]}
                rows = []

                progress = st.progress(0, text="Scoring pairs…")
                for i, (ref, cand) in enumerate(zip(refs, cands)):
                    b = compute_bleu(cand, ref)
                    r = compute_rouge(cand, ref)
                    totals["bleu_1"] += b["bleu_1"]; totals["bleu_2"] += b["bleu_2"]
                    totals["bleu_3"] += b["bleu_3"]; totals["bleu_4"] += b["bleu_4"]
                    totals["r1_f1"] += r["rouge_1"]["f1"]; totals["r2_f1"] += r["rouge_2"]["f1"]
                    totals["rl_f1"] += r["rouge_l"]["f1"]
                    rows.append({
                        "Pair": i+1,
                        "BLEU-1": b["bleu_1"], "BLEU-2": b["bleu_2"],
                        "BLEU-3": b["bleu_3"], "BLEU-4 ★": b["bleu_4"],
                        "ROUGE-1": r["rouge_1"]["f1"], "ROUGE-2": r["rouge_2"]["f1"],
                        "ROUGE-L": r["rouge_l"]["f1"],
                    })
                    all_results.append({"pair":i+1,"reference":ref,"candidate":cand,"bleu":b,"rouge":r})
                    progress.progress((i+1)/len(refs), text=f"Scoring pair {i+1}/{len(refs)}…")

                progress.empty()
                n = len(refs)
                avgs = {k: v/n for k, v in totals.items()}

                # Average chips
                st.markdown(f"""
                <div class="batch-summary">
                  <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#4a6fa8;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px">
                    Corpus Averages — {n} pairs
                  </div>
                  <div>
                    <span class="avg-chip">BLEU-1 <span>{avgs['bleu_1']*100:.1f}%</span></span>
                    <span class="avg-chip">BLEU-2 <span>{avgs['bleu_2']*100:.1f}%</span></span>
                    <span class="avg-chip">BLEU-3 <span>{avgs['bleu_3']*100:.1f}%</span></span>
                    <span class="avg-chip">BLEU-4 <span>{avgs['bleu_4']*100:.1f}%</span></span>
                    <span class="avg-chip">ROUGE-1 <span>{avgs['r1_f1']*100:.1f}%</span></span>
                    <span class="avg-chip">ROUGE-2 <span>{avgs['r2_f1']*100:.1f}%</span></span>
                    <span class="avg-chip">ROUGE-L <span>{avgs['rl_f1']*100:.1f}%</span></span>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Per-pair table
                df = pd.DataFrame(rows).set_index("Pair")

                def color_cell(val):
                    if val >= 0.5: return 'color: #34d399'
                    if val >= 0.25: return 'color: #fbbf24'
                    return 'color: #f87171'

                styled = (df.style
                          .format("{:.4f}")
                          .applymap(color_cell)
                          .set_properties(**{
                              'background-color': '#0d1426',
                              'border': '1px solid #1e2d4a',
                              'font-family': 'Space Mono, monospace',
                              'font-size': '0.78rem',
                          })
                          .set_table_styles([{
                              'selector': 'th',
                              'props': [('background-color','#090e1c'),
                                        ('color','#4a6fa8'),
                                        ('font-family','Space Mono, monospace'),
                                        ('font-size','0.72rem'),
                                        ('letter-spacing','1px')]
                          }]))
                st.dataframe(styled, use_container_width=True, height=380)

                # Corpus-level radar
                pseudo_bleu = {"bleu_1":avgs["bleu_1"],"bleu_2":avgs["bleu_2"],
                               "bleu_3":avgs["bleu_3"],"bleu_4":avgs["bleu_4"]}
                pseudo_rouge = {"rouge_1":{"f1":avgs["r1_f1"]},
                                "rouge_2":{"f1":avgs["r2_f1"]},
                                "rouge_l":{"f1":avgs["rl_f1"]}}
                st.markdown('<div class="section-title">Corpus-Level Radar</div>', unsafe_allow_html=True)
                st.plotly_chart(radar_chart(pseudo_bleu, pseudo_rouge), use_container_width=True,
                                config={"displayModeBar": False})

                # JSON export
                batch_json = json.dumps({
                    "pairs": all_results,
                    "averages": {k: round(v, 4) for k, v in avgs.items()}
                }, ensure_ascii=False, indent=2)
                st.download_button("⬇  Download Full Results (JSON)", batch_json,
                                   "batch_results.json", "application/json")


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 3 — SCORE GLOSSARY
# ─────────────────────────────────────────────────────────────────────────────

with tab_compare:
    st.markdown('<div class="section-title">Metric Reference</div>', unsafe_allow_html=True)

    for key, ex in EXPLANATIONS.items():
        with st.expander(f"📐  {ex['title']}"):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.markdown(f"**What it measures:** {ex['what']}")
                st.markdown("**Score ranges:**")
                for threshold, desc in ex["ranges"]:
                    pct = f"{int(threshold*100)}%"
                    verd, cls, _ = verdict(threshold)
                    col_map = {"score-good":"🟢","score-fair":"🟡","score-low":"🔴"}
                    st.markdown(f"{col_map[cls]} **≥ {pct}** — {desc}")
                st.caption(f"💡 {ex['tip']}")
            with c2:
                st.markdown("**Quick verdicts:**")
                for score_val, label in [(0.75,"0.75"),(0.50,"0.50"),(0.35,"0.35"),(0.15,"0.15")]:
                    v, cls, _ = verdict(score_val)
                    color = {"score-good":"#34d399","score-fair":"#fbbf24","score-low":"#f87171"}[cls]
                    st.markdown(f"""<span style="font-family:'Space Mono',monospace;color:{color}">{label}</span>
                    <span style="color:#4a6fa8;font-size:0.82rem"> → {v}</span>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">BLEU vs ROUGE — At a Glance</div>', unsafe_allow_html=True)
    compare_data = {
        "Dimension":  ["Focus","Direction","Common use","Scores 0–1","Needs reference"],
        "BLEU":       ["Precision","Candidate → Reference","MT / Generation","Yes","Yes"],
        "ROUGE":      ["Recall + F1","Reference → Candidate","Summarisation","Yes","Yes"],
    }
    df_cmp = pd.DataFrame(compare_data).set_index("Dimension")
    st.dataframe(df_cmp, use_container_width=True)

    st.markdown("""
    <div class="info-box" style="margin-top:16px">
    <strong>Important caveats:</strong> Both BLEU and ROUGE measure <em>surface-form overlap</em>, not semantic
    similarity or factual correctness. A perfect paraphrase can score near zero. Always interpret scores
    alongside human evaluation.
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  TAB 4 — IMPROVE YOUR SCORES
# ─────────────────────────────────────────────────────────────────────────────

with tab_improve:

    st.markdown("""
    <div class="info-box">
    A practical guide to improving <strong>BLEU</strong> and <strong>ROUGE</strong> scores — covering
    model training, decoding strategies, data quality, and the limits of these metrics.
    </div>""", unsafe_allow_html=True)

    # ── Quick diagnosis tool ──────────────────────────────────────────────────
    st.markdown('<div class="section-title">🔍 Quick Score Diagnosis</div>', unsafe_allow_html=True)

    diag_col1, diag_col2, diag_col3 = st.columns(3, gap="small")
    with diag_col1:
        diag_bleu = st.slider("Your BLEU-4 score", 0.0, 1.0, 0.25, 0.01, format="%.2f")
    with diag_col2:
        diag_r1   = st.slider("Your ROUGE-1 score", 0.0, 1.0, 0.40, 0.01, format="%.2f")
    with diag_col3:
        diag_task = st.selectbox("Task type", ["Machine Translation", "Summarisation", "Text Generation", "Indian Language MT"])

    # Diagnosis logic
    diag_tips = []

    if diag_task == "Machine Translation":
        if diag_bleu < 0.15:
            diag_tips.append(("🔴 Very low BLEU for MT", "Below 15% BLEU is typical of rule-based or untrained systems. Focus on: (1) getting a baseline NMT model running, (2) ensuring your tokeniser handles the language correctly, (3) checking for encoding issues in your data pipeline."))
        elif diag_bleu < 0.3:
            diag_tips.append(("🟡 Developing MT quality", "15–30% BLEU is early-stage NMT. Key improvements: more parallel training data, domain adaptation, subword tokenisation (BPE/SentencePiece), and larger beam search at inference."))
        elif diag_bleu < 0.5:
            diag_tips.append(("🟡 Moderate MT quality", "30–50% BLEU is competitive but below human quality. Try: ensemble decoding, minimum Bayes risk decoding, back-translation for data augmentation, and length normalisation."))
        else:
            diag_tips.append(("🟢 Strong MT quality", "50%+ BLEU is near human-level for many language pairs. Fine-tune with in-domain data, try reranking with a language model, and evaluate with chrF/TER alongside BLEU."))

    elif diag_task == "Summarisation":
        if diag_r1 < 0.3:
            diag_tips.append(("🔴 Low ROUGE for summarisation", "Below 30% ROUGE-1 suggests the summary misses key content. Ensure extractive coverage of key sentences, increase summary length, and check if the model is hallucinating content not in the source."))
        elif diag_r1 < 0.45:
            diag_tips.append(("🟡 Developing summarisation quality", "30–45% ROUGE-1 is typical for abstractive summarisation. Improve with: fine-tuning on domain data, coverage mechanisms, and explicit length targets."))
        else:
            diag_tips.append(("🟢 Strong summarisation quality", "45%+ ROUGE-1 is competitive. For further gains: use oracle sentence selection as upper bound analysis, try contrastive learning objectives, and evaluate factual consistency separately."))

    elif diag_task == "Indian Language MT":
        diag_tips.append(("🌐 Indian Language MT specific advice",
            "BLEU scores for Indian languages are typically lower than for European pairs due to: "
            "(1) morphological richness — words inflect heavily, so surface overlap is harder. "
            "(2) script differences — ensure your tokeniser handles Unicode Devanagari/Tamil/etc. correctly. "
            "(3) data scarcity — use IndicCorp, Samanantar, or AI4Bharat datasets. "
            "(4) subword models — BPE or SentencePiece with a shared vocabulary significantly helps low-resource pairs."))
        if diag_bleu < 0.2:
            diag_tips.append(("💡 Start with IndicTrans2", "For Indian language MT, IndicTrans2 (AI4Bharat) is the current state-of-the-art baseline. Fine-tuning it on your domain data will give a much stronger starting point than training from scratch."))

    else:  # Text Generation
        if diag_r1 < 0.35:
            diag_tips.append(("🔴 Low overlap for generation", "Surface-form metrics are hard to improve for open-ended generation — the model may be semantically correct but phrased differently. Consider: constrained generation (forced keywords), retrieval-augmented generation, or switching to semantic metrics like BERTScore."))
        else:
            diag_tips.append(("🟡 Generation quality note", "For open-ended text generation, ROUGE/BLEU have limited meaning. A high score can mean the model is copying; a low score can still mean a great output. Use human evaluation or G-Eval alongside these metrics."))

    for title, body in diag_tips:
        st.markdown(f"""
        <div style="background:#0d1426;border:1px solid #1e3a5f;border-radius:10px;
             padding:16px 20px;margin-bottom:10px;">
          <div style="font-family:'Space Mono',monospace;font-size:0.78rem;color:#38bdf8;
               font-weight:700;margin-bottom:8px">{title}</div>
          <div style="font-size:0.85rem;color:#93b4d4;line-height:1.7">{body}</div>
        </div>""", unsafe_allow_html=True)

    # ── The 5 pillars ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📋 The 5 Pillars of Better Scores</div>', unsafe_allow_html=True)

    PILLARS = [
        {
            "icon": "🗂️", "title": "1. Data Quality & Quantity",
            "color": "#38bdf8",
            "points": [
                ("More parallel data", "The single biggest lever. More in-domain parallel sentences = better coverage of reference phrasing."),
                ("Clean your corpus", "Remove duplicate pairs, misaligned sentences, and encoding errors. A small clean dataset beats a large noisy one."),
                ("Back-translation", "Generate synthetic source sentences from monolingual target data. Highly effective for low-resource languages including Indian languages."),
                ("Domain adaptation", "Fine-tune on domain-specific data (medical, legal, news). General-purpose models score lower on specialised references."),
            ]
        },
        {
            "icon": "🧮", "title": "2. Tokenisation",
            "color": "#a78bfa",
            "points": [
                ("Use subword tokenisation", "BPE or SentencePiece prevents unknown tokens and handles morphologically rich languages (Hindi, Tamil, Telugu) far better than whitespace splitting."),
                ("Consistent tokeniser", "The tokeniser used at evaluation must match training. Mismatches directly reduce measured scores."),
                ("Script-aware tokenisation", "For Indian scripts, ensure your tokeniser handles Unicode correctly — use IndicNLP or SentencePiece trained on Indic text."),
                ("Normalise before scoring", "Unicode normalisation (NFC/NFKC) and consistent punctuation handling prevent spurious token mismatches."),
            ]
        },
        {
            "icon": "⚙️", "title": "3. Decoding Strategy",
            "color": "#34d399",
            "points": [
                ("Increase beam size", "Beam search with width 10–20 typically improves BLEU over greedy (width 1) at modest speed cost."),
                ("Length normalisation", "Divide beam scores by output length to avoid short-output bias (brevity penalty in BLEU)."),
                ("Minimum Bayes Risk (MBR)", "Instead of the highest-scoring beam, pick the candidate with highest average similarity to all beams. Consistently outperforms MAP decoding on BLEU."),
                ("Ensemble decoding", "Average logits from multiple model checkpoints. Often gains +1–2 BLEU at inference time."),
            ]
        },
        {
            "icon": "🏋️", "title": "4. Model Training",
            "color": "#fbbf24",
            "points": [
                ("Label smoothing", "Smoothing factor 0.1 is standard in NMT and prevents overconfidence, improving generalisation."),
                ("Larger model capacity", "Transformer-big vs Transformer-base typically gives +2–4 BLEU on standard benchmarks."),
                ("Longer training / learning rate schedule", "Under-trained models score low. Use a warmup + inverse square root or cosine decay schedule."),
                ("Checkpoint averaging", "Average the last 5–10 checkpoints. Almost free BLEU improvement with no extra training."),
            ]
        },
        {
            "icon": "📏", "title": "5. Evaluation Setup",
            "color": "#f87171",
            "points": [
                ("Use multiple references", "Official BLEU supports multiple references per source — scores rise significantly with 2–4 references."),
                ("Corpus-level vs sentence-level", "Always report corpus-level BLEU (not averaged sentence BLEU) — it's more stable and the standard in MT papers."),
                ("Use sacreBleu", "For reproducible, comparable BLEU scores use the sacreBleu library which standardises tokenisation."),
                ("Complement with other metrics", "chrF correlates better with human judgement for morphologically rich languages. BERTScore captures semantics. Always use 2–3 metrics."),
            ]
        },
    ]

    for pillar in PILLARS:
        with st.expander(f"{pillar['icon']}  {pillar['title']}"):
            for point_title, point_body in pillar["points"]:
                st.markdown(f"""
                <div style="display:flex;gap:12px;margin-bottom:12px;align-items:flex-start">
                  <div style="width:6px;height:6px;border-radius:50%;background:{pillar['color']};
                       flex-shrink:0;margin-top:6px"></div>
                  <div>
                    <span style="color:{pillar['color']};font-weight:600;font-size:0.85rem">{point_title}</span>
                    <span style="color:#7ea8cc;font-size:0.84rem"> — {point_body}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── Score benchmarks table ─────────────────────────────────────────────────
    st.markdown('<div class="section-title">🎯 Score Benchmarks by Task</div>', unsafe_allow_html=True)
    bench_data = {
        "Task":         ["MT (high-resource, e.g. EN-DE)", "MT (low-resource)", "MT (Indian languages)", "Abstractive Summarisation", "Extractive Summarisation", "Text Generation (open-ended)"],
        "BLEU-4 range": ["30–45%", "10–25%", "15–30%", "5–20%", "15–30%", "2–15%"],
        "ROUGE-1 range":["45–65%", "30–50%", "35–55%", "35–50%", "45–60%", "25–45%"],
        "Notes":        ["SacreBLEU standard", "Back-translation helps", "IndicTrans2 baseline", "Abstractive paraphrase hurts", "Near-extractive copies score high", "Metric less meaningful here"],
    }
    df_bench = pd.DataFrame(bench_data).set_index("Task")
    st.dataframe(df_bench, use_container_width=True)

    # ── Common mistakes ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">❌ Common Mistakes That Hurt Scores</div>', unsafe_allow_html=True)

    MISTAKES = [
        ("Tokeniser mismatch at eval time", "Training with BPE but evaluating on raw whitespace-split tokens. Always use the same tokeniser."),
        ("Evaluating on sentence-level BLEU average", "Averaging per-sentence BLEU scores is not the same as corpus BLEU. Use corpus-level computation."),
        ("Not normalising Unicode", "Mixed Unicode forms (NFC vs NFD) for Indian scripts create spurious token mismatches that lower scores artificially."),
        ("Short candidate outputs", "Short outputs trigger BLEU's brevity penalty hard. Ensure your model's length bias is tuned."),
        ("Using only one reference", "A single reference is a weak proxy. Where possible collect 2–4 human translations as references."),
        ("Treating 0% cross-lingual score as a bug", "EN→Hindi BLEU is always 0 — no token overlap across scripts. Use chrF for character-level cross-lingual evaluation instead."),
    ]

    mc1, mc2 = st.columns(2, gap="medium")
    for i, (mistake, fix) in enumerate(MISTAKES):
        col = mc1 if i % 2 == 0 else mc2
        with col:
            st.markdown(f"""
            <div style="background:#0d1426;border:1px solid #3a1a1a;border-left:3px solid #f87171;
                 border-radius:10px;padding:14px 16px;margin-bottom:10px;">
              <div style="color:#f87171;font-size:0.82rem;font-weight:600;margin-bottom:4px">✗ {mistake}</div>
              <div style="color:#93b4d4;font-size:0.82rem;line-height:1.6">✓ {fix}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
.footer-bar {
    margin-top: 48px;
    padding: 18px 0 10px;
    border-top: 1px solid #1e2d4a;
    text-align: center;
}
.footer-inner {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 0.82rem;
    color: #4a6fa8;
    font-family: 'DM Sans', sans-serif;
}
.footer-inner a {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #38bdf8;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.2s;
}
.footer-inner a:hover { color: #7dd3fc; }
.footer-inner svg { vertical-align: middle; }
</style>

<div class="footer-bar">
  <div class="footer-inner">
    <span>Developed by</span>
    <a href="https://github.com/yaduk883/" target="_blank" rel="noopener noreferrer">
      <svg height="18" width="18" viewBox="0 0 16 16" fill="#38bdf8" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
          0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13
          -.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66
          .07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15
          -.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.66 7.66 0 0 1 2-.27
          c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12
          .51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48
          0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8
          c0-4.42-3.58-8-8-8z"/>
      </svg>
      yadu
    </a>
  </div>
</div>
""", unsafe_allow_html=True)