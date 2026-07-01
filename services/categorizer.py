CATEGORIES = {
    "Food": [
        "zomato", "swiggy", "bakery", "restaurant", "cafe", "food",
        "kitchen", "dhaba", "hotel", "pizza", "burger", "biryani"
    ],
    "Health": [
        "apollo", "pharmacy", "medical", "hospital", "clinic",
        "doctor", "medicine", "health", "chemist"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "ajio", "store", "shop",
        "market", "mall", "retail"
    ],
    "Fitness": [
        "gym", "fitness", "protein", "protinworld", "supplement"
    ],
    "Transport": [
        "uber", "ola", "rapido", "auto", "bus", "metro", "petrol"
    ],
    "Entertainment": [
        "netflix", "spotify", "youtube", "prime", "hotstar", "cinema"
    ],
    "Education": [
        "udemy", "coursera", "books", "stationery", "college", "school"
    ],
    "Investment": [
        "moneywise", "groww", "zerodha", "kuvera", "coin", "mutual fund",
        "mf", "sip", "stock", "demat", "angel", "upstox"
    ],
    "Pass-Through": [
        "transfer to", "neft", "imps", "rtgs", "sent to", "received from",
        "family", "father", "mother", "papa", "mom"
    ]
}

def categorize(merchant: str) -> str:
    merchant_lower= merchant.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in merchant_lower:
                return category
    return "Uncategorized"