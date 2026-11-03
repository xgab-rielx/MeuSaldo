from models import SpendingCreate, SpendingGet
from fastapi import FastAPI, HTTPException
from database import init_db, create_spending, get_spendings, get_spending_by_id
from decimal import Decimal
from datetime import datetime

    
app = FastAPI()

init_db()


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.post("/spendings", response_model=SpendingGet, status_code=201)
def create_spending_route(spending: SpendingCreate):
    spending_id = create_spending(
        spending.description,
        spending.category,
        str(spending.value),
        spending.date.isoformat(),
    )

    return SpendingGet(
        spending_id=spending_id,
        description=spending.description,
        category=spending.category,
        value=str(spending.value),
        date=spending.date.isoformat(),
    )


@app.get("/spendings", response_model=list[SpendingGet])
def get_spendings_route():
    rows = get_spendings()

    spendings = [
        {
            "spending_id": row["spending_id"],
            "description": row["description"],
            "category": row["category"],
            "value": (Decimal(row["value"])),
            "date": datetime.fromisoformat(row["date"]),
        } for row in rows
    ]

    return spendings

@app.get("/spendings/{spending_id}", response_model=SpendingGet)
def get_spending_by_id_route(spending_id: int):
    row =  get_spending_by_id(spending_id)
    if row:
        return {
            "spending_id": row["spending_id"],
            "description": row["description"],
            "category": row["category"],
            "value": (Decimal(row["value"])),
            "date": datetime.fromisoformat(row["date"])  
        }

    else:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")