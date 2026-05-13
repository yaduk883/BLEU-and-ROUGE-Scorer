# ⚡ BLEU & ROUGE Scorer

A sleek, fully self-contained **Streamlit web app** for evaluating NLP model outputs using BLEU and ROUGE metrics — with first-class support for **Indian language scripts** and **English ↔ Indian language translation** pairs.

> Developed by [yadu](https://github.com/yaduk883/)

---

## ✨ Features

### 📊 Metrics
- **BLEU-1, BLEU-2, BLEU-3, BLEU-4** with brevity penalty
- **ROUGE-1, ROUGE-2, ROUGE-L** (Precision, Recall, F1)
- Visual metric cards with colour-coded verdicts (Good / Fair / Low)
- Radar and bar chart visualisations

### 🌐 Language Support
- Full **Unicode-aware tokeniser** — no external NLP libraries required
- Built-in monolingual examples: **English, Hindi, Tamil, Malayalam, Telugu**
- Built-in **cross-lingual translation examples**:
  - English → Hindi, Tamil, Malayalam, Telugu, Kannada, Bengali
  - Hindi, Tamil, Malayalam, Telugu, Kannada, Bengali → English
- Translation direction selector with contextual hints for cross-lingual pairs

### 💡 Improve Your Scores
- **Smart inline tips** — after every scoring run, context-aware cards diagnose your results and explain exactly what to fix
- **Dedicated "Improve Scores" tab** with:
  - Interactive Quick Diagnosis tool (slider-based, task-aware)
  - The 5 Pillars guide: Data, Tokenisation, Decoding, Training, Evaluation
  - Score benchmark table by task type
  - Common mistakes & fixes reference

### 🗂️ Modes
| Mode | Description |
|------|-------------|
| **Single Pair** | Score one reference–candidate pair with full breakdown |
| **Batch Mode** | Upload two line-aligned `.txt` files; scores every pair |
| **Score Glossary** | Explains each metric, score ranges, and BLEU vs ROUGE |
| **Improve Scores** | Actionable guide to raising your scores |

### 📤 Export
- Download results as **JSON** (single pair or full batch)
- Batch mode includes per-pair scores + corpus averages

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yaduk883/bleu-rouge-scorer.git
cd bleu-rouge-scorer

# 2. Install dependencies
pip install streamlit plotly pandas

# 3. Run the app
streamlit run bleu_rouge_scorer.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `plotly` | Radar & bar charts |
| `pandas` | Batch results table |

> **No external NLP libraries required.** BLEU and ROUGE are implemented in pure Python with a Unicode-aware tokeniser.

---

## 🧮 How Scores Are Computed

### BLEU (Bilingual Evaluation Understudy)
BLEU measures **n-gram precision** of the candidate against the reference, with a brevity penalty for short outputs.

```
BLEU-N = BP × exp( (1/N) × Σ log precision_n )
BP     = 1  if |candidate| ≥ |reference|
       = exp(1 - |reference| / |candidate|)  otherwise
```

This implementation uses **add-1 smoothing** to handle zero n-gram counts for short sentences.

### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
ROUGE measures **recall** of reference n-grams in the candidate, reported as F1.

- **ROUGE-1** — unigram overlap
- **ROUGE-2** — bigram overlap
- **ROUGE-L** — Longest Common Subsequence (LCS)

---

## 📁 Project Structure

```
bleu-rouge-scorer/
│
├── bleu_rouge_scorer.py   # Main app — all logic and UI in one file
└── README.md
```

---

## 🌍 Cross-lingual Evaluation Note

BLEU and ROUGE measure **token surface overlap**. When evaluating English → Indian language translation (or vice versa), scores will be near **0** because the scripts share no tokens. This is expected behaviour — not a bug.

For cross-lingual evaluation, consider:
- **chrF** (character n-gram F-score) — works across scripts
- **BERTScore** — semantic similarity using multilingual embeddings
- **IndicEval** toolkits from [AI4Bharat](https://ai4bharat.org/)

---

## 🎯 Score Benchmarks

| Task | Typical BLEU-4 | Typical ROUGE-1 |
|------|---------------|-----------------|
| MT (high-resource, e.g. EN-DE) | 30–45% | 45–65% |
| MT (low-resource) | 10–25% | 30–50% |
| MT (Indian languages) | 15–30% | 35–55% |
| Abstractive Summarisation | 5–20% | 35–50% |
| Extractive Summarisation | 15–30% | 45–60% |
| Open-ended Text Generation | 2–15% | 25–45% |

---

## 💡 Quick Tips to Improve Scores

1. **More in-domain parallel data** — the single biggest lever for MT
2. **Subword tokenisation** (BPE / SentencePiece) — essential for Indian scripts
3. **Larger beam search** (width 10–20) at inference time
4. **Checkpoint averaging** — average last 5–10 checkpoints for free gains
5. **Multiple references** — BLEU/ROUGE scores rise with 2–4 human references
6. **Use sacreBleu** for reproducible, comparable BLEU reporting

See the **💡 Improve Scores** tab inside the app for a full interactive guide.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- BLEU metric: [Papineni et al., 2002](https://aclanthology.org/P02-1040/)
- ROUGE metric: [Lin, 2004](https://aclanthology.org/W04-1013/)
- Indian language resources: [AI4Bharat](https://ai4bharat.org/), [IndicNLP](https://indicnlp.ai4bharat.org/)
