from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Dict, Any, Optional
from datetime import datetime

from api.dependencies import get_db
from services.plaid_service import PlaidService

router = APIRouter()
plaid_service = PlaidService()

@router.post("/create_link_token")
def create_link_token(
    user_id: UUID = Query(..., description="ID of the user for whom to create a link token"),
    client_name: str = "My Dinero"
):
    """
    Create a link token for a user to connect their bank accounts via Plaid Link.
    """
    result = plaid_service.create_link_token(str(user_id), client_name)
    
    if "error" in result:
        raise HTTPException(
            status_code=result["error"]["status_code"],
            detail=result["error"]["message"]
        )
    
    return result

@router.post("/exchange_public_token")
def exchange_public_token(
    public_token: str,
    db: Session = Depends(get_db)
):
    """
    Exchange a public token received from Plaid Link for an access token.
    """
    result = plaid_service.exchange_public_token(public_token)
    
    if "error" in result:
        raise HTTPException(
            status_code=result["error"]["status_code"],
            detail=result["error"]["message"]
        )
    
    # TODO: Store the access token associated with the user who initiated the Plaid Link flow in database
    
    return result

@router.get("/transactions")
def get_transactions(
    access_token: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get transactions for a user's financial accounts.
    """
    result = plaid_service.get_transactions(access_token, start_date, end_date)
    
    if "error" in result:
        raise HTTPException(
            status_code=result["error"]["status_code"],
            detail=result["error"]["message"]
        )
    
    return result

@router.get("/account_balances")
def get_account_balances(
    access_token: str
):
    """
    Get balances for a user's financial accounts.
    """
    result = plaid_service.get_account_balances(access_token)
    
    if "error" in result:
        raise HTTPException(
            status_code=result["error"]["status_code"],
            detail=result["error"]["message"]
        )
    
    return result