# LexiMini Legal Chatbot ⚖️

AI-powered legal assistant using RAG (Retrieval-Augmented Generation) to answer questions from legal documents. Built with Streamlit, LangChain, and Groq LLM.

## 🚀 Live Demo

**Try it now**: [https://leximini-legal-chatbot.streamlit.app/](https://leximini-legal-chatbot.streamlit.app/)

## 🎥 Demo Video

Watch LexiMini in action:

![Demo Video](https://github.com/user-attachments/assets/85481859-9231-4636-9582-83810ac6634d)

**What the demo shows:**
- ✅ Legal question answering in real-time
- ✅ Source attribution from legal documents  
- ✅ Natural conversation flow
- ✅ Professional UI with custom avatars

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
   # Create .env file and add your API key
   echo "GROQ_API_KEY=your_actual_api_key_here" > .env
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



## Project Structure

```
├── app.py              # Streamlit chatbot interface
├── ingestion.py        # PDF processing & vector store creation
├── requirements.txt    # Python dependencies
└── data/              # Put your PDF files here
```

## License

MIT License - feel free to use for your projects!











