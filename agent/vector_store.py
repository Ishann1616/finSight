from functools import lru_cache
from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
from database import SessionLocal
from models.transaction import Transaction

CHROMA_PATH = "./chroma_db"

class FastEmbeddings(Embeddings):
    def __init__(self):
        self.model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return [v.tolist() for v in self.model.embed(texts)]

    def embed_query(self, text):
        return next(iter(self.model.embed([text]))).tolist()

@lru_cache(maxsize=1)
def get_embeddings():
    return FastEmbeddings()   # loaded once, reused

def load_transactions_to_chroma(user_id: int):
    db= SessionLocal()
    try:
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).all()

        if not transactions:
            return "No transactions found"
        
        texts =[
            f"{t.date} | {t.merchant} | ₹{t.amount} | {t.category}"
            for t in transactions
        ]

        ids = [str(t.id) for t in transactions]

        try:
            Chroma(collection_name=f"user_{user_id}_transactions",
                embedding_function=get_embeddings(),
                persist_directory=CHROMA_PATH).delete_collection()
        except Exception:
            pass
        vectorstore = Chroma(
            collection_name=f"user_{user_id}_transactions",
            embedding_function=get_embeddings(),
            persist_directory=CHROMA_PATH
        )

        vectorstore.add_texts(texts=texts, ids=ids)
        return f"Loaded {len(texts)} transactions into ChromaDB"

    finally: 
        db.close()

def search_transactions(query: str,user_id: int, k: int=5):
    vectorstore = Chroma(
            collection_name=f"user_{user_id}_transactions",
            embedding_function=get_embeddings(),
            persist_directory=CHROMA_PATH
    )
    results = vectorstore.similarity_search(query,k=k)
    return"\n".join([doc.page_content for doc in results])

