from fastapi import FastAPI
from api.routes import auth, users, accounts, transactions, plaid

app = FastAPI()

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(plaid.router, prefix="/plaid", tags=["Plaid"])
