# Glade.ai-AI Contract Review Assistant

**Fast, structured contract review for attorneys and legal professionals.**

Glade.ai is an AI-powered contract review tool built for law firms and legal teams. It extracts key terms, surfaces risks, and generates a decision-ready summary in seconds. The interface is designed to support attorneys during initial contract triage, reducing manual review time without replacing attorney judgment.

---

## What It Does

Glade.ai analyzes any contract and returns a structured six-section review:

| Section | Description |
|---|---|
| **Contract Summary** | Plain-English overview of what the contract is about |
| **Key Parties** | Identified parties and their roles |
| **Important Terms** | Duration, payment, responsibilities, termination, and IP provisions |
| **Risks & Red Flags** | Flagged clauses rated HIGH, MEDIUM, or LOW risk |
| **Missing or Unclear Info** | Gaps, ambiguities, and incomplete terms |
| **Lawyer Review Checklist** | Actionable items to verify before signing or sending |

---

## Requirements

- Python 3.10 or higher
- A **Groq API key** is required for the AI review to work

### Getting Your Groq API Key

Glade.ai uses the [Groq API](https://console.groq.com) to run large language models at high speed. You must obtain a Groq API key before running the application.

1. Go to [console.groq.com](https://console.groq.com)
2. Create a free account, no credit card required
3. Navigate to **API Keys** and generate a new key
4. Copy the key; it starts with `gsk_`

You will enter this key in the app's **Settings** sidebar each time you run it. The key is never stored or transmitted outside your local session.

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### 3. Enter your Groq API key

Open the **Settings** panel in the sidebar, paste your `gsk_...` key into the API Key field, and select a model. The app will not function without a valid key.

---

## Usage

1. Open the app and enter your **Groq API key** in the Settings sidebar
2. Select a model **LLaMA 3.3 70B** is recommended for the most thorough analysis
3. Paste your contract text directly or upload a `.txt` file
4. Click **Generate Legal Review**
5. Review the structured output across all six sections
6. Optionally download the full report as a `.md` file for your records

---

## Model Options

| Model | Best For |
|---|---|
| `llama-3.3-70b-versatile` | Most thorough analysis recommended |
| `llama-3.1-8b-instant` | Fastest response, lighter contracts |
| `mixtral-8x7b-32768` | Long contracts, good reasoning |
| `gemma2-9b-it` | Alternative option |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| AI / LLM | Groq API (LLaMA 3.3 70B, Mixtral 8x7B, Gemma2 9B) |
| Styling | Custom CSS DM Serif Display / DM Sans / DM Mono |

---

## Disclaimer

Glade.ai is a decision support tool. It does not provide legal advice. All output should be reviewed by a qualified attorney before any legal decisions are made. No contract data is stored or retained by the application.

---

This demo is meant to show how AI can help law firms review contracts faster, with a clean and practical interface designed for real-world legal workflows.
