from random import randrange
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from  psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas, utils, config
from .routers import posts, users, auth, vote



models.Base.metadata.create_all(bind=engine)

app = FastAPI() # Create an instance of the FastAPI class



'''Pydantic is a Python library that provides 
runtime validation and parsing of data based on
a predefined schema. 
It's particularly useful when working with APIs, 
data processing, and data validation.
key needs that Pydantic addresses:
Data Validation, Runtime Type Checking, Data Parsing, 
Serialization, Error Handling, Code Generation.
Pydantic is often used to define a schema for the data that 
will be sent to an API. By creating a Pydantic model, you can define the
structure and constraints of the data that will be accepted by the API
'''



# Creating a Pydantic model

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

## Root endpoint     
# this @app is the decorator that tells FastAPI to use this function as a route
# async is the keyword to define an asynchronous function
# asynchronous function is a function that can be paused and resumed at any point


@app.get("/") # This is the root URL of the application
async def root(): # This is the "function" that will be called when the root URL is accessed
    return {"message": "Welcome to my API"}

# # ------ sqlalchemy ------
# @app.get("/sqlalchemy")
# def text_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts



