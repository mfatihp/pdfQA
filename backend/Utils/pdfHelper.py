from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



def pdf2chunks(pdf_path:str):
    """
    Load a PDF file and convert to vector embeddings.
    """
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    return chunks



if __name__ == "__main__":
    print(pdf2chunks("../data/pdfs/mathematics-10-01555-v2.pdf"))