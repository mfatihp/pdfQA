from fastapi import FastAPI
from Utils.librarian_llm import LibrarianLLM


app = FastAPI()
librarian = LibrarianLLM()


@app.get("/")
def answer_question(user_message:str):
    response = librarian.respond(text_input=user_message)
    return response