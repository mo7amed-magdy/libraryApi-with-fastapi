from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get("/")

def index():
    return {'Data' : {'Name' : 'Mohamed'}}


@app.get("/about")

def about():
    return {'Data' : 'about page'}

@app.get("/blog/{id}")

def show(id: int):
    return {'Data' : id}


@app.get("/blog/{id}/comments")

def show(id: int):
    return {'Data' : {id : 'comment'}}



class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    

@app.post("/blog")

def createblog(request : Blog):
    return {'Data' : f"blog is created with title {request.title}"}

