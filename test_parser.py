from services.pdf_parser import parse_statement_pdf
from services.categorizer import categorize

transactions = parse_statement_pdf("/Users/ishandewangan/Downloads/GPay_statement.pdf")

for t in transactions[:10]:
    category = categorize(t["merchant"])
    print(f"{t['merchant']:<30} ₹{t['amount']:<10} {category}")