import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from utils.librarian_llm import LibrarianLLM
from utils.librarian_db import LibrarianDB


app = FastAPI()


librarian_db = None
librarian_llm = None

def get_db_instance():
    global librarian_db

    if librarian_db is None:
        librarian_db = LibrarianDB()
        print("Librarian_db initialized")
    
    return librarian_db


def get_llm_instance():
    global librarian_llm
    
    if librarian_llm is None:
        librarian_llm = LibrarianLLM()
        print("Librarian_llm initialized")
    
    return librarian_llm


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
    Creates llm response using RAG for user 
    """
    message = await user_message.json()
    response = model.respond(text_input=message["text"])
    reply = {"reply" : response}
    return reply



@app.post("/upload")
async def upload_pdf(pdf_file: UploadFile=File(...), model= Depends(get_db_instance)): #TODO: add proper file upload and test it 
    """
    Uploads pdf files into local chromadb
    """
    print("It started...")
    file_bytes = await pdf_file.read()
    model.add_documents_to_collection(pdf_file=file_bytes)
    print("Success...")





if __name__ == '__main__':
    uvicorn.run(app, port=8000)