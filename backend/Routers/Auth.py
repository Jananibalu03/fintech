from fastapi import APIRouter
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
from Models.StocksModels import Users
import re
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi_sqlalchemy import db
import os

AuthRouter =  APIRouter()

#username validation
def validate_username(username):
    return re.match(r"^(?!\d+$)[a-zA-Z0-9]{3,15}$",username)

#email validation
def validate_email_format(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, email):
        return True
    else:
        return False
        
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def Get_Token(id):
    token = jwt.encode({'sub': str(id),'exp' : datetime.utcnow() + timedelta(days = 1)},os.getenv("SECRET_KEY"))
    return token

class Register(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

@AuthRouter.post('/register')
def Register(UserDetails : Register):

    username = UserDetails.username
    email = UserDetails.email
    password = UserDetails.password
    confirm_password = UserDetails.confirm_password

    query = db.session.query(Users)

    # Validate password match
    if password != confirm_password:
        return JSONResponse({'message': 'Confirm password does not match'})

    #username validation
    if not validate_username(username):
        return JSONResponse(status_code=403,content={"message": "Username should contain only letters and numbers, have a length between 3 and 15 characters, and cannot be only numbers."})

    # # Validate email format
    if not validate_email_format(email):
        return JSONResponse(status_code=403, content={'message': 'Invalid email address'})

    # Check if username already exists in the database
    existing_username=query.filter_by(username=username).first()
    if existing_username:
        return JSONResponse(status_code=403, content={'message': 'Username already exists'})

    # Check if email already exists in the database
    existing_email=query.filter_by(email=email).first()
    if existing_email:
        return JSONResponse(status_code = 403, content={'message': 'Email already exists'})

    # Hash the password before saving it
    hashed_password = hash_password(password)

    # empty fields
    if not username or not email or not password:
        return JSONResponse(status_code = 403, content={"message": "Empty Values not Allowed"})

    try:
        users=Users(username=username,email=email,password=hashed_password)
        db.session.add(users)
        db.session.commit()
        db.session.refresh(users)
        return JSONResponse(status_code = 201, content={'message': 'User registered successfully!'})

    except:
        return JSONResponse(status_code = 403, content={'message':"Oops! Something went wrong. Please try again later."})

class Login(BaseModel):
    email: str
    password: str

# #user login function
@AuthRouter.post('/login')
def Login(UserLogin: Login):

    email=UserLogin.email
    password=UserLogin.password
    
    query = db.session.query(Users)

    # Validate email format
    if not validate_email_format(email):
        return JSONResponse(status_code=403, content={'message': 'Invalid email address'})

    if not email or not password:
        return JSONResponse(status_code=403, content={"message": "Empty Values not Allowed"})
    
    #get the login user in the database
    valid_user= query.filter_by(email=email).first()
    
    if valid_user:
        user_id=valid_user.id
        encrypted_pass=valid_user.password
        #check if the password already exist in the database
        if bcrypt.checkpw(password.encode('utf-8'),encrypted_pass.encode('utf-8')):
            result=Get_Token(user_id)
            return JSONResponse(status_code=200,content={'message':'successfully login','access_token': result})
        else:
            return JSONResponse(status_code=403,content={'message':'Incorrect Password'})
    else:
        return JSONResponse(status_code=403, content={'message':'User not found!'})
    