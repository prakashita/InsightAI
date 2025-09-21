Deep Researcher Agent

An AI-powered local research assistant that can search, analyze, and synthesize information from large-scale local data sources — without relying on external web search APIs.
This project uses FastAPI for the backend (document processing, embeddings, and retrieval) and React for the frontend (chat interface).

🔑 Features

    📂 Upload and manage local PDF documents
    
    🧠 Local embedding generation using OllamaEmbeddings (no external APIs)
    
    🔍 Efficient document indexing and retrieval with ChromaDB
    
    🪜 Multi-step reasoning with a RAG (Retrieval-Augmented Generation) pipeline
    
    💬 Interactive chat interface for asking research questions
    
    📝 Summarization and structured responses
    
    🔄 Support for model restarts and follow-up queries

🛠️ Tech Stack

  Backend (FastAPI)
  
    FastAPI + Uvicorn
    
    LangChain (document loaders, retrievers, RAG pipeline)
    
    Ollama for local LLM embeddings & reasoning
    
    ChromaDB for vector storage
  
  Frontend (React)
  
    React + Vite
    
    Axios (API calls)
    
    ReactMarkdown (for rich text display)

⚙️ Setup Instructions

  1️⃣ Clone the repository
  
    git clone https://github.com/your-username/deep-researcher-agent.git
    cd insightai
  
  2️⃣ Backend Setup (FastAPI)
  
    cd ModelServer
    pip install -r requirements.txt
    uvicorn main:app --reload
  
  
  3️⃣ Frontend Setup (React + Vite)
  
    cd client
    npm install
    npm run dev


🌟 Future Enhancements

    📑 Export research reports (PDF/Markdown)
    
    🔄 Interactive query refinement (follow-up clarifications)
    
    🧩 Explainable reasoning steps
