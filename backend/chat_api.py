import uvicorn
from fastapi import FastAPI, Request, UploadFile, File
from utils.librarian_llm import LibrarianLLM
from utils.librarian_db import LibrarianDB


app = FastAPI()

librarian_db = LibrarianDB()
librarian_llm = LibrarianLLM()



@app.post("/answer")
async def answer_question(user_message: Request):
    """
    Creates llm response using RAG for user 
    """
    message = await user_message.json()
    response = librarian_llm.respond(text_input=message["text"])
    return response



@app.post("/upload")
async def upload_pdf(pdf_file: UploadFile=File(...)): #TODO: add proper file upload and test it 
    """
    Uploads pdf files into local chromadb
    """
    print("It started...")
    file_bytes = await pdf_file.read()
    librarian_db.add_documents_to_collection(pdf_file=file_bytes)
    print("Success...")





if __name__ == '__main__':
    uvicorn.run(app, port=8000)