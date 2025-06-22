import chromadb
import pymupdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document



class LibrarianDB:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="../data/chroma_persistent_db")
        self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
    

    def __prepare_files(self, file_bytes: bytes):
        pdf = pymupdf.open(stream=file_bytes, filetype="pdf")

        docs = []
        for i, page in enumerate(pdf.pages()):
            text = page.get_text()
            metadata = {"page": i + 1}
            docs.append(Document(page_content=text, metadata=metadata))

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)

        documents = [chunk.page_content for chunk in chunks]
        ids = [str(i) for i in range(len(documents))]
        return ids, documents


    def add_documents_to_collection(self, pdf_file: bytes):
        ids, documents = self.__prepare_files(file_bytes=pdf_file)
        self.collection.upsert(ids=ids, documents=documents)