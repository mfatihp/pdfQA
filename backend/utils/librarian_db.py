import chromadb
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



class LibrarianDB:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="../data/chroma_persistent_db")
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
    

    def prepare_files(self, pdf_file:str): # TODO: pdf file will be received from API
        loader = PyMuPDFLoader(pdf_file)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        documents = [chunk.metadata["subject"] for chunk in chunks]
        ids = [str(i) for i in range(len(documents))]
        return ids, documents


    def add_documents_to_collection(self, pdf_file):
        ids, documents = self.prepare_files(self, pdf_file=pdf_file)
        self.collection.upsert(ids=ids, documents=documents)