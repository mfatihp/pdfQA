import chromadb
from sentence_transformers import SentenceTransformer
from Utils.pdfHelper import pdf2chunks
from Utils.vectordbHelper import add_document2collection, create_embeddings


chroma_client = chromadb.PersistentClient(path="../data/chroma_persistent_db")

path = "../data/pdfs/mathematics-10-01555-v2.pdf"
chunks = pdf2chunks(pdf_path=path)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings_list = [create_embeddings(chunk.metadata["subject"], model=model) for chunk in chunks]

add_document2collection(embedding_list=embeddings_list,
                        chromadb_client=chroma_client, 
                        collection_name="my_collection")