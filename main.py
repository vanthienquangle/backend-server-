from fastapi import FastAPI, Response, status, HTTPException, Depends 
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session 
from . import models
from . database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind= engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    


class Post(BaseModel):
    title: str
    content: str 
    published: bool = True 

while True:


    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite foods","content":"I like pizza","id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p 
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        

@app.get("/")                          #only represents the path of the link
def root():
    return {"message":"Welcome to my API"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/posts")                     #If both paths are set the same, the prior will be shown
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}
# title str, content str, category, bool published 

@app.get("/posts/lastest")
def get_lastest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int): # If there is no id for it, it will show "null" but if the data type is wrong, it will show ERROR
    cursor.execute("""SELECT * from posts where id = %s """, (id))
    test_post = cursor.fetchone()
    print(test_post)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts where id = %s returning *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content %s, published =%s""", (post.title, post.content, post.published))
    
    updated_post = cursor.fetchone()
    conn.commit() 
    if updated_post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id {id} does not exist")
    
    return {"data": updated_post}