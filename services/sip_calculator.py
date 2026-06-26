def calculate_sip(amount: float, months: int ,risk: str)-> dict:
    rates={
        "conservative": 0.08,
        "moderate":0.12,
        "aggressive":0.15
    }
    allocations={
        "conservative": {"Large Cap":"80%", "Debt/Bonds": "20%"},
        "moderate":{"Large Cap":"60%", "Mid Cap": "30%", "Small Cap": "10%"},
        "aggressive":{"Large Cap":"40%", "Mid Cap": "40%", "Small Cap": "20%"}
    }

    r = rates.get(risk.lower())
    if not r:
        return {"error":"Invalid risk. Choose conservativemoderate, or aggressive."}
    
    monthly_rate = r/12
    corpus = amount*(((1+monthly_rate)**months-1)/monthly_rate)*(1+monthly_rate)

    return{
        "monthly_sip":amount,
        "duration_months":months,
        "risk_profile":risk,
        "allocation": allocations[risk.lower()],
        "expected_annual_return": f"{int(r*100)}%",
        "properted_corpus": round(corpus,2)
    }