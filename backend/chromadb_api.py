import chromadb
from sentence_transformers import SentenceTransformer
from backend.Utils.pdf_helper import pdf2chunks
from backend.Utils.vectordb_helper import add_document2collection


#TODO: transform into REST API

chroma_client = chromadb.PersistentClient(path="../data/chroma_persistent_db")

path = "../data/pdfs/mathematics-10-01555-v2.pdf"
chunks = pdf2chunks(pdf_path=path)

documents = [chunk.metadata["subject"] for chunk in chunks]
ids = [str(i) for i in range(len(documents))]

collection = chroma_client.get_or_create_collection(name="my_collection")
collection.upsert(ids=ids, documents=documents)

# add_document2collection(embedding_list=embeddings_list,
#                         chromadb_client=chroma_client, 
#                         collection_name="my_collection")
