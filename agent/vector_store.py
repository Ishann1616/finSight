from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from database import SessionLocal
from models.transaction import Transaction

CHROMA_PATH ="./chroma_db"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

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

