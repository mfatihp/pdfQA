from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


loader = PyMuPDFLoader("../data/pdfs/mathematics-10-01555-v2.pdf")
docs = loader.load()


splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

## Word embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

text = chunks[1].metadata["subject"]
embedding = model.encode(text)

## Insert into chromaDB

