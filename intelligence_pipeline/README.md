# LangGraph Company Intelligence Pipeline

Production-grade pipeline integrating a multi-agent architecture to generate, validate, and store company intelligence.

## Features
- **Multi-LLM Parallel Execution:** Uses OpenAI, Gemini, and Groq simultaneously to prevent single-model hallucinations.
- **Deterministic Validation:** Leverages the existing `pytests/rules` suite as an absolute gatekeeper. No LLMs are used for validation.
- **Intelligent Consolidation:** Uses frequency counts to resolve conflicts and merge JSON schemas.
- **Regeneration Loop:** Extracts specific failure feedback and reroutes failed LLMs back for targeted data corrections.
- **Supabase Persistence:** Saves only perfectly validated records into the database.

## Setup
1. Create a `.env` file in the `langgraph/` directory with the following keys:
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `GROQ_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Execution
Run the CLI tool with the company name:
```bash
python main.py "SpaceX" --debug
```
