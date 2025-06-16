from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer



def pdf_text2Vec(pdf_path:str, 
                 model_transformer:SentenceTransformer = SentenceTransformer('all-MiniLM-L6-v2')):
    """
    Load a PDF file and convert to vector embeddings.
    """
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    ## Word embeddings
    model = model_transformer
    vector_embeddings = []
    
    # Iterate over the chunks and compute embeddings
    for i, chunk in enumerate(chunks):
        text = chunk.metadata["subject"]
        embedding = model.encode(text)

        vector_embeddings.append(embedding)


    return vector_embeddings



if __name__ == "__main__":
    print(len(pdf_text2Vec("../data/pdfs/mathematics-10-01555-v2.pdf")))