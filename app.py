import streamlit as st
import os
import time
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

# Set up environment variables
load_dotenv()

# API key validation with helpful error messages
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("""
    🔑 **GROQ_API_KEY not found!** 
    
    Please set up your API keys:
    1. Create a `.env` file in the project root
    2. Add: `GROQ_API_KEY=your_actual_api_key`
    3. Get your key from: https://console.groq.com/keys
    
    Or set the environment variable: `export GROQ_API_KEY=your_key`
    """)
    st.stop()

# Optional configurations with defaults
vector_store_path = os.getenv("VECTOR_STORE_PATH", "my_vector_store")
embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Streamlit UI setup
st.set_page_config(
    page_title="LexiMini - Legal Assistant", 
    page_icon="⚖️",
    layout="wide"
)

# Header with title
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    # Use emoji-based design for the header
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 4rem; margin-bottom: 10px;'>⚖️</div>
            <h1 style='margin: 0; color: #1f4e79; font-family: serif;'>LexiMini</h1>
            <p style='margin: 5px 0 0 0; color: #666; font-style: italic;'>AI-Powered Legal Assistant</p>
        </div>
    """, unsafe_allow_html=True)

# Add prominent disclaimer with better styling
st.markdown("""
    <div style='background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 15px; margin: 20px 0;'>
        <p style='margin: 0; color: #856404; font-weight: bold;'>
            ⚠️ <strong>IMPORTANT DISCLAIMER:</strong> This AI chatbot provides general information only and is not a substitute for professional legal advice. Always consult with a qualified attorney for specific legal matters.
        </p>
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Custom button styling */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #1f4e79, #2c5f8a);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        background: linear-gradient(45deg, #2c5f8a, #1f4e79);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    div.stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e6ed;
        padding: 12px 20px;
    }
    .stChatInput > div > div > input:focus {
        border-color: #1f4e79;
        box-shadow: 0 0 0 2px rgba(31, 78, 121, 0.2);
    }
    
    /* Status widget styling */
    div[data-testid="stStatusWidget"] div button {
        display: none;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    button[title="View fullscreen"] {visibility: hidden;}
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        margin: 10px 0;
    }
    
    /* Professional legal color scheme */
    :root {
        --legal-blue: #1f4e79;
        --legal-gold: #d4af37;
        --legal-gray: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# Reset conversation function
def reset_conversation():
    st.session_state.messages = []
    st.session_state.memory.clear()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)

# Initialize embeddings and vector store with multiple fallbacks
embeddings = None

# Try different embedding approaches in order of preference
try:
    # First try: Original model
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model,
        model_kwargs={'device': 'cpu'}
    )
except (NotImplementedError, Exception) as e:
    st.warning(f"⚠️ Primary embedding model failed: {embedding_model}")
    
    try:
        # Second try: Use HuggingFace API instead of local model
        from langchain_huggingface import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu', 'trust_remote_code': True}
        )
    except Exception as e2:
        try:
            # Third try: Use OpenAI embeddings if available
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                try:
                    from langchain_openai import OpenAIEmbeddings
                    embeddings = OpenAIEmbeddings(
                        openai_api_key=openai_key,
                        model="text-embedding-ada-002"
                    )
                    st.success("✅ Using OpenAI embeddings as fallback")
                except ImportError:
                    st.warning("OpenAI embeddings not available - install langchain-openai")
                    raise Exception("OpenAI import failed")
            else:
                raise Exception("No OpenAI key available")
        except Exception as e3:
            # Final fallback: Show error and use dummy embeddings for demo
            st.error(f"""
            🚨 **All embedding methods failed on this platform**
            
            **Solutions:**
            1. **Add OpenAI API key** to Streamlit secrets: `OPENAI_API_KEY`
            2. **Use a vector store** created locally and uploaded
            3. **Deploy on different platform** (local, Heroku, etc.)
            
            **Current Error**: Streamlit Cloud has PyTorch compatibility issues
            """)
            
            # Create a simple dummy embeddings class for demonstration
            class DummyEmbeddings:
                def embed_documents(self, texts):
                    return [[0.1] * 384 for _ in texts]
                def embed_query(self, text):
                    return [0.1] * 384
            
            embeddings = DummyEmbeddings()
            st.warning("⚠️ Using demo mode - functionality limited")

