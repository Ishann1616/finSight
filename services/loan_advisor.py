from services.emi_calculator import calculate_emi
def loan_advisor(loan_type:str, amount:float, tenure_months:int)->dict:
    rates = {
    "home": 8.5,
    "car": 9.5,
    "personal": 12.0
    }
    rate= rates.get(loan_type.lower())
    if not rate :
        return{"error": "Invalid loan type. Choose home, car, or personal."}

    emi= calculate_emi(amount, rate, tenure_months)

    if rate < 8.5:
        verdict = "Great rate"
    elif rate <= 10:
        verdict = "Average rate"
    else:
        verdict = "High interest — consider alternatives"
    return{
        "loan_type":loan_type,
        "amount":amount,
        "tenure_monthss":tenure_months,
        "interest_rate":f"{rate}%",
        "monthly_emi": emi["monthly_emi"],
        "total_payment": emi["total_payment"],
        "total_interest": emi["total_interest"],
        "verdict": verdict,
        "note": "Rates as of 2024. Verify with your bank before applying."
    }