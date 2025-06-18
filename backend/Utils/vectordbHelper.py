import chromadb
from sentence_transformers import SentenceTransformer

  

def create_embeddings(text:str, model:SentenceTransformer):
    """
    Create embeddings for a given text using the specified SentenceTransformer model.
    """
    print("Embedding text...")
    embedding = model.encode(text, convert_to_tensor=True).cpu().numpy()

    print("Embedding created.")
    print(type(embedding))
    return embedding



def add_document2collection(embedding_list:list, chromadb_client:chromadb.Client, collection_name:str="my_collection"):
    """
    Add a list of embeddings to the specified ChromaDB collection.
    """
    print("Adding documents to collection...")

    collection = chromadb_client.get_or_create_collection(name=collection_name)
    
    # TODO: Loop will be here and give propoer info for each document
    # Add documents to the collection
    collection.upsert(
        ids = [f"chunk-{i}" for i in range(len(embedding_list))],
        documents=[str(embedding_list[i]) for i in range(len(embedding_list))],
        embeddings=embedding_list)
    
    print(f"Added {len(embedding_list)} documents to collection '{collection_name}'.") #TODO: write to log file, not print






if __name__ == "__main__":
    pass