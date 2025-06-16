import chromadb
from sentence_transformers import SentenceTransformer


def create_embeddings(text:str, model_name:str="all-MiniLM-L6-v2"):
    """
    Create embeddings for a given text using the specified SentenceTransformer model.
    """
    model = SentenceTransformer(model_name)
    embedding = model.encode(text, convert_to_tensor=True)

    return embedding



def add_document2collection(embedding_list:list, chromadb_client:chromadb.Client, collection_name:str="my_collection"):
    """
    Add a list of embeddings to the specified ChromaDB collection.
    """
    collection = chromadb_client.get_or_create_collection(name=collection_name, embedding_function=SentenceTransformer("all-MiniLM-L6-v2"))
    
    # TODO: Loop will be here and give propoer info for each document
    # Add documents to the collection
    collection.upsert(
        documents=[str(i) for i in range(len(embedding_list[0].metadata["subject"]))],
        embeddings=embedding_list)
    
    print(f"Added {len(embedding_list)} documents to collection '{collection_name}'.") #TODO: write to log file, not print






if __name__ == "__main__":
    pass