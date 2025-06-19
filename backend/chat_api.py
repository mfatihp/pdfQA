import torch
import chromadb
from fastapi import FastAPI
from transformers import pipeline
from sentence_transformers import SentenceTransformer


app = FastAPI()


@app.get("/")
def answer_question(user_message:str):
    return None


#TODO: transform into REST API

chroma_client = chromadb.PersistentClient(path="../data/chroma_persistent_db")
collection = chroma_client.get_or_create_collection(name="my_collection")

user_input = "What can you say about video anomaly detection?"

result = collection.query(query_texts=user_input, n_results=5)

model_id = "meta-llama/Llama-3.2-1B-Instruct"
pipe = pipeline(task="text-generation",
                model=model_id,
                torch_dtype=torch.bfloat16,
                device_map="auto")

messages = [
    {"role": "system", "content": "You are a Q&A chatbot. Answer the user's question using the provided context, \
                                   which comes from academic papers in PDF format. Do not mention the context itself. \
                                   Keep your answer under 256 tokens."},   
    {"role": "user", "content": f"""Context: {result["documents"]}
                                    Question: {user_input}"""},
]

outputs = pipe(messages, max_new_tokens=256)

print(outputs[0]["generated_text"][-1])