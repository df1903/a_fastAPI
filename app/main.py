from fastapi import FastAPI, HTTPException
from datetime import datetime
import zoneinfo
from .models import Customer, CustomerCreate, Invoice, Transaction


app = FastAPI(title="learn_fastAPI")

COUNTRIES_TIMEZONES = {
    "US": "America/New_York",
    "MX": "America/Mexico_City",
    "ES": "Europe/Madrid",
    "FR": "Europe/Paris",
    "DE": "Europe/Berlin",
    "IT": "Europe/Rome",
    "JP": "Asia/Tokyo",
    "CN": "Asia/Shanghai",
    "IN": "Asia/Kolkata",
    "BR": "America/Sao_Paulo",
    "CO": "America/Bogota",
}

db_customers: list[Customer] = []




# default

@app.get("/")
async def root():
    return {"status": "ok", "message": "RUNNING FASTAPI"}

@app.get("/hola")
async def hello():
    return {"status": "ok", "message": "Hello, World!"}

@app.get("/hora/{iso_code}")
async def hora(iso_code: str):
    iso_code = iso_code.upper()
    timezone = COUNTRIES_TIMEZONES.get(iso_code)
    
    if timezone is None:
        return {"status": "error", "message": "Country not found"}
    
    current_time = datetime.now(zoneinfo.ZoneInfo(timezone)).strftime('%Y-%m-%d %H:%M:%S')
    return {
        "status": "ok",
        "message": f"The current time in {timezone} is: {current_time}"
    }

# customers
@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers

@app.get("/customers/{id}", response_model=Customer)
async def customer(id: int):
    for cust in db_customers:
        if cust.id == id:
            return cust
    raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())
    # DB
    customer.id = len(db_customers) + 1
    db_customers.append(customer)
    return customer

# transactions
@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

# invoices
@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data



