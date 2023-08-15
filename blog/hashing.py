from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password):
        return pwd_context.hash(password)
    
    def verify(hashedpass , plainpass):
        return pwd_context.verify(plainpass , hashedpass)