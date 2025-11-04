# LexiMini Legal Chatbot ⚖️

AI-powered legal assistant using RAG (Retrieval-Augmented Generation) to answer questions from legal documents. Built with Streamlit, LangChain, and Groq LLM.

## Quick Start

1. **Get API Key**: Sign up at [Groq Console](https://console.groq.com/keys) and get your API key

2. **Clone & Setup**:
   ```bash
   git clone https://github.com/munikumar229/LexiMini-Legal-Chatbot.git
   cd LexiMini-Legal-Chatbot
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Add Documents & Run**:
   ```bash
   # Put your PDF files in the data/ folder
   python ingestion.py  # Process documents
   streamlit run app.py # Start the chatbot
   ```

## Features

- 💬 Interactive legal Q&A interface
- 📚 RAG pipeline with FAISS vector search  
- 🔍 Source attribution for answers
- 🚀 Easy deployment to Streamlit Cloud

## Deployment

### Streamlit Cloud (Recommended)
1. Fork this repo
2. Connect to [Streamlit Cloud](https://share.streamlit.io)
3. Set secrets in app settings:
   ```toml
   GROQ_API_KEY = "your_groq_api_key"
   ```

### GitHub Secrets (for CI/CD)
Set repository secrets for automated deployment:
- `GROQ_API_KEY`: Your Groq API key

See [GitHub Secrets Setup Guide](GITHUB_SECRETS_SETUP.md) for detailed instructions.

## Project Structure

```
├── app.py              # Streamlit chatbot interface
├── ingestion.py        # PDF processing & vector store creation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── data/              # Put your PDF files here
```

## Troubleshooting

- **No API key**: Copy `.env.example` to `.env` and add your Groq API key
- **No documents**: Add PDF files to `data/` folder and run `python ingestion.py`
- **Import errors**: Try `pip install faiss-cpu` if FAISS installation fails

## License

MIT License - feel free to use for your projects!

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Notes: If you need FAISS and the wheel in `requirements.txt` doesn't work, install `faiss-cpu` explicitly:

```bash
pip install faiss-cpu
```

3. Provide environment variables

Create a `.env` file in the project root (example below). The project looks for API keys for embedding/LLM providers; if you use local models or open alternatives you may not need all keys.

Example `.env`:

```text
# Google Generative Embeddings (optional)
GOOGLE_API_KEY=your_google_api_key

# LLM provider (e.g. GROQ, OpenAI, or local model endpoints)
GROQ_API_KEY=your_groq_api_key

# Optional: path to store vector index (default: my_vector_store/index.faiss)
VECTOR_STORE_PATH=my_vector_store/index.faiss
```

4. Ingest documents (build embeddings / FAISS index)

Place your PDFs or text files in a folder (e.g. `data/`) and run:

```bash
python ingestion.py
```

This will create/overwrite the FAISS index at the configured `VECTOR_STORE_PATH`.

5. Run the app

```bash
streamlit run app.py
```

Open the Streamlit URL printed in the terminal (usually http://localhost:8501).

## Ingestion & vector store

- `ingestion.py` handles loading files, text splitting, embedding, and saving to FAISS. If your corpus is large, ingestion may take time — monitor memory and disk usage.
- `my_vector_store/index.faiss` (if present) is the on-disk example vector store; you can replace it by re-running ingestion.

## Configuration and env vars

- GROQ_API_KEY — for ChatGroq / Groq-based LLM usage (if used)

If you use different providers (OpenAI, local LLMs, or alternatives) adapt `app.py` and `ingestion.py` to the provider SDKs you choose.











