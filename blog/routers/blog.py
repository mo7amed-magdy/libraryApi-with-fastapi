from fastapi import FastAPI , Depends , status ,Response,HTTPException,APIRouter
from .. import schemas,models,database
from sqlalchemy.orm import session
from ..oauth2 import get_current_user
get_db=database.get_db

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)

@router.get("/" , response_model=list[schemas.ShowBlog])
def get_all(db : session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
     blogs = db.query(models.Blog).all()
     return blogs
 
 
 
@router.post("/" , status_code=status.HTTP_201_CREATED )

def create(request : schemas.Blog , db : session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    new_blog = models.Blog(title = request.title , body = request.body,user_id =1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put("/{id}" , status_code=status.HTTP_202_ACCEPTED)

def update(id,request : schemas.Blog , db : session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    blog =db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")

    blog.update({'title' : request.title , 'body' : request.body}, synchronize_session=False)
    db.commit()
    return 'updated'
    

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)

def destroy(id , db : session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    blog =db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@router.get("/{id}",response_model=schemas.ShowBlog)
def get_blog(id,db : session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
     
     if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")

     return blog
 
