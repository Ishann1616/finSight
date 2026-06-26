def calculate_emi(principal: float, annual_rate: float, months: int) -> dict:
    r = (annual_rate / 100) / 12
    emi = principal * r * (1 + r)**months / ((1 + r)**months - 1)
    total_payment = emi * months
    total_interest = total_payment - principal
    return {
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2)
    }
