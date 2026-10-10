import pdfplumber
import re

LINE_RE = re.compile(
    r'(?P<date>\d{1,2}[A-Za-z]{3},\d{4})\s+'
    r'(?P<kind>Paid\s*to|Received\s*from)\s*'
    r'(?P<merchant>.+?)\s+'
    r'₹(?P<amount>[\d,]+(?:\.\d+)?)'
)

def parse_statement_pdf(pdf_path: str) -> list:
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split('\n'):
                m = LINE_RE.search(line)
                if not m:
                    continue
                transactions.append({
                    "date": m.group("date"),
                    "merchant": m.group("merchant").strip(),
                    "amount": float(m.group("amount").replace(",", "")),
                    "direction": "debit" if m.group("kind").lower().startswith("paid") else "credit",
                    "payment_method": "UPI",
                })
    return transactions