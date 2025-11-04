import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Set up environment variables
load_dotenv()

# Configuration with defaults
data_directory = os.getenv("DATA_DIRECTORY", "./data")
vector_store_path = os.getenv("VECTOR_STORE_PATH", "my_vector_store")
embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

def embed_and_save_documents():
    # Check if data directory exists
    if not os.path.exists(data_directory):
        print(f"❌ Error: Data directory '{data_directory}' not found!")
        print(f"Please create the directory and add your PDF files.")
        print(f"Or set DATA_DIRECTORY environment variable to a different path.")
        return False
    
    # Check if directory has PDF files
    pdf_files = [f for f in os.listdir(data_directory) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"❌ Error: No PDF files found in '{data_directory}'!")
        print(f"Please add PDF files to process.")
        return False
    
    print(f"📁 Found {len(pdf_files)} PDF files in '{data_directory}'")
    
    # Use HuggingFace embeddings (free, local, no API needed)
    embeddings = HuggingFaceEmbeddings(
        model_name=embedding_model,
        model_kwargs={'device': 'cpu'}  # Use CPU to avoid GPU dependencies
    )
    print(f"🤖 Using embedding model: {embedding_model}")
    
    loader = PyPDFDirectoryLoader(data_directory)
    print("Loader initialised")
    docs = loader.load()
    print("Loading the docs")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)
    print("Splitting the docs")
    
    # Ensure metadata includes the source file name
    for doc in final_documents:
        if 'source' in doc.metadata:
            source_file = doc.metadata['source']
            doc.metadata['source'] = os.path.basename(source_file)
        else:
            # If source metadata is not present, add it
            doc.metadata['source'] = os.path.basename(loader.directory)
    
    # Ensure the payload size is within limits by batching the documents
    batch_size = 100  # Adjust batch size as needed
    batched_documents = [final_documents[i:i + batch_size] for i in range(0, len(final_documents), batch_size)]
    vector_stores = []
    for batch in batched_documents:
        vector_store = FAISS.from_documents(batch, embeddings)
        vector_stores.append(vector_store)
    print("created batched documents")
    
    # Merge the vector stores
    vectors = vector_stores[0]
    for vector_store in vector_stores[1:]:
        vectors.merge_from(vector_store)
    print("merged the vectors")
    
    # Save the vector store to disk
    vectors.save_local(vector_store_path)
    print(f"✅ Vector store saved to: {vector_store_path}")
    print(f"📊 Total documents processed: {len(final_documents)}")
    return True

if __name__ == "__main__":
    print("🚀 Starting document ingestion...")
    success = embed_and_save_documents()
    if success:
        print("🎉 Ingestion completed successfully!")
    else:
        print("❌ Ingestion failed!")
        exit(1)
