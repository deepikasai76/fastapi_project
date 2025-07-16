from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from typing import List, Optional
from ..database import get_db

router = APIRouter( prefix="/posts", tags=["Posts"])
# APIRouter is a class that helps us create API endpoints


## ----- Get all posts -------
@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), 
              current_user: int= Depends(oauth2.get_current_user),
              limit: int =10, skip: int=0, search: Optional[str]=""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    return posts

# POST method is used to send data to the server, to create new resources.
# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']}"}

## --------- Create posts -------
@router.post("/", status_code=status.HTTP_201_CREATED,  response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content, published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # # cursor is the object that allows us to execute SQL commands
    # new_post =cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(
    #     title = post.title, content = post.content,
    #         published = post.published)
    
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id , **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# {id} is the path parameter, it is a variable that is passed to the function
@router.get("/{id}", response_model=schemas.Post)
def get_post(id:int, db: Session = Depends(get_db),
             current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(
        models.Post.id == id).first()

    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found "}
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int= Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """ , (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(
        models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} doesnot exits")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)   
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

## Update posts
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db: Session = Depends(get_db), 
                current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s,content=%s, published=%s where id = %s RETURNING * """, \
    #                (post.title,post.content, post.published, str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post= post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} doesnot exits")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
