from database import SessionLocal
from models.banks import Bank

def seed_banks_loan_details():
    db = SessionLocal()
    bank_rate = [
        # Home Loans
        Bank(bank_name="SBI", loan_type="home", interest_rate=7.50, processing_fee=0.35, max_tenure_months=360),
        Bank(bank_name="HDFC", loan_type="home", interest_rate=7.90, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="ICICI", loan_type="home", interest_rate=8.75, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="Axis", loan_type="home", interest_rate=8.35, processing_fee=1.0, max_tenure_months=360),
        Bank(bank_name="Kotak", loan_type="home", interest_rate=7.99, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="PNB", loan_type="home", interest_rate=7.45, processing_fee=0.35, max_tenure_months=360),
        Bank(bank_name="Bank of Baroda", loan_type="home", interest_rate=7.45, processing_fee=0.25, max_tenure_months=360),
        Bank(bank_name="Union Bank", loan_type="home", interest_rate=7.50, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="Canara Bank", loan_type="home", interest_rate=7.40, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="Indian Bank", loan_type="home", interest_rate=7.40, processing_fee=0.23, max_tenure_months=360),
        Bank(bank_name="IDBI", loan_type="home", interest_rate=8.40, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="Federal Bank", loan_type="home", interest_rate=8.80, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="Yes Bank", loan_type="home", interest_rate=9.15, processing_fee=1.0, max_tenure_months=360),
        Bank(bank_name="AU Small Finance", loan_type="home", interest_rate=9.50, processing_fee=1.0, max_tenure_months=360),
        Bank(bank_name="IndusInd", loan_type="home", interest_rate=8.75, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="UCO Bank", loan_type="home", interest_rate=7.50, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="Bandhan Bank", loan_type="home", interest_rate=9.15, processing_fee=1.0, max_tenure_months=360),
        Bank(bank_name="Central Bank", loan_type="home", interest_rate=7.50, processing_fee=0.25, max_tenure_months=360),
        Bank(bank_name="Indian Overseas Bank", loan_type="home", interest_rate=7.55, processing_fee=0.50, max_tenure_months=360),
        Bank(bank_name="Bank of India", loan_type="home", interest_rate=7.50, processing_fee=0.25, max_tenure_months=360),
        # Car Loans
        Bank(bank_name="SBI", loan_type="car", interest_rate=8.50, processing_fee=0.51, max_tenure_months=84),
        Bank(bank_name="HDFC", loan_type="car", interest_rate=9.00, processing_fee=0.65, max_tenure_months=84),
        Bank(bank_name="ICICI", loan_type="car", interest_rate=9.10, processing_fee=1.0, max_tenure_months=84),
        Bank(bank_name="Axis", loan_type="car", interest_rate=9.25, processing_fee=1.0, max_tenure_months=84),
        Bank(bank_name="Kotak", loan_type="car", interest_rate=9.99, processing_fee=0.50, max_tenure_months=84),
        Bank(bank_name="PNB", loan_type="car", interest_rate=8.75, processing_fee=0.25, max_tenure_months=84),
        Bank(bank_name="Bank of Baroda", loan_type="car", interest_rate=8.75, processing_fee=0.25, max_tenure_months=84),
        Bank(bank_name="Union Bank", loan_type="car", interest_rate=8.70, processing_fee=0.50, max_tenure_months=84),
        Bank(bank_name="Canara Bank", loan_type="car", interest_rate=8.70, processing_fee=0.25, max_tenure_months=84),
        Bank(bank_name="Indian Bank", loan_type="car", interest_rate=8.50, processing_fee=0.23, max_tenure_months=84),
        Bank(bank_name="IDBI", loan_type="car", interest_rate=8.90, processing_fee=0.50, max_tenure_months=84),
        Bank(bank_name="Federal Bank", loan_type="car", interest_rate=9.50, processing_fee=0.50, max_tenure_months=84),
        Bank(bank_name="Yes Bank", loan_type="car", interest_rate=9.75, processing_fee=1.0, max_tenure_months=84),
        Bank(bank_name="AU Small Finance", loan_type="car", interest_rate=10.50, processing_fee=1.5, max_tenure_months=84),
        Bank(bank_name="IndusInd", loan_type="car", interest_rate=9.50, processing_fee=1.0, max_tenure_months=84),
        Bank(bank_name="UCO Bank", loan_type="car", interest_rate=8.70, processing_fee=0.50, max_tenure_months=84),
        Bank(bank_name="Bandhan Bank", loan_type="car", interest_rate=10.99, processing_fee=1.0, max_tenure_months=84),
        Bank(bank_name="Central Bank", loan_type="car", interest_rate=8.65, processing_fee=0.25, max_tenure_months=84),
        Bank(bank_name="Indian Overseas Bank", loan_type="car", interest_rate=8.75, processing_fee=0.50, max_tenure_months=84),
        Bank(bank_name="Bank of India", loan_type="car", interest_rate=8.60, processing_fee=0.25, max_tenure_months=84),
        # Personal Loans
        Bank(bank_name="SBI", loan_type="personal", interest_rate=11.0, processing_fee=1.0, max_tenure_months=60),
        Bank(bank_name="HDFC", loan_type="personal", interest_rate=10.75, processing_fee=2.5, max_tenure_months=60),
        Bank(bank_name="ICICI", loan_type="personal", interest_rate=10.85, processing_fee=2.25, max_tenure_months=60),
        Bank(bank_name="Axis", loan_type="personal", interest_rate=11.25, processing_fee=2.0, max_tenure_months=60),
        Bank(bank_name="Kotak", loan_type="personal", interest_rate=10.99, processing_fee=2.5, max_tenure_months=60),
        Bank(bank_name="PNB", loan_type="personal", interest_rate=11.40, processing_fee=1.0, max_tenure_months=60),
        Bank(bank_name="Bank of Baroda", loan_type="personal", interest_rate=11.15, processing_fee=1.0, max_tenure_months=60),
        Bank(bank_name="Union Bank", loan_type="personal", interest_rate=11.20, processing_fee=0.50, max_tenure_months=60),
        Bank(bank_name="Canara Bank", loan_type="personal", interest_rate=11.90, processing_fee=0.50, max_tenure_months=60),
        Bank(bank_name="Indian Bank", loan_type="personal", interest_rate=10.90, processing_fee=1.0, max_tenure_months=60),
        Bank(bank_name="IDBI", loan_type="personal", interest_rate=11.0, processing_fee=1.0, max_tenure_months=60),
        Bank(bank_name="Federal Bank", loan_type="personal", interest_rate=11.49, processing_fee=1.0, max_tenure_months=60),
        Bank(bank_name="Yes Bank", loan_type="personal", interest_rate=11.50, processing_fee=2.0, max_tenure_months=60),
        Bank(bank_name="AU Small Finance", loan_type="personal", interest_rate=12.50, processing_fee=2.0, max_tenure_months=60),
        Bank(bank_name="IndusInd", loan_type="personal", interest_rate=10.49, processing_fee=2.5, max_tenure_months=60),
        Bank(bank_name="UCO Bank", loan_type="personal", interest_rate=11.45, processing_fee=1.0, max_tenure_months=60),
        Bank(bank_name="Bandhan Bank", loan_type="personal", interest_rate=13.50, processing_fee=2.0, max_tenure_months=60),
        Bank(bank_name="Central Bank", loan_type="personal", interest_rate=11.50, processing_fee=0.50, max_tenure_months=60),
        Bank(bank_name="Indian Overseas Bank", loan_type="personal", interest_rate=11.35, processing_fee=0.50, max_tenure_months=60),
        Bank(bank_name="Bank of India", loan_type="personal", interest_rate=11.25, processing_fee=0.50, max_tenure_months=60),
    ]
    db.add_all(bank_rate)
    db.commit()
    db.close()
    print("Bank Loan Rates seeded successfully")

if __name__ == "__main__":
    seed_banks_loan_details()
