# Gemini Context & Project Documentation

## Project Overview

**Project Name:** Preekvoorbereiding (Sermon Preparation)
**Purpose:** An AI-powered CLI tool designed to assist Protestant (PKN) ministers in sermon preparation. It generates comprehensive context analyses (social, cultural, political) and liturgical building blocks (exegesis, prayers, sermon sketches).
**Core Methodology:** Based on the homiletic framework of De Leede & Stark (context analysis) and Eugene Lowry (narrative preaching), utilizing the "Naardense Bijbel" translation.
**Technologies:** Python, Google Gemini API (v1.0+ SDK with Search Grounding), BeautifulSoup4.

## Environment & Setup

### Requirements
*   **Python:** 3.8+ recommended.
*   **Dependencies:**
    *   `google-genai` (Google GenAI SDK v1.0+)
    *   `requests`
    *   `beautifulsoup4`
    *   `tiktoken` (optional, for token counting)

### Installation
```bash
pip install -r requirements.txt
pip install requests beautifulsoup4
```

### Configuration
The project requires a valid Gemini API key set as an environment variable:
```bash
export GEMINI_API_KEY='your-api-key-here'
```

## Project Structure

### Core Scripts
*   **`contextduiding.py`**: The primary entry point. Orchestrates the "Basic Analysis" (Phase 1 & 2).
    *   Prompts user for: Place, Church Municipality, Date.
    *   Generates markdown files `00` through `06` (Context, News, Politics, etc.).
*   **`verdieping.py`**: The "Deep Dive" script (Phase 3).
    *   Reads existing output from `contextduiding.py`.
    *   Generates markdown files `07` through `13` (Exegesis, Art, Prayers, Sermon Plot).
*   **`naardense_bijbel.py`**: A utility module to scrape Bible texts from `naardensebijbel.nl`. Handles caching and URL construction. Saves texts exclusively as JSON (`.json`, NBV21-compatible structure).
*   **`nbv21_bijbel.py`**: A utility module to fetch NBV21 Bible texts from local JSON files (output of `get_chapter.R`). Handles book name mapping and reference parsing.
*   **`count_tokens.py`**: Utility to analyze token usage of generated outputs.

### Directories
*   **`prompts/`**: Contains the specific prompts sent to the LLM. Each file corresponds to a specific analysis step (e.g., `07_exegese.md`).
    *   *Note:* Prompts use Mustache-style placeholders (e.g., `{{plaatsnaam}}`) filled by the Python scripts.
*   **`output/`**: Stores the generated content. Each session creates a timestamped subdirectory (e.g., `output/Utrecht_25_december_2025_.../`).
*   **`docs/`**: A lightweight static web viewer to browse the `output/` content.
    *   `generate_data.py`: Converts `output/` Markdown files into a JSON data blob (`data.js`) for the viewer.
*   **`misc/`**: Background reading and theoretical frameworks (De Leede & Stark, Lowry).
*   **`nbv21/`**: JSON files containing Bible texts (likely NBV21 translation), possibly used as an alternative or supplementary source.

## Workflow

1.  **Basic Analysis:**
    Run `python contextduiding.py`. Input the local details. This creates the foundational context files (00-06).

2.  **Deep Dive (Optional but recommended):**
    Run `python verdieping.py`. Select the previously generated session. This adds theological and liturgical depth (07-13), including exegesis and prayer suggestions.

3.  **Visualization:**
    Run `python docs/generate_data.py` to update the local web viewer data, then open `docs/index.html` (or serve `docs/` via a local server).

## Technical Constraints & Notes

*   **Model:** Currently configured to use `gemini-2.0-flash-exp` (or similar preview models as defined in scripts).
*   **Grounding:** Heavily relies on Google Search grounding to provide up-to-date local news and statistics.
*   **Safety:** The prompts and scripts are designed to minimize hallucinations, but output should always be verified, especially for local statistics and specific church details.
*   **File Formats:** All textual output is strictly Markdown.

## Key Commands

| Task | Command |
| :--- | :--- |
| **Run Basic Analysis** | `python contextduiding.py` |
| **Run Deep Dive** | `python verdieping.py` |
| **Update Web Viewer** | `python docs/generate_data.py` |
| **Count Tokens** | `python count_tokens.py` |
