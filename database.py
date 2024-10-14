# from langchain_community.vectorstores import FAISS
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader 
from uuid import uuid4



class VectorStore:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.loader = PyPDFLoader(self.pdf_path)
        self.pages = self.loader.load_and_split()  
        
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="abcd")
        
        self.embedding_model = HuggingFaceEmbeddings()


    def load_pdf(self):
        if not self.collection.count():
            for page in self.pages:
                embedding = self.embedding_model.embed_documents([page.page_content])[0]

                self.collection.add(documents=page.page_content,
                                    metadatas={"source": self.pdf_path},
                                    ids=[str(uuid4())],
                                    embeddings=[embedding])
        return self.pages

    def retriever(self,query_text):
        # retr = self.collection.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        query_embedding = self.embedding_model.embed_query(query_text)

        # Perform a similarity search using the embedding
        results = self.collection.query(
            query_embeddings=[query_embedding],  # Use query embedding for similarity search
            n_results=5  # Number of results to return
        )
        return results
