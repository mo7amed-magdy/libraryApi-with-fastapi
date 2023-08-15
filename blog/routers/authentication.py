from fastapi import FastAPI , Depends , status ,Response,HTTPException,APIRouter
from .. import schemas,database,models
from ..hashing import Hash
from sqlalchemy.orm import session
from ..JWTtoken import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm





router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db : session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid")
    
    if not Hash.verify(user.password , request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"wrong password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
