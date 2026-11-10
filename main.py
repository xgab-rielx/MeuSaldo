from models import SpendingCreate, SpendingGet, SpendingUpdate, LoginRequest
from security import verify_password
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
import os
from starlette.middleware.sessions import SessionMiddleware

from database import (
    init_db,
    create_spending,
    get_spendings,
    get_spending_by_id,
    update_spending,
    delete_spending,
    get_month_spendings,
    get_user_by_username
)

from decimal import Decimal
from datetime import datetime, date

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET"]
)

app.mount("/app", StaticFiles(directory="static", html=True), name="static")

init_db()


@app.post("/login")
def login(login_request: LoginRequest, request: Request):
    user = get_user_by_username(
        login_request.username
    )

    if user is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")

    senha_valida = verify_password(login_request.password, user["password_hash"])

    if senha_valida is False:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")

    request.session["user_id"] = user["user_id"]

    return{
        "message": "Login feito com sucesso."
    }


@app.post("/logout")
def logout(request: Request):
    request.session.clear()

    return {
        "message": "Logout feito com sucesso."
    }


@app.post("/spendings", response_model=SpendingGet, status_code=201)
def create_spending_route(spending: SpendingCreate, request: Request):

    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Necessário Login.")

    spending_id = create_spending(
        user_id,
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
def get_spendings_route(
    request: Request,
    start_date: date | None = None,
    end_date: date | None = None,
    category: str | None = None,
):

    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Necessário Login.")
    
    rows = get_spendings(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        category=category
    )

    spendings = [
        {
            "spending_id": row["spending_id"],
            "description": row["description"],
            "category": row["category"],
            "value": (Decimal(row["value"])),
            "date": datetime.fromisoformat(row["date"]),
        }
        for row in rows
    ]

    return spendings


@app.get("/spendings/monthly_total")
def month_spendings_route(year: int, month: int, request: Request):

    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Necessário Login.") 

    if month < 1 or month > 12:
        raise HTTPException(status_code=422, detail="Mês inválido")
    
    rows = get_month_spendings(year, month, user_id)

    amounts = Decimal("0.00")

    for row in rows:
        amounts += Decimal(row["value"])

    return {
        "year": year,
        "month": month,
        "total": amounts
    }


@app.get("/spendings/{spending_id}", response_model=SpendingGet)
def get_spending_by_id_route(spending_id: int, request: Request):

    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Necessário Login.")

    row = get_spending_by_id(spending_id, user_id)
    if row:
        return {
            "spending_id": row["spending_id"],
            "description": row["description"],
            "category": row["category"],
            "value": (Decimal(row["value"])),
            "date": datetime.fromisoformat(row["date"]),
        }

    else:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")


@app.put("/spendings/{spending_id}", response_model=SpendingGet)
def update_spending_route(
    spending_id: int,
    spending_update: SpendingUpdate,
    request: Request
):

    user_id = request.session.get("user_id")
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Necessário Login.")

    spending = get_spending_by_id(spending_id, user_id)

    if spending is None:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")

    update_spending(
        spending_id=spending_id,
        user_id=user_id,
        description=spending_update.description,
        category=spending_update.category,
        value=str(spending_update.value),
        date=spending["date"],
    )

    return {
        "spending_id": spending_id,
        "description": spending_update.description,
        "category": spending_update.category,
        "value": spending_update.value,
        "date": datetime.fromisoformat(spending["date"]),
    }


@app.delete("/spendings/{spending_id}", status_code=204)
def delete_spending_route(spending_id: int, request: Request):

    user_id = request.session.get("user_id")
        
    if user_id is None:
        raise HTTPException(status_code=401, detail="Necessário Login.")
    
    rows_effected = delete_spending(spending_id, user_id)

    if rows_effected == 0:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")  


@app.get("/session")
def valid_session(request: Request):
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Sessão inativa.")

    return {
        "message": "Há uma sessão válida."
    }
        