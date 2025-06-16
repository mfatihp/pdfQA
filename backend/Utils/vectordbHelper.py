import chromadb


def add_document2collection(embedding_list:list, chromadb_client:chromadb.Client, collection_name:str="my_collection"):
    """
    Add a list of embeddings to the specified ChromaDB collection.
    """
    collection = chromadb_client.get_or_create_collection(name=collection_name)
    
    # Add documents to the collection
    collection.add(
        documents=[str(i) for i in range(len(embedding_list))],  # Dummy document names
        embeddings=embedding_list)
    
    print(f"Added {len(embedding_list)} documents to collection '{collection_name}'.") #TODO: write to log file, not print






if __name__ == "__main__":
    from pdfHelper import pdf_text2Vec
    
    embedding_list = pdf_text2Vec("../data/pdfs/mathematics-10-01555-v2.pdf")
    chroma_client = chromadb.Client()

    add_document2collection(embedding_list=embedding_list, chromadb_client=chroma_client, collection_name="my_collection")