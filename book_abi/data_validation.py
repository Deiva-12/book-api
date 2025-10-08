from pydantic import BaseModel,Field
import uuid


class Author(BaseModel):
    # name:str 
    # country: str 
    name: str = Field(min_length=3, description="The full name of the author.")
    country: str = Field(min_length=2, max_length=50, description="The author's country of origin.")

class BookBase(BaseModel):
    title : str = Field(min_length=1, description="The title of the book")
    year : int = Field(gt=1980, lt=2025, description="The publication year of the book.")
    author : Author
class Book(BaseModel):
    id : uuid.UUID = Field(default_factory=uuid.uuid4,description="The unique identifier for the book.")


    

 
# try:

#     new_book = Book(
#         id=uuid.uuid4(),
#         title="Clean Architecture",
#         year=2017,
#         author={
#             "name": "Robert C. Martin", 
#             "country": "USA"}
#     )
#     print(new_book)
# except Exception as e:
#     print("Validation Error:", e)
