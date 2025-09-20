from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

app = FastAPI()

# Global variable initialization
runningproject = "default"

def startmodal(username: str):
    global runningproject
    runningproject = username
    print(runningproject)

    # Load environment variables
    load_dotenv()

    # Delete existing Chroma DB folder
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")

    # Load and split documents
    loader = PyPDFDirectoryLoader(f'data/{username}')
    documents = loader.load()

    # Optimized text splitting using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", ".", "!", "?"],  # Natural boundaries: paragraphs and sentences
        chunk_size=1000,  # Larger chunk size to retain more context
        chunk_overlap=150  # Small overlap to maintain coherence across chunks
    )
    chunks = text_splitter.split_documents(documents)

    # Create Chroma index and retriever
    index = Chroma.from_documents(chunks, OllamaEmbeddings(model="qwen2:0.5b", show_progress=True), persist_directory="./chroma_db")
    retriever = index.as_retriever()

    # Optimized prompt template with clearer instructions and examples for the model
    template = """
    You are a helpful assistant with access to the following document context. 
    Answer the question **based ONLY on this context**. If the context doesn't have the information, say "I don't know".
    
    Document Context: 
    {context}
    
    Question: {question}
    
    Please provide a clear and concise answer in a few sentences.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    model = Ollama(model="qwen2:0.5b")

    global rag_chain
    rag_chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question")
        }
        | prompt
        | model
        | StrOutputParser()
    )

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

UPLOAD_DIR = "/Users/praka/Korosuke/ModelServer/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Uploadda(BaseModel):
    name: str

class Usermodel:
    def __init__(self, username: str):
        self.username = username

@app.get('/')
async def root():
    return {"message": "API is up and running"}

@app.get("/files/")
async def list_files(username: str = Query(...)):
    try:
        userobj = Usermodel(username=username)
        user_upload_dir = os.path.join('data', userobj.username)
        if not os.path.exists(user_upload_dir):
            return {"error": "Directory not found"}
        files = [file for file in os.listdir(user_upload_dir) if file.endswith('.pdf')]
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
async def ask_question(data: Uploadda):
    try:
        response = rag_chain.invoke({"question": data.name})
        return {"message": response}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload/")
async def upload_file(username: str = Form(...), file: UploadFile = File(...)):
    try:
        userobj = Usermodel(username=username)
        global runningproject
        runningproject = "fileschanged"
        user_upload_dir = os.path.join('data', userobj.username)
        file_location = os.path.join(user_upload_dir, file.filename)
        os.makedirs(user_upload_dir, exist_ok=True)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/start_model/")
async def start_model_endpoint(username: str = Form(...)):
    try:
        userobj = Usermodel(username=username)
        startmodal(userobj.username)
        return {"message": "Model preparation started successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.delete("/delete/{filename}")
async def delete_file(filename: str, username: str = Query(...)):
    try:
        userobj = Usermodel(username=username)
        global runningproject
        runningproject = "fileschanged"
        user_upload_dir = os.path.join('data', userobj.username)
        file_path = os.path.join(user_upload_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            return {"message": f"File '{filename}' deleted successfully"}
        else:
            return {"error": "File not found"}
    except Exception as e:
        return {"error": str(e)}

@app.get('/currentmodel/')
async def getmodelname():
    try:
        return {"modelname": runningproject}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
