import torch
import chromadb
from transformers import pipeline
from sentence_transformers import SentenceTransformer

from Utils.vectordbHelper import create_embeddings



chroma_client = chromadb.PersistentClient(path="../data/chroma_persistent_db")
collection = chroma_client.get_or_create_collection(name="my_collection")

user_input = "Does surveillance systems regularly create massive video data?"

print("===============================================")

model = SentenceTransformer("all-MiniLM-L6-v2")
embedding = create_embeddings(user_input, model=model) #FIXME: create embeddings not working, returns empty list


result = collection.query(query_embeddings=embedding, n_results=1)
print(result["documents"][0])

print("===============================================")

model_id = "meta-llama/Llama-3.2-1B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a Q&A chatbot. Use the provided context to answer the user's question. \
                                   If the context does not provide enough or zero information, respond with variations of this quote 'I could not find relevant information.'"},   
    {"role": "user", "content": f"""Context: {result["documents"][0]}
                                    Question: Does surveillance systems regularly create massive video data?"""},
]

outputs = pipe(
    messages,
    max_new_tokens=256,
)

print(outputs[0]["generated_text"][-1])