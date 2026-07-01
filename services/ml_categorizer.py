from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from services.categorizer import categorize, CATEGORIES
from database import SessionLocal
from models.transaction import Transaction

def build_training_data():
    merchants=[]
    labels=[]
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            merchants.append(keyword)
            labels.append(category)
    
    return merchants ,labels

def train_model():
    merchants , label = build_training_data()
    model= Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))),
        ('clf', MultinomialNB())
    ])
    model.fit(merchants,label)
    return model

ml_model = train_model()

def ml_categorize(merchant: str) -> str:
    keyword_result = categorize(merchant)
    if keyword_result != "Uncategorized":
        return keyword_result
    prediction = ml_model.predict([merchant.lower()])[0]
    return prediction

def backfill_categories(user_id: int):
    db= SessionLocal()
    transactions= db.query(Transaction).filter(
        Transaction.user_id== user_id,
        Transaction.category == "Uncategorized"
    ).all()

    for t in transactions:
        t.category = ml_categorize(t.merchant)

    db.commit()
    db.close()
