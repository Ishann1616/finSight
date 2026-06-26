from database import SessionLocal
from models.fund import Fund

def seed_funds():
    db= SessionLocal()
    funds = [
        Fund(fund_name="Axis Bluechip", category="Large Cap", risk_profile="conservative", expected_return=8.0),
        Fund(fund_name="Mirae Asset Large Cap", category="Large Cap", risk_profile="conservative", expected_return=9.0),
        Fund(fund_name="Parag Parikh Flexi Cap", category="Mid Cap", risk_profile="moderate", expected_return=12.0),
        Fund(fund_name="Axis Midcap", category="Mid Cap", risk_profile="moderate", expected_return=13.0),
        Fund(fund_name="Nippon Small Cap", category="Small Cap", risk_profile="aggressive", expected_return=15.0),
        Fund(fund_name="Quant Small Cap", category="Small Cap", risk_profile="aggressive", expected_return=16.0),
    ]
    db.add_all(funds)
    db.commit()
    db.close()
    print("Funds seeded successfully")

if __name__== "__main__":
    seed_funds()