# Check if vector store exists
if not os.path.exists(vector_store_path):
    st.error(f"""
    📁 **Vector store not found at `{vector_store_path}`!**
    
    **For Streamlit Cloud deployment:**
    1. Run `python ingestion.py` locally 
    2. Commit the `my_vector_store/` folder to your repo
    3. Redeploy the app
    
    **Alternative**: Use OpenAI embeddings by adding `OPENAI_API_KEY` to secrets
    """)
    st.stop()

# Load vector store with error handling
try:
    db = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
    if isinstance(embeddings, type(embeddings)) and hasattr(embeddings, '__class__') and 'Dummy' in str(embeddings.__class__):
        st.warning("⚠️ Demo mode active - vector search may not work properly")
except Exception as e:
    st.error(f"""
    🚨 **Failed to load vector store**: {str(e)}
    
    **Solutions:**
    1. **Regenerate vector store** locally with `python ingestion.py`
    2. **Use matching embedding model** that created the vector store
    3. **Add OpenAI API key** for cloud compatibility
    """)
    st.stop()
db_retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Define the prompt template
prompt_template = """
<s>[INST]This is a chat template and As a legal chat bot , your primary objective is to provide accurate and concise information based on the user's questions. Do not generate your own questions and answers. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from posing additional questions. The aim is to deliver professional, precise, and contextually relevant information pertaining to the Indian Penal Code.
CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}
ANSWER:
</s>[INST]
"""
prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question', 'chat_history'])

# Initialize the LLM
try:
    llm = ChatGroq(groq_api_key=groq_api_key, model_name=groq_model)
except Exception as e:
    st.error(f"""
    🤖 **Error initializing Groq LLM:**
    
    {str(e)}
    
    Please check:
    - Your GROQ_API_KEY is valid
    - You have internet connection
    - The model `{groq_model}` is available
    """)
    st.stop()

# Set up the QA chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=st.session_state.memory,
    retriever=db_retriever,
    combine_docs_chain_kwargs={'prompt': prompt}
)

# Display previous messages
for message in st.session_state.messages:
    role = message.get("role")
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(message.get("content"))
    else:
        with st.chat_message("assistant", avatar="⚖️"):
            st.write(message.get("content"))

# Input prompt
input_prompt = st.chat_input("Say something")

if input_prompt:
    with st.chat_message("user", avatar="👤"):
        st.write(input_prompt)

    st.session_state.messages.append({"role": "user", "content": input_prompt})

    with st.chat_message("assistant", avatar="⚖️"):
        with st.status("Thinking 💡...", expanded=True):
            result = qa.invoke(input=input_prompt)
            message_placeholder = st.empty()
            
            # Add disclaimer to the response
            disclaimer = "\n\n---\n**⚠️ Disclaimer:** This response is generated by an AI chatbot for informational purposes only and should not be considered as legal advice. Please consult with a qualified legal professional for specific legal matters."
            
            full_response = result["answer"] + disclaimer

            # Simulate typing effect
            displayed_response = ""
            for chunk in full_response:
                displayed_response += chunk
                time.sleep(0.01)
                message_placeholder.markdown(displayed_response + " ▌")
            
            # Final response without cursor
            message_placeholder.markdown(full_response)

        st.button('Reset All Chat 🗑️', on_click=reset_conversation)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666; font-size: 0.9rem;'>
        <p style='margin: 0;'>⚖️ <strong>LexiMini</strong> - Powered by AI Technology</p>
        <p style='margin: 5px 0 0 0; font-size: 0.8rem;'>
            Built with Streamlit • LangChain • HuggingFace • Groq
        </p>
    </div>
""", unsafe_allow_html=True)