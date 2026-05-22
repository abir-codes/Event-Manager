from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from EventsUserDatabase import SessionLocal,engine
from EventsDatabaseModel import Base,User,Eventdb
from fastapi import FastAPI,HTTPException,Depends,Header
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt,JWTError
import EventsDatabaseModel
from EventsModel import CreateUser,Event
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://event-manager-wheat-three.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EventsDatabaseModel.Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated = 'auto'
)

def get_db():
    db =    SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(payload):
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

@app.post("/signup")
def create_user(user: CreateUser,db:Session = Depends(get_db)):
    existing_user = db.query(EventsDatabaseModel.User).filter(EventsDatabaseModel.User.username==user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        username = user.username,
        password = hashed_password
    )
    db.add(new_user)
    db.commit()
    return{
        "message":"User added"
    }

@app.post("/login")
def user_login(user: CreateUser,db:Session = Depends(get_db)):
    db_user = db.query(EventsDatabaseModel.User).filter(EventsDatabaseModel.User.username==user.username).first()
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )
    valid_password = pwd_context.verify(user.password,db_user.password)
    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    payload = {
        "sub":db_user.username,
        "user_id":db_user.id,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    access_token = create_token(payload)
    return{
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/events")
def add_event(event: Event,db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    new_event = Eventdb(
        title=event.title,
        category=event.category,
        due_date=event.due_date,
        priority=event.priority,
        status=event.status,
        notes=event.notes,
        owner_id=payload['user_id']
    )
    db.add(new_event)
    db.commit()
    return{"message":"Event added"}

@app.get("/events")
def get_events(db:Session = Depends(get_db),token:str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    events = []
    db_events = db.query(EventsDatabaseModel.Eventdb).filter(EventsDatabaseModel.Eventdb.owner_id==payload["user_id"]).all()
    if not db_events:
        return []
    for event in db_events:
        events.append({
            "id":event.id,
            "title":event.title,
            "category":event.category,
            "due_date":event.due_date,
            "priority":event.priority,
            "status":event.status,
            "notes":event.notes,
            "owner_id":payload["user_id"]
        })
    return events

@app.put("/events/{event_id}")
def edit_event(event_id: int, event: Event, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db_event = db.query(EventsDatabaseModel.Eventdb).filter(EventsDatabaseModel.Eventdb.id == event_id,EventsDatabaseModel.Eventdb.owner_id == payload['user_id']).first()
    if db_event:
        db_event.title = event.title
        db_event.category = event.category
        db_event.due_date = event.due_date
        db_event.priority = event.priority
        db_event.status = event.status
        db_event.notes = event.notes
        db_event.owner_id = payload['user_id']
        db.commit()
        return {"message": "Event edited"}
    return {"message": "Event not found"}

@app.delete("/events/{event_id}")
def delete_event(event_id: int,db:Session = Depends(get_db),token:str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    db_event = db.query(EventsDatabaseModel.Eventdb).filter(EventsDatabaseModel.Eventdb.id==event_id,EventsDatabaseModel.Eventdb.owner_id==payload['user_id']).first()
    if not db_event:
        return{"message":"Event not found"}
    db.delete(db_event)
    db.commit()
    return{"message":"Event deleted"}













