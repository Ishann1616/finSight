import pdfplumber
import re

def parse_statement_pdf(pdf_path: str) -> list:
    transactions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            
            i = 0
            while i < len(lines):
                line = lines[i]
                
                date_match = re.search(r'(\d{1,2}\w+,\d{4})', line)
                amount_match = re.search(r'₹([\d,]+)', line)
                
                if date_match and amount_match:
                    date = date_match.group(1)
                    amount = float(amount_match.group(1).replace(',', ''))
                    
                    merchant = "Unknown"
                    if 'Paid to' in line:
                        merchant = line.split('Paidto')[-1].split('₹')[0].strip()
                    elif 'Received from' in line:
                        merchant = line.split('Receivedfrom')[-1].split('₹')[0].strip()
                    
                    transactions.append({
                        "date": date,
                        "merchant": merchant,
                        "amount": amount,
                        "payment_method": "UPI"
                    })
                i += 1
    
    return transactions