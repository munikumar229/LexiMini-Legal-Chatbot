# GitHub Secrets Setup Guide for LexiMini

This guide shows how to configure GitHub secrets for secure API key management in your LexiMini Legal Chatbot repository.

## Required GitHub Secrets

### 1. GROQ_API_KEY (Required)
- **Purpose**: Powers the LLM for generating responses
- **How to get**: 
  1. Visit [Groq Console](https://console.groq.com/keys)
  2. Sign up/login to your Groq account
  3. Create a new API key
  4. Copy the key

### 2. GOOGLE_API_KEY (Optional)
- **Purpose**: For future Google AI integrations (currently not used)
- **How to get**:
  1. Visit [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
  2. Create a new project or select existing one
  3. Enable the Generative AI API
  4. Create credentials (API key)
  5. Copy the key

## Setting Up GitHub Secrets

### Method 1: Via GitHub Web Interface

1. **Navigate to your repository** on GitHub
2. **Go to Settings** (repository settings, not account settings)
3. **Click on "Secrets and variables"** in the left sidebar
4. **Select "Actions"**
5. **Click "New repository secret"**
6. **For each secret**:
   - Name: `GROQ_API_KEY`
   - Value: Your actual Groq API key
   - Click "Add secret"
   - Repeat for `GOOGLE_API_KEY` if needed

### Method 2: Via GitHub CLI (if you have it installed)

```bash
# Set Groq API key
gh secret set GROQ_API_KEY --body "your_actual_groq_api_key_here"

# Set Google API key (optional)
gh secret set GOOGLE_API_KEY --body "your_actual_google_api_key_here"
```

## Deployment Options

### Option 1: Streamlit Cloud Deployment

1. **Connect to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select this repository
   - Choose `app.py` as your main file

2. **Add secrets in Streamlit Cloud**:
   - In the app settings, go to "Secrets"
   - Add your environment variables:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   GOOGLE_API_KEY = "your_actual_google_api_key"
   ```

### Option 2: Manual Deployment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/munikumar229/LexiMini-Legal-Chatbot.git
   cd LexiMini-Legal-Chatbot
   ```

2. **Set up environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

4. **Process documents and run**:
   ```bash
   python ingestion.py
   streamlit run app.py
   ```

## Security Best Practices

1. **Never commit API keys** to your repository
2. **Use different keys** for development/production if possible
3. **Rotate keys regularly**
4. **Monitor API usage** in your provider dashboards
5. **Use environment variables** everywhere, never hard-code keys

## Verification

After setting up secrets, the GitHub Actions workflow will:

1. ✅ **Test imports** and basic functionality
2. 🔍 **Run security scans** on your code
3. 🚀 **Validate deployment readiness**
4. 📦 **Create releases** automatically

## Troubleshooting

### Common Issues:

1. **"GROQ_API_KEY not found" error**:
   - Verify secret name is exactly `GROQ_API_KEY`
   - Check that the secret value doesn't have extra spaces
   - Ensure the workflow has access to secrets

2. **API key invalid errors**:
   - Verify your API key is active in the provider console
   - Check for API usage limits
   - Ensure the key has the right permissions

3. **Workflow not using secrets**:
   - Check that secrets are set at repository level (not organization)
   - Verify the workflow file is in `.github/workflows/`
   - Ensure the workflow has the correct permissions

### Getting Help:

- Check the [Actions tab](../../actions) for detailed error logs
- Review the [Issues page](../../issues) for known problems
- Create a new issue if you encounter problems

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | - | Groq LLM API key |
| `GOOGLE_API_KEY` | ❌ No | - | Google AI API key (future use) |
| `VECTOR_STORE_PATH` | ❌ No | `my_vector_store` | Path to FAISS index |
| `DATA_DIRECTORY` | ❌ No | `./data` | Directory containing PDFs |
| `EMBEDDING_MODEL` | ❌ No | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model name |
| `GROQ_MODEL` | ❌ No | `llama-3.1-8b-instant` | Groq model to use |