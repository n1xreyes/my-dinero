from fastapi import FastAPI
from api.routes import users, accounts, transactions

app = FastAPI()

# Include API routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])