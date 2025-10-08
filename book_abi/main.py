import json
import logging
import os 
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from data_validation import  BookBase, Book

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

DATA_FILE = Path("data/books-data.json")

books_db = []

def _load_data():
    """Loads book data from the JSON file into the in-memory database."""
    global books_db
    try:
        with open(DATA_FILE, 'r') as f:
            books_db = json.load(f)
        logger.info(f"Successfully loaded {len(books_db)} records from {DATA_FILE}")
    except FileNotFoundError:
        logger.warning(f"{DATA_FILE} not found. Initializing with empty database.")
        books_db = []
    # except NameError:
    #     logger.warning("file name not defined")
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {DATA_FILE}. Initializing with empty database.")
        books_db = []

def _save_data():
    """Saves the current state of the in-memory database back to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            # Use indent=2 for readability in the file
            json.dump(books_db, f, indent=2)
        logger.info(f"Successfully saved {len(books_db)} records to {DATA_FILE}")
    except Exception as e:
        logger.error(f"Failed to save data to {DATA_FILE}: {e}")

# Load initial data when the application starts
_load_data()
_save_data()

app = FastAPI(title="Book CRUD API", version="1.0")

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    """
    Checks the service health and verifies the existence of the data file.
    Always returns 200 OK if the service is running, with detailed status.
    """
    # Check if the data file exists on the file system
    file_exists = os.path.exists(DATA_FILE)
    
    status_detail = {
        "status": "OK",
        "service": "Book CRUD API",
        "data_file_status": "Available" if file_exists else "Missing (Check deployment volume)",
    }
    
    logger.info(f"Health check performed. Data file status: {status_detail['data_file_status']}")
    return status_detail


# @app.get("/books/", response_model=list[Book])
# def get_books():
#     """Retrieve all books."""
#     logger.info("Fetching all books.")
#     return books_db




# POST: CREATE operation
# @app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
# def create_book(book_data: BookBase):
#     """
#     Creates a new book record.
#     The input data is automatically validated against the BookBase model.
#     """
#     new_id = uuid.uuid4()
#     # Convert Pydantic model to a dict, then add the generated ID
#     new_book = book_data.model_dump()
#     new_book["id"] = str(new_id)

#     books_db.append(new_book)
#     _save_data()

#     logger.info(f"Book created with ID: {new_book['id']}")
#     # Return the created book using the full Book response model
#     return new_book