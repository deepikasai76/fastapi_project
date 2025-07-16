## handles the login functionality — i.e., verifying user credentials
#  and generating a JWT token by using the functions defined in oauth2.py.

from fastapi import APIRouter, FastAPI, HTTPException, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2


#creates the router
router = APIRouter(tags = ['Authentication'])

# this oauth2 dependency is used to get the user from the database
# it is used in the login route to authenticate the user 

# OAuth2PasswordRequestForm is a form that is used to get the username and password from the user


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(),
          db: Session = Depends(database.get_db)):
   
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f"Invalid Credentials")
    
    # create a token 
    access_token = oauth2.create_access_token(data = {"user_id" : str(user.id)})

    # return tokemn
    return {"access_token": access_token, "token_type": "bearer"}