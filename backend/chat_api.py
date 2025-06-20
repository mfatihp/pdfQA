from fastapi import FastAPI, UploadFile
from utils.librarian_llm import LibrarianLLM
from utils.librarian_db import LibrarianDB


app = FastAPI()

librarian_llm = LibrarianLLM()
librarian_db = LibrarianDB()



@app.post("/answer")
async def answer_question(user_message): #TODO: decide input type 
    """
    Creates llm response using RAG for user 
    """
    response = librarian_llm.respond(text_input=user_message)
    return response



@app.post("/upload")
async def upload_pdf(pdf_file): #TODO: add proper file upload and test it 
    """
    Uploads pdf files into local chromadb
    """
    librarian_db.add_documents_to_collection(pdf_file=pdf_file)