from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Customer(BaseModel):
    name: str
    mobile: str
    city: str
    minutes: int
    texts: int

@app.post("/generate_bill")
def generate_bill(data: Customer):

    # Base Plan
    base_charge = 15.00
    base_minutes = 50
    base_texts = 50

    # Extra charges
    extra_min_charge = 0
    extra_text_charge = 0

    if data.minutes > base_minutes:
        extra_min_charge = (data.minutes - base_minutes) * 0.25

    if data.texts > base_texts:
        extra_text_charge = (data.texts - base_texts) * 0.15

    # Fixed charges
    fee_911 = 0.44

    subtotal = base_charge + extra_min_charge + extra_text_charge + fee_911
    tax = subtotal * 0.05
    total = subtotal + tax

    return {
        "Customer Name": data.name,
        "Mobile Number": data.mobile,
        "City": data.city,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Base Charge": round(base_charge, 2),
        "Extra Minutes Charge": round(extra_min_charge, 2),
        "Extra Text Charge": round(extra_text_charge, 2),
        "Call Center Price": round(fee_911, 2),
        "Tax": round(tax, 2),
        "Total Bill": round(total, 2)
    }