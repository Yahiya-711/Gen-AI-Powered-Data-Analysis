<<<<<<< HEAD
# Gen-AI-Powered-Data-Analysis
=======
# 📊 AI Data Analyst Agent (LangChain + Gemini)

This starter shows how to build a tool-using agent that answers natural-language data questions over a CSV, produces charts, and returns **strict JSON**.

## 1) Prereqs
- Python 3.10+
- A Google Generative AI API key with Gemini access.

## 2) Get the code
Unzip the archive, then:
```bash
cd ai-data-analyst-agent
python -m venv venv
# Windows: venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
```

## 3) Configure
Copy `.env.example` -> `.env` and set your key:
```
GOOGLE_API_KEY=your_google_generative_ai_api_key_here
```
(Optional) Change `DATA_PATH` to point at a different CSV.

## 4) Inspect the sample data
Open `data/sales.csv` to see columns: date, region, product, revenue, units.

## 5) Run the agent
```bash
python main.py
```

## 6) Try these prompts
- Total revenue this month
- Average units sold for Widget A
- Show revenue trend over time
- List rows where revenue > 2000 and region == 'South'

Charts are saved to `charts/` and logs to `logs/`.

## 7) Extend
- Replace CSV with your data (keep the column `date` parseable).
- Add a tool to export filtered rows to CSV.
- Swap the backend for Postgres/BigQuery via SQLAlchemy and a new tool.

## 8) Troubleshooting
- If the model outputs non-JSON text, re-run. The parser reports the raw output for debugging.
- Ensure your API key is valid and that your environment can access Gemini.
>>>>>>> 8766a5d (Structuring the LLM by google api key)
