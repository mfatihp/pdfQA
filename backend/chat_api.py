import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from utils.librarian_llm import LibrarianLLM
from utils.librarian_db import LibrarianDB


app = FastAPI()


librarian_db = None
librarian_llm = None

def get_db_instance():
    """
    Returns LibrarianDB for speed up the initialization of DB class.

    Returns:
        librarian_db: LibrarianDB instance.
    """
    global librarian_db

    if librarian_db is None:
        librarian_db = LibrarianDB()
    
    return librarian_db


def get_llm_instance():
    """
    Returns LibrarianLLM for speed up the initialization of LLM class.

    Returns:
        librarian_llm: LibrarianLLM instance.
    """
    global librarian_llm
    
    if librarian_llm is None:
        librarian_llm = LibrarianLLM()
    
    return librarian_llm

# Enable Cross-Origin Resource Sharing (CORS) to allow requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/answer")
async def answer_question(user_message: Request, model= Depends(get_llm_instance)):
    """
    Creates llm response using RAG for user question.

    Args:
        user_message: User's question in JSON format.

    Returns:
        reply: Chat response to the user's message.
    """
    message = await user_message.json()
    response = model.respond(text_input=message["text"])
    reply = {"reply" : response}
    return reply



@app.post("/upload")
async def upload_pdf(pdf_file: UploadFile=File(...), model= Depends(get_db_instance)):
    """
    Uploads pdf files into local chroma DB

    Args:
        pdf_file: 
    """
    print("It started...")
    file_bytes = await pdf_file.read()
    model.add_documents_to_collection(pdf_file=file_bytes)
    print("Success...")





if __name__ == '__main__':
    uvicorn.run(app, port=8000)