import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import json
from app.core.config import (
    PLAID_CLIENT_ID,
    PLAID_SECRET,
    PLAID_ENV,
    PLAID_COUNTRY_CODES,
    PLAID_PRODUCTS
)

class PlaidService:
    def __init__(self):
        """Initialize the Plaid client with credentials from config."""
        # Configure the Plaid client
        configuration = plaid.Configuration(
            host=self._get_plaid_host(),
            api_key={
                'clientId': PLAID_CLIENT_ID,
                'secret': PLAID_SECRET,
            }
        )
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def _get_plaid_host(self) -> str:
        """Get the appropriate Plaid API host based on the environment."""
        if PLAID_ENV == 'sandbox':
            return plaid.Environment.Sandbox
        elif PLAID_ENV == 'development':
            return plaid.Environment.Development
        elif PLAID_ENV == 'production':
            return plaid.Environment.Production
        else:
            # Default to sandbox if environment is not recognized
            return plaid.Environment.Sandbox

    def create_link_token(self, user_id: str, client_name: str = "My Dinero") -> Dict[str, Any]:
        """
        Create a link token for a user to connect their bank accounts.

        Args:
            user_id: The ID of the user in your application
            client_name: The name of your application

        Returns:
            A dictionary containing the link token and expiration
        """
        try:
            # Convert string country codes to CountryCode enum values
            country_codes = [CountryCode(code) for code in PLAID_COUNTRY_CODES]

            # Convert string products to Products enum values
            products = [Products(product) for product in PLAID_PRODUCTS]

            # Create the link token request
            request = LinkTokenCreateRequest(
                user=LinkTokenCreateRequestUser(
                    client_user_id=user_id
                ),
                client_name=client_name,
                products=products,
                country_codes=country_codes,
                language='en'
            )

            # Create the link token
            response = self.client.link_token_create(request)
            return {
                'link_token': response['link_token'],
                'expiration': response['expiration']
            }
        except plaid.ApiException as e:
            error_response = json.loads(e.body)
            return {
                'error': {
                    'status_code': e.status,
                    'message': error_response.get('error_message', 'An unknown error occurred'),
                    'error_code': error_response.get('error_code', 'UNKNOWN_ERROR'),
                    'error_type': error_response.get('error_type', 'API_ERROR')
                }
            }

    def exchange_public_token(self, public_token: str) -> Dict[str, Any]:
        """
        Exchange a public token for an access token and item ID.

        Args:
            public_token: The public token received from the Plaid Link onSuccess callback

        Returns:
            A dictionary containing the access token and item ID
        """
        try:
            request = ItemPublicTokenExchangeRequest(
                public_token=public_token
            )
            response = self.client.item_public_token_exchange(request)
            return {
                'access_token': response['access_token'],
                'item_id': response['item_id']
            }
        except plaid.ApiException as e:
            error_response = json.loads(e.body)
            return {
                'error': {
                    'status_code': e.status,
                    'message': error_response.get('error_message', 'An unknown error occurred'),
                    'error_code': error_response.get('error_code', 'UNKNOWN_ERROR'),
                    'error_type': error_response.get('error_type', 'API_ERROR')
                }
            }

    def get_transactions(self, access_token: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get transactions for a user's financial accounts.

        Args:
            access_token: The access token for the user's financial institution
            start_date: The start date for transactions (defaults to 30 days ago)
            end_date: The end date for transactions (defaults to today)

        Returns:
            A dictionary containing transactions and account information
        """
        try:
            # Set default dates if not provided
            if start_date is None:
                start_date = datetime.now() - timedelta(days=30)
            if end_date is None:
                end_date = datetime.now()

            # Format dates as ISO strings (YYYY-MM-DD)
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            # Create the transactions request
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date_str,
                end_date=end_date_str
            )

            # Get transactions
            response = self.client.transactions_get(request)

            return {
                'accounts': response['accounts'],
                'transactions': response['transactions'],
                'total_transactions': response['total_transactions'],
                'item': response['item']
            }
        except plaid.ApiException as e:
            error_response = json.loads(e.body)
            return {
                'error': {
                    'status_code': e.status,
                    'message': error_response.get('error_message', 'An unknown error occurred'),
                    'error_code': error_response.get('error_code', 'UNKNOWN_ERROR'),
                    'error_type': error_response.get('error_type', 'API_ERROR')
                }
            }

    def get_account_balances(self, access_token: str) -> Dict[str, Any]:
        """
        Get balances for a user's financial accounts.

        Args:
            access_token: The access token for the user's financial institution

        Returns:
            A dictionary containing account information with balances
        """
        try:
            request = AccountsGetRequest(
                access_token=access_token
            )
            response = self.client.accounts_get(request)

            return {
                'accounts': response['accounts'],
                'item': response['item']
            }
        except plaid.ApiException as e:
            error_response = json.loads(e.body)
            return {
                'error': {
                    'status_code': e.status,
                    'message': error_response.get('error_message', 'An unknown error occurred'),
                    'error_code': error_response.get('error_code', 'UNKNOWN_ERROR'),
                    'error_type': error_response.get('error_type', 'API_ERROR')
                }
            }
