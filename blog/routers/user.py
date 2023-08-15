from fastapi import FastAPI , Depends , status ,Response,HTTPException,APIRouter
from .. import schemas,models,database,hashing
from sqlalchemy.orm import session

get_db=database.get_db

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.ShowUser)

def create(request : schemas.User , db : session = Depends(get_db)):
    hashedpassword = hashing.Hash.bcrypt(request.password)
    new_user = models.User(name = request.name , email = request.email,password = hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schemas.ShowUser)
def get_user(id,db : session = Depends(get_db)):
     user = db.query(models.User).filter(models.User.id == id).first()
     
     if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")

     return user