def calculate_tax(annual_income: float)-> dict:
    tax=0
    slab=[
        (300000, 0),
        (700000, 0.05),
        (1000000, 0.10),
        (1200000, 0.15),
        (1500000, 0.20),
        (float('inf'), 0.30)
    ]
    prev=0
    for limit, rate in slab:
        if annual_income<=prev:
            break
        taxable=min(annual_income,limit)-prev
        tax += taxable * rate
        prev=limit
    
    effective_rate= round((tax / annual_income)*100,2) if annual_income >0 else 0
    return{
      "taxable_income":annual_income,
      "tax_amount":round(tax,2),
      "effective_rate":effective_rate,
      "regime":"new regime"
    }
