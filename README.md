# My-Dinero Backend

This is the backend service for the My-Dinero application, built with FastAPI and SQLAlchemy.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (optional but recommended)

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd my-dinero
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the `backend` directory with the following variables:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///./test.db  # Default SQLite database
   PLAID_CLIENT_ID=your_plaid_client_id
   PLAID_SECRET=your_plaid_secret
   PLAID_ENV=sandbox  # sandbox, development, or production
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Backend Locally

1. Start the FastAPI server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. The server will start at `http://127.0.0.1:8000`

## Accessing the OpenAPI/Swagger Documentation

FastAPI automatically generates interactive API documentation:

1. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/docs
   ```
   This will open the Swagger UI where you can explore and test all available endpoints.

2. Alternatively, you can access the ReDoc documentation at:
   ```
   http://127.0.0.1:8000/redoc
   ```

## Testing

The project uses pytest for testing. To run the tests:

1. Make sure you're in the backend directory:
   ```bash
   cd backend
   ```

2. Run the tests:
   ```bash
   pytest
   ```

3. For more detailed test output:
   ```bash
   pytest -v
   ```

## API Endpoints

The backend provides the following main API routes:

- `/auth` - Authentication endpoints
- `/users` - User management
- `/accounts` - Bank account management
- `/transactions` - Transaction management
- `/plaid` - Plaid API integration

For detailed information about each endpoint, refer to the Swagger documentation at `http://127.0.0.1:8000/docs`.

## Project Structure

```
backend/
├── alembic.ini          # Alembic configuration
├── app/
│   ├── api/             # API routes
│   ├── core/            # Core functionality and config
│   ├── db/              # Database models and schemas
│   ├── migrations/      # Database migrations
│   ├── services/        # Business logic services
│   ├── tests/           # Test files
│   └── main.py          # Application entry point
└── requirements.txt     # Python dependencies
```