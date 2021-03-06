#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic.networks import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Puerto Montt"
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Los Lagos"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Chile"
    )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Giocrisrai"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Godoy"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=30
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example=HairColor.black
        )
    is_married: Optional[bool] = Field(
        default=None
        )
    email:str = EmailStr(
        ...
        )
    
    #class Config:
    #    schema_extra = {
    #        "example": {
    #            "first_name": "Giocrisrai",
    #            "last_name": "Godoy Bonillo",
    #            "age": 30,
    #            "hair_color": "black",
    #            "is_married": False,
    #            "email": "contact@giocrisrai.com"
    #        }
    #    }

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validations: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_Length=1,
        max_Length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Daniela"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example="29"
        )
):
    return {name: age}

# Validations : Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path (
        ...,
        gt=0,
        title="Person Id",
        description="This is the person Id. It's required and greater than 0",
        example=20
        )
):
    return {person_id: "It exists!"}

# Validations: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the personID",
        gt=0,
        example=5
    ),
    person: Person = Body(...),
    #Location: Location = Body(...)
):
    #results = person.dict()
    #results.update(Location.dict())
    #return results
    return person