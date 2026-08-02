from fastapi import FastAPI, HTTPException
from datetime import datetime
import zoneinfo
from app.db import SessionDep, creaate_all_tables
from .models import Customer, CustomerCreate, Invoice, Transaction
from sqlmodel import select


app = FastAPI(title="learn_fastAPI", lifespan=creaate_all_tables)

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
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get("/customers/{id}", response_model=Customer)
async def customer(id: int, session: SessionDep):
    customer = session.exec(select(Customer).where(Customer.id == id)).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# transactions
@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

# invoices
@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data



