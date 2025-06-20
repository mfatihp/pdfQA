import chromadb
import torch
import transformers


class LibrarianLLM:
    def __init__(self):
        self.model_name = "meta-llama/Llama-3.2-1B-Instruct"

        self.pipeline = transformers.pipeline(task="text-generation",
                                              model=self.model_name,
                                              torch_dtype=torch.bfloat16,
                                              device_map="auto")
        
        self.chroma_client = chromadb.PersistentClient(path="../data/chroma_persistent_db")
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")

        self.query_result = None
    

    def __query(self, text_input:str):
        self.query_result = self.collection.query(query_texts=text_input, n_results=5)


    def respond(self, text_input:str):
        self.__query(text_input=text_input)

        message = [
                    {"role": "system", "content": "You are a Q&A chatbot. Answer the user's question using the provided context, \
                                                which comes from academic papers in PDF format. Do not mention the context itself. \
                                                Keep your answer under 256 tokens."},   
                    {"role": "user", "content": f"""Context: {self.query_result["documents"]}
                                                    Question: {text_input}"""},
                ]
        
        output = self.pipeline(message, max_new_tokens=256)

        return output[0]["generated_text"][-1]["content"]