from fastapi import APIRouter
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
from Models.StocksModels import Users,PasswordRest
import re
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi_sqlalchemy import db
import os
import random
import uuid
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

AuthRouter =  APIRouter()

PasswordResetLink_BaseUrl = "http://localhost:5173/resetpassword"

conf = ConnectionConfig(
    MAIL_USERNAME="iamjagadeesh.d@gmail.com",
    MAIL_PASSWORD="ptkjiazovhzlpiyp", 
    MAIL_FROM="iamjagadeesh.d@gmail.com",
    MAIL_PORT=465,  
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,  
    MAIL_SSL_TLS=True,  
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


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

    username = UserDetails.username.strip()
    email = UserDetails.email.strip()
    password = UserDetails.password.strip()
    confirm_password = UserDetails.confirm_password.strip()

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

    email=UserLogin.email.strip()
    password=UserLogin.password.strip()
    
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



async def SendEmail(link: str, email: str, username: str):
    try:
        body = f"""
                    <html>
                    <body>
                        <p>Dear {username},</p>
                        <p>We received a request to reset the password for your Fintech Account.</p>
                        <p>If you made this request, use the Link below to proceed:</p>
                        <p><strong>Your Password Reset Link: {link}</strong></p>
                        <p>This Link will expire in 10 minutes.</p>
                        <p>If you didn't request a password reset, please ignore this email. Your account is safe, and no changes will be made.</p>
                        <p>If you need further assistance, please visit the Fintech Account Help Center.</p>
                        <p>Thank you.</p>
                    </body>
                    </html>
                """
            
        message = MessageSchema(
            subject="Password Reset Request From Fintech",
            recipients=[email],
            body=body,
            subtype='html'
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        return True
    except Exception as e:
        return False

def ResetLink(timer):
    generate_uuid = str(uuid.uuid4())
    expiry = datetime.now() + timedelta(minutes=timer)
    return generate_uuid, expiry

class forgotPassword(BaseModel):
    email: str    

@AuthRouter.post('/forgotpassword')
async def ForgotPassword(UserEmail:forgotPassword):

    email = UserEmail.email.strip()

    user = db.session.query(Users)

    # Validate email format
    if not validate_email_format(email):
        return JSONResponse(status_code=403, content={'message': 'Invalid email address'})
    
    if not email:
        return JSONResponse(status_code=403, content={"message": "Empty Values not Allowed"})
    
    exist_user = user.filter_by(email=email).first()

    if exist_user:
        unique_id, expiry = ResetLink(10)

        link = f"{PasswordResetLink_BaseUrl}?token={unique_id}"

        result = await SendEmail(link,exist_user.email,exist_user.username)

        if result:
            Savetoken = PasswordRest(user_id=exist_user.id,token = unique_id, expiry = expiry)
            db.session.add(Savetoken)
            db.session.commit()
            db.session.refresh(Savetoken)

            return JSONResponse(status_code = 200, content={"message":"Mail Sent Successfully"})
        else:
            return JSONResponse(status_code = 502, content={"message":"Unable to Send Mail"})
    else:
        return JSONResponse(status_code = 404, content={"message":"User Not Found"})

class ResetPass(BaseModel):
    password : str
    confirm_password: str

@AuthRouter.post('/resetpassword')
def ResetPassword(token : str,Reset : ResetPass):

    password = Reset.password.strip()
    confirm_password = Reset.confirm_password.strip()

    if password != confirm_password:
        return JSONResponse(status_code=403, content={"message": "Password Not Match"})

    query = db.session.query(PasswordRest).filter_by(token=token).first()

    user = db.session.query(Users).filter_by(id = query.user_id).first()

    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found."})
    
    if query:

        if datetime.now() < query.expiry:
            hashed_password = hash_password(password)
            user.password = hashed_password
            db.session.delete(query)
            db.session.commit()
            db.session.refresh(user)
            return JSONResponse(status_code = 200, content={"message": "Password reset successful!"})
        else:
            db.session.delete(query)
            db.session.commit()
            return JSONResponse(status_code = 403, content={"message": "Token Expired"})
    else:
        return JSONResponse(status_code = 404, content= {"message": "Token Not Found"})





        

        